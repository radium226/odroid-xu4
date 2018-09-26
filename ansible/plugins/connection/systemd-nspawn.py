# Based on chroot.py (c) 2013, Maykel Moya <mmoya@speedyrails.com>
# Based on chroot.py (c) 2015, Toshio Kuratomi <tkuratomi@ansible.com>
# (c) 2018, Enrico Zini <enrico@debian.org>
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import distutils.spawn
import os
import os.path
import pipes
import subprocess
import time
import hashlib

from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.plugins.connection import ConnectionBase, BUFSIZE
from ansible.module_utils.basic import is_executable

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class Connection(ConnectionBase):
    ''' Local chroot based connections '''

    transport = 'systemd-nspawn'
    has_pipelining = True
    # su currently has an undiagnosed issue with calculating the file
    # checksums (so copy, for instance, doesn't work right)
    # Have to look into that before re-enabling this
    become_methods = frozenset(C.BECOME_METHODS).difference(('su',))

    def __init__(self, play_context, new_stdin, *args, **kwargs):
        super(Connection, self).__init__(play_context, new_stdin, *args, **kwargs)

        self.chroot = self._play_context.remote_addr
        # We need short and fast rather than secure

        self.machine_name = "odroid-xu4"

        if os.geteuid() != 0:
            raise AnsibleError("nspawn connection requires running as root")

        self.nspawn_cmd = distutils.spawn.find_executable('systemd-nspawn')
        if not self.nspawn_cmd:
            raise AnsibleError("systemd-nspawn command not found in PATH")
        self.machinectl_cmd = distutils.spawn.find_executable('machinectl')
        if not self.machinectl_cmd:
            raise AnsibleError("machinectl command not found in PATH")
        self.run_cmd = distutils.spawn.find_executable('systemd-run')
        if not self.run_cmd:
            raise AnsibleError("systemd-run command not found in PATH")

        existing = subprocess.call([self.machinectl_cmd, "show", self.machine_name], stdout=open("/dev/null", "wb"))
        self.machine_exists = existing == 0

    def set_host_overrides(self, host, hostvars=None):
        super(Connection, self).set_host_overrides(host, hostvars)

    def _connect(self):
        ''' connect to the chroot; nothing to do here '''
        super(Connection, self)._connect()
        if not self._connected:
            if not self.machine_exists:
                display.vvv("Starting nspawn machine", host=self.chroot)
                self.chroot_proc = subprocess.Popen([self.nspawn_cmd, "-D", self.chroot, "-M", self.machine_name, "--register=yes", "--boot"], stdout=open("/dev/null", "w"))
                time.sleep(0.5)
            else:
                self.chroot_proc = None
                display.vvv("Reusing nspawn machine", host=self.chroot)
            self._connected = True

    def _local_run_cmd(self, cmd, stdin=None):
        display.vvv(" -exec %s" % repr(cmd), host=self.chroot)
        display.vvv(" -  or %s" % " ".join(pipes.quote(x.decode("utf-8")) for x in cmd), host=self.chroot)
        p = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate(stdin)
        display.vvv(" - got %d" % p.returncode, host=self.chroot)
        display.vvv(" - out %s" % repr(stdout), host=self.chroot)
        display.vvv(" - err %s" % repr(stderr), host=self.chroot)
        return p.returncode, stdout, stderr

    def _systemd_run_cmd(self, cmd, stdin=None):
        local_cmd = [self.run_cmd, "-M", self.machine_name, "-q", "--pipe", "--wait", "-E", "HOME=/root", "-E", "USER=root", "-E", "LOGNAME=root"] + cmd
        local_cmd = [x.encode("utf8") if isinstance(x, str) else x for x in local_cmd]
        return self._local_run_cmd(local_cmd, stdin=stdin)

    def exec_command(self, cmd, in_data=None, sudoable=False):
        ''' run a command on the chroot '''
        super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)

        display.vvv("cmd: %s" % repr(cmd), host=self.chroot)
        return self._systemd_run_cmd(["/bin/sh", "-c", cmd], stdin=in_data)

    def _prefix_login_path(self, remote_path):
        ''' Make sure that we put files into a standard path

            If a path is relative, then we need to choose where to put it.
            ssh chooses $HOME but we aren't guaranteed that a home dir will
            exist in any given chroot.  So for now we're choosing "/" instead.
            This also happens to be the former default.

            Can revisit using $HOME instead if it's a problem
        '''
        if not remote_path.startswith(os.path.sep):
            remote_path = os.path.join(os.path.sep, remote_path)
        return os.path.normpath(remote_path)

    def put_file(self, in_path, out_path):
        ''' transfer a file from local to chroot '''
        super(Connection, self).put_file(in_path, out_path)
        display.vvv("PUT %s TO %s" % (in_path, out_path), host=self.chroot)

        out_path = pipes.quote(self._prefix_login_path(out_path))
        p = subprocess.Popen([self.machinectl_cmd, "-q", "copy-to", self.machine_name, in_path, out_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise AnsibleError("failed to transfer file %s to %s:\n%s\n%s" % (in_path, out_path, stdout, stderr))

    def fetch_file(self, in_path, out_path):
        ''' fetch a file from chroot to local '''
        super(Connection, self).fetch_file(in_path, out_path)
        display.vvv("FETCH %s TO %s" % (in_path, out_path), host=self.chroot)

        in_path = pipes.quote(self._prefix_login_path(in_path))
        p = subprocess.Popen([self.machinectl_cmd, "-q", "copy-from", self.machine_name, in_path, out_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise AnsibleError("failed to transfer file %s from %s:\n%s\n%s" % (out_path, in_path, stdout, stderr))

    def close(self):
        super(Connection, self).close()

# FIXME: how can we power off the machine? close and __del__ seem to be called after each command
#    def __del__(self):
#        ''' terminate the connection; nothing to do here '''
#        # super(Connection, self).close()
#        display.vvv("CLOSE", host=self.chroot)
#        if self._connected:
#            p, stdout, stderr = self._local_run_cmd([self.machinectl_cmd, "poweroff", self.machine_name])
#            if p == 0 and self.chroot_proc:
#                self.chroot_proc.wait()
#            self._connected = False

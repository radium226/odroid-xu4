#!/usr/bin/env python

from sys import argv
from system.context import Context
from system.tools.ansible import Inventory, Ansible

def hostname():
    return "odroid-xu4-01"
    return socket.gethostname()

if __name__ == "__main__":
    if len(argv) in [3, 4] and argv[1] == "run-playbook":
        playbook_file_name = argv[2]
        with Context() as folder_path:
            inventory = Inventory.read(folder_path / "inventory.ini")
            limit = []
            if len(argv) == 4 and argv[3] == "--locally-only":
                local_host_name = hostname()
                inventory = inventory.modify_host(local_host_name, ansible_connection="local", ansible_port=None, ansible_host=None)
                limit = [local_host_name]
            Ansible(inventory).run_playbook(folder_path / playbook_file_name, limit=limit)

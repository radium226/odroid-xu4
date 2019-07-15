#!/usr/bin/env python

from subprocess import Popen
from whistleblower.client import Client

class Ansible:

    def __init__(self, inventory_file_path, vault_password_file_path = None):
        self.inventory_file_path = inventory_file_path
        self.vault_password_file_path = vault_password_file_path

    def run_playbook(self, playbook_file_path, limit=[], local=False):
        inventory_args = [f"--inventory-file={str(self.inventory_file_path)}"]
        limit_args = [f"--limit={','.join(limit)}"] if len(limit) > 0 else []
        connection_args = ["--connection=local"] if local else []
        playbook_args = [str(playbook_file_path)]
        vault_password_args = [f"--vault-password-file={str(self.vault_password_file_path)}"] if self.vault_password_file_path else []
        command = ["ansible-playbook"] + inventory_args + playbook_args + connection_args + vault_password_args + limit_args
        #print(f"command={command}")
        process = Popen(command)
        return_code = process.wait()

        client = Client()
        client.send_message(f"ansible-playbook has run and returned {return_code}")

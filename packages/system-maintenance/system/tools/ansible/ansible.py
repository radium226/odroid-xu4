#!/usr/bin/env python

from subprocess import Popen

class Ansible:

    def __init__(self, inventory):
        self.inventory = inventory

    def modify_host(self, host_name, **vars):
        new_inventory = self.inventory.modify_host(host_name, **vars)
        return Ansible(new_inventory)

    def run_playbook(self, playbook_file_path, limit=[]):
        inventory_file_path = self.inventory.write(temp=True)
        inventory_args = [f"--inventory-file={str(inventory_file_path)}"]
        limit_args = [f"--limit={','.join(limit)}"] if len(limit) > 0 else []
        playbook_args = [str(playbook_file_path)]
        process = Popen(["ansible-playbook"] + inventory_args + playbook_args + limit_args)
        process.wait()

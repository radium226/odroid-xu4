#!/usr/bin/env python

from tempfile import mkstemp
from pathlib import Path
from pprint import pprint

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager

from .host import Host
from .group import Group

class Inventory:

    def __init__(self, hosts=[], groups=[]):
        self.hosts = hosts
        self.groups = groups

    def modify_host(self, host_name, **new_vars):
        modified_hosts = list(map(lambda host: host.modify(**new_vars) if host.name == host_name else host, self.hosts))
        return Inventory(hosts=modified_hosts, groups=self.groups)

    def _format_hosts(self):
        return "\n".join(list(map(lambda host: host.format(), self.hosts)))

    def _format_groups(self):
        return "\n\n".join(list(map(lambda group: group.format(), self.groups)))

    def format(self):
        return "\n\n".join([self._format_hosts(), self._format_groups()])

    @classmethod
    def _parse(cls, ansible_inventory_manager):
        hosts = {}
        for ansible_host in ansible_inventory_manager.get_hosts():
            name = ansible_host.name
            print(" --> " + name)
            _vars = {var_name: ansible_host.vars[var_name] for var_name in (set(ansible_host.vars.keys()) - set(["inventory_dir", "inventory_file"]))}
            pprint(vars(ansible_host))
            hosts[name] = Host(name, vars=_vars)
        print("==================")
        print(hosts)
        print("==================")

        groups = {}
        for ansible_group in filter(lambda ansible_group: ansible_group.name not in ["all", "ungrouped"], ansible_inventory_manager.groups.values()):
            name = ansible_group.name
            _vars = {var_name: ansible_group.vars[var_name] for var_name in (set(ansible_group.vars.keys()))}
            pprint(vars(ansible_group))
            groups[name] = Group(name, host_names=list(map(lambda ansible_host: ansible_host.name, ansible_group.hosts)), vars=_vars)

        print("--------------------")
        print(groups)
        print("--------------------")
        return cls(hosts=list(hosts.values()), groups=list(groups.values()))

    @classmethod
    def read(cls, file_path):
        data_loader = DataLoader()
        ansible_inventory_manager = InventoryManager(data_loader, str(file_path))
        return cls._parse(ansible_inventory_manager)


    def write(self, file_path=None, temp=None):
        if temp:
            file_path = Path(mkstemp(prefix="inventory", suffix=".ini")[1])
            self.write(file_path=file_path)
            return file_path
        else:
            Path(file_path).write_text(self.format())
            return file_path

    def __str__(self):
        return f"Inventory(hosts={self.hosts}, groups={self.groups})"

    def __repr__(self):
        return str(self)

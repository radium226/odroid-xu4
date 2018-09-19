#!/usr/bin/env python

class Group:

    def __init__(self, name, host_names=[], vars={}):
        self.name = name
        self.host_names = host_names
        self.vars = vars

    def add_host(self, host):
        return Group(self.name, self.host_names + [host.name], self.vars)

    def add_vars(self, vars):
        return Group(self.name, self.hosts, {**self.vars, **vars})

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Group(name={self.name}, host_names={self.host_names}, vars={self.vars})"

    def format(self):
        return "\n".join([f"[{self.name}]"] + self.host_names)

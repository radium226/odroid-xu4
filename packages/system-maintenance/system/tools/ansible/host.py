#!/usr/bin/env python

class Host:

    def __init__(self, name, vars={}):
        self.name = name
        self.vars = vars

    def __str__(self):
        return f"Host(name={self.name}, vars={self.vars})"

    def __repr__(self):
        return str(self)

    def modify(self, **kwargs):
        _vars = {**self.vars, **kwargs}
        return Host(self.name, vars={var_name: _vars[var_name] for var_name in set(filter(lambda var_name: _vars[var_name], _vars.keys()))})

    def format(self):
        return " ".join([self.name] + list(map(lambda p: f"{p[0]}={p[1]}", self.vars.items())))

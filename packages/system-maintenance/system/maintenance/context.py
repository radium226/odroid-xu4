#!/usr/bin/env python

from functools import reduce
import os
import toml
from pathlib import Path
import socket


class Context:

    DEFAULT_CONFIG = {
        "provision": {
            "host_name": socket.gethostname(),
            "inventory_file_path": "inventory.ini",
            "playbook_file_path": "provision.yml"
        }
    }

    def __init__(self):
        self.config = Context._read_config()

    def __str__(self):
        return f"Context(config={self.config})"

    def __repr__(self):
        return str(self)

    @staticmethod
    def _read_config():
        file_paths = [
            Path("/etc/system-maintenance.toml"),
            Path(os.getcwd()) / "system-maintenance.toml"
        ]
        print(file_paths)
        config = reduce(lambda left_config, right_config: {**left_config, **right_config},
            map(lambda file_path: toml.loads(file_path.read_text()),
                filter(lambda file_path: file_path.exists(), file_paths)), Context.DEFAULT_CONFIG)
        return config

if __name__ == "__main__":
    context = Context()
    print(context)

#!/usr/bin/env python

from functools import reduce
import os
import toml
from pathlib import Path
import socket

from deepmerge import Merger
from copy import deepcopy

class Context:

    DEFAULT_CONFIG = {
        "provision": {
            "host_name": socket.gethostname(),
            "inventory_file_path": "inventory.ini",
            "playbook_file_path": "provision.yml",
            "git_repo_url": "https://github.com/radium226/odroid-xu4.git",
            "folder_path": "ansible"
        }
    }

    def __init__(self):
        self.config = Context._read_config()
        self.vault_password_file_path = Path("/etc/system-maintenance/vault-password")

    def __str__(self):
        return f"Context(config={self.config})"

    def __repr__(self):
        return str(self)

    @staticmethod
    def _merge_config(left_config, right_config):
        merger = Merger(
            [
                (list, ["append"]),
                (dict, ["merge"])
            ],
            ["override"],
            ["override"]
        )
        merged_config = deepcopy(left_config)
        merger.merge(merged_config, right_config)
        return merged_config

    @staticmethod
    def _read_config():
        file_paths = [
            Path("/etc/system-maintenance.toml"),
            Path("/etc/system-maintenance/config.toml"),
            Path(os.getcwd()) / "system-maintenance.toml"
        ]
        print(file_paths)
        config = reduce(Context._merge_config,
            map(lambda file_path: toml.loads(file_path.read_text()),
                filter(lambda file_path: file_path.exists(), file_paths)), Context.DEFAULT_CONFIG)
        return config

if __name__ == "__main__":
    context = Context()
    print(context)

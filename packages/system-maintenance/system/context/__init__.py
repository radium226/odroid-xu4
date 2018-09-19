#!/usr/bin/env python

from functools import reduce
import os
import toml
from pathlib import Path

class Context:

    def __init__(self):
        self.config = Context._read_config()

    def __str__(self):
        return f"Context(config={self.config})"

    def __repr__(self):
        return str(self)

    def __enter__(self):
        return Path(self.config["provisioning"]["folder_path"])

    def __exit__(self, type, value, traceback):
        pass

    @staticmethod
    def _read_config():
        file_paths = [
            Path("/etc/system-maintenance.toml"),
            Path(os.getcwd()) / "system-maintenance.toml"
        ]
        print(file_paths)
        config = reduce(lambda left_config, right_config: {**left_config, **right_config},
            map(lambda file_path: toml.loads(file_path.read_text()),
                filter(lambda file_path: file_path.exists(), file_paths)), {})
        return config

if __name__ == "__main__":
    context = Context()
    print(context)

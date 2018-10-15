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
        "telegram": {
            "token": "TOKEN",
            "chat_id": "CHAT_ID"
        }
    }

    def __init__(self):
        self.config = Context._read_config()

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
            Path("/etc/whistleblower.toml"),
            Path(os.getcwd()) / "whistleblower.toml"
        ]
        config = reduce(Context._merge_config,
            map(lambda file_path: toml.loads(file_path.read_text()),
                filter(lambda file_path: file_path.exists(), file_paths)), Context.DEFAULT_CONFIG)
        return config

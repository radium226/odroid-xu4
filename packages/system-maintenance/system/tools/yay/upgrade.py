#!/usr/bin/env python

import re

from .package import Package

class Upgrade:

    LINE_PATTERN = "^(?P<package_name>\S+) (?P<old_version>\S+) -> (?P<new_version>\S+)$"

    def __init__(self, package, old_version, new_version):
        self.package = package
        self.old_version = old_version
        self.new_version = new_version

    @classmethod
    def parse_lines(cls, lines):
        for line in lines:
            match = re.search(cls.LINE_PATTERN, line)
            if match:
                package_name = match.group("package_name")
                old_version = match.group("old_version")
                new_version = match.group("new_version")
                yield cls(Package(package_name), old_version, new_version)

    def __str__(self):
        return f"Upgrade(package={self.package}, old_version={self.old_version}, new_version={self.new_version})"

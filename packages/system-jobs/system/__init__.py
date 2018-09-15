#!/usr/bin/env python

import subprocess as sp
import re

class Package:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Package(name={self.name})"

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

class System:

    @classmethod
    def refresh_available_packages(cls):
        process = sp.Popen(["yay", "-Sy", "--noconfirm"])
        process.wait()

    @classmethod
    def list_upgrades(cls):
        return list(cls._yield_upgrades())

    @classmethod
    def upgrade_packages(cls, packages):
        process = sp.Popen(["yay", "-S"] + list(map(lambda package: package.name, packages)) + ["--noconfirm"])
        process.wait()

    @classmethod
    def _yield_upgrades(cls):
        process = sp.Popen(["yay", "-Qu", "--devel", "--noconfirm"], stdin=None, stdout=sp.PIPE)
        lines = map(lambda b: b.decode("utf-8").strip(), iter(process.stdout.readline, b""))
        yield from Upgrade.parse_lines(lines)

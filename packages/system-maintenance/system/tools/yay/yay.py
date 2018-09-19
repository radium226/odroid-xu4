#!/usr/bin/env python

from subprocess import Popen, PIPE

from .upgrade import Upgrade

class Yay:

    @classmethod
    def refresh_available_packages(cls):
        process = Popen(["yay", "-Sy", "--noconfirm"])
        process.wait()

    @classmethod
    def list_upgrades(cls):
        return list(cls._yield_upgrades())

    @classmethod
    def upgrade_packages(cls, packages):
        process = Popen(["yay", "-S"] + list(map(lambda package: package.name, packages)) + ["--noconfirm"])
        process.wait()

    @classmethod
    def _yield_upgrades(cls):
        process = Popen(["yay", "-Qu", "--devel", "--noconfirm"], stdin=None, stdout=PIPE)
        lines = map(lambda b: b.decode("utf-8").strip(), iter(process.stdout.readline, b""))
        yield from Upgrade.parse_lines(lines)

#!/usr/bin/env python

from yay import System
from .prompt import Prompt, AlwaysYesPrompt, AlwaysNoPrompt

def list_upgrades():
    upgrades = System.list_upgrades()
    for upgrade in upgrades:
        print(f"{upgrade.package} is going to be updated from {upgrade.old_version} to {upgrade.new_version}")

def upgrade_packages(prompt):
    System.refresh_available_packages()
    upgrades = System.list_upgrades()
    if prompt.validate_upgrades(upgrades) == Prompt.YES:
        packages = map(lambda upgrade: upgrade.package, upgrades)
        System.upgrade_packages(packages)

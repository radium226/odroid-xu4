#!/usr/bin/env python

from system.prompt import Prompt, AlwaysYesPrompt, AlwaysNoPrompt
from system.tools.yay import Yay

def upgrade(prompt):
    Yay.refresh_available_packages()
    upgrades = Yay.list_upgrades()
    if prompt.validate(upgrades) == Prompt.YES:
        packages = map(lambda upgrade: upgrade.package, upgrades)
        Yay.upgrade_packages(packages)

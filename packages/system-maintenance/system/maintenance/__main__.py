#!/usr/bin/env python

from sys import argv
from system.maintenance import list_upgrades, upgrade_packages, AlwaysYesPrompt, AlwaysNoPrompt

def main(arguments):
    if arguments[1] == "list-upgrades":
        list_upgrades()
    elif arguments[1] == "upgrade-packages":
        upgrade_packages(AlwaysYesPrompt())
    else:
        print("Nothing to do!")

if __name__ == "__main__":
    main(argv)

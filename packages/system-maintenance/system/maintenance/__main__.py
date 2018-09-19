#!/usr/bin/env python

from sys import argv

from system.maintenance import upgrade, provision
from system.prompt import AlwaysYesPrompt

def main(arguments):
    if len(arguments) == 2:
        if arguments[1] == "upgrade":
            upgrade(AlwaysYesPrompt())
        elif arguments[1] == "provision":
            provision(AlwaysYesPrompt())
        else:
            "Nothing to do!"
    else:
        print("Still nothing to do!")

if __name__ == "__main__":
    main(argv)

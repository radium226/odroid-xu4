#!/bin/env python

import os
from setuptools import setup

def version():
    try:
        return os.environ["PKGVER"]
    except:
        with open("./VERSION.txt", "r") as f:
            return f.read().strip()

def name():
    try:
        return os.environ["PKGNAME"]
    except:
        return os.path.basename(os.getcwd())

setup(
    name=name(),
    version=version(),
    description="Whistleblower",
    license="GPL",
    zip_safe=True,
    install_requires=[],
    scripts=[
        "scripts/whistleblowerctl",
        "scripts/whistleblowerd"
    ],
    packages=[
        "whistleblower.server",
        "whistleblower.client",
        "whistleblower.dbus"
    ]
)

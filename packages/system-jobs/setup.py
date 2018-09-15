#!/bin/env python

from setuptools import setup

setup(
    name="yay-jobs",
    version="1.0",
    description="Some timers for Yay",
    license="GPL",
    zip_safe=True,
    install_requires=[],
    scripts=[],
    packages=[
        "system",
        "system.jobs"
    ]
)

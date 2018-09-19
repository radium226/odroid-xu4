#!/usr/bin/env python

from subprocess import Popen

def git(*args):
    process = Popen(["git"] + list(args))
    process.wait()

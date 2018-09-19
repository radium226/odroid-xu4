#!/usr/bin/env python

class Package:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Package(name={self.name})"

#!/usr/bin/env python

from abc import ABC, abstractmethod

class Prompt(ABC):

    YES = "yes"
    NO = "no"

    @abstractmethod
    def validate(upgrades):
        pass

class AlwaysYesPrompt(Prompt):

    def validate(self, upgrades):
        return Prompt.YES

class AlwaysNoPrompt(Prompt):

    def validate(self, upgrades):
        return Prompt.NO

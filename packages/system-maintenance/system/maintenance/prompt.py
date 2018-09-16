#!/usr/bin/env python

from abc import ABC, abstractmethod

class Prompt(ABC):

    YES = "yes"
    NO = "no"

    @abstractmethod
    def validate_upgrades(upgrades):
        pass

class AlwaysYesPrompt(Prompt):

    def validate_upgrades(self, upgrades):
        return Prompt.YES

class AlwaysNoPrompt(Prompt):

    def validate_upgrades(self, upgrades):
        return Prompt.NO

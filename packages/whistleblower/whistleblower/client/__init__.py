#!/usr/bin/env python

from pydbus import SystemBus
from gi.repository import GLib
from whistleblower.dbus import Interface


class Client:

    def __init__(self):
        bus = SystemBus()
        self.interface = bus.get(Interface.SERVICE_NAME)

    def send_message(self, text):
        self.interface.SendMessage(text)

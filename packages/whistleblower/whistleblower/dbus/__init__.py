#!/usr/bin/env python

from pydbus import SessionBus
from pydbus.generic import signal

from time import sleep

from whistleblower.server import Server

class Interface(object):
    """
        <node>
            <interface name='com.github.radium226.whistleblower.Whistleblower'>
                <signal name='MessageReceived'>
                    <arg type='s' />
                </signal>
                <method name='SendMessage'>
                    <arg name='keys' type='s' direction='in'/>
                </method>
            </interface>
        </node>
    """

    SERVICE_NAME = "com.github.radium226.Whistleblower"

    MessageReceived = signal()

    def __init__(self, server):
        self.server = server

    def SendMessage(self, text):
        self.server.send_message(text)

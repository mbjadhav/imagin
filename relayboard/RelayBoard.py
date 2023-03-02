import os
import argparse
import subprocess
import re
import serial
import sys
import time

class RelayBoard():
    def __init__(self,  channel=0, value=0, stack=0):
        self.channel=channel
        self.value=value
        self.stack=0

    def relwr(self, channel, value):
        command = "ioplus {} relwr {} {}".format(self.stack,channel,value)
        os.system(command)
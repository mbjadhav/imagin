import os
import argparse
import subprocess
import re
import serial
import sys
import time 

class RelayBoard():
    def __init__(self,  channel=0, value=0):
        self.channel=channel
        self.value=value

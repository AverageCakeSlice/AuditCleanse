from __future__ import print_function
import os
import ctypes
import stat
import platform
import sys
import argparse
from datetime import datetime, timedelta, date
import time
import pyperclip
import pysnow
import getpass
import subprocess
from colorama import Fore, Back, Style
from termcolor import cprint

from os.path import expanduser
import logging
import re
import urllib.request

import ssl
ssl._create_default_https_context = ssl._create_unverified_context



try:
        from msvcrt import getch,kbhit
        OS = True
except ImportError:
        OS = False
        from getch import getch
        import termios




def checkPriv():
        import ctypes, sys
        if is_admin():
                pass
        else:
                #try:
                        ctypes.windll.shell32.ShellExecuteW(None, u'runas', sys.executable, "", None, 1)
                #       sys.exit()
                #except:
                #       pass
                #raise Exception('Run the script as super user! [sudo ./script]')

def is_admin():
        if OS:
                try:
                        return ctypes.windll.shell32.IsUserAnAdmin()
                except:
                        return False
        else:
                try:
                        is_admin = os.getuid() == 0
                        return True
                except:
                       return False



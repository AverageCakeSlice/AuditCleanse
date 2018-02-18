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




def checkVersion():
        try:
                os.remove(_desktop + 'updater.exe')
                clear()
                print(Changelog)
                newLine()
                line()
                input('  Press enter to continue...')
                return
        except:
                pass
        try:
            urllib.request.urlretrieve("http://helpdesk.liberty.edu/hdtools/scripts/Python/v.ersion", "v.ersion")
        except:
            print('Error Connecting to Libertys Network.')
            return

        filename = os.path.basename(__file__).split('.')
        with open ('v.ersion') as version_file:
                for i,line in enumerate(version_file):
                        if filename[0] in line:
                                versionLine = line
                                break;
        try:
                os.remove("v.ersion")
        except:
                pass
        
        versionLine = versionLine.split(" ")
        versionLine = versionLine[1].strip()
        nV = versionLine.split(".")

        if (   int(nV[0]) >  int(version[0])
                or int(nV[0]) == int(version[0]) and int(nV[1]) >  int(version[1])
                or int(nV[0]) == int(version[0]) and int(nV[1]) == int(version[1]) and int(nV[2]) >  int(version[2])
                or int(nV[0]) == int(version[0]) and int(nV[1]) == int(version[1]) and int(nV[2]) == int(version[2]) and nV[3] >  version[3]):
                if platform.system() == 'Windows':
                        wUpdate() #Windows update
                else:
                        uUpdate() #UNIX update
        else:
                pass


def wUpdate():
        print('Update Available!')
        print('  Update? [Y/n]')
        checkChar = wait() 
        #input('  check char is ' + checkChar)
        if checkChar == 'Y' or checkChar == 'y':
            os.system('cls')
            print('')
            print('UPDATING...')
            ini = open(_desktop + 'u.pdate', 'w+')
            ini.write(_filePath + '|')
            ini.write(_scriptname + '|')
            ini.write(_downloadDIR)
            ini.close()
            urllib.request.urlretrieve('http://helpdesk.liberty.edu/hdtools/scripts/Python/updater.exe', _desktop + 'updater.exe')
            subprocess.Popen(_desktop + 'updater.exe')
            sys.exit()
        else:
            pass



def uUpdate():
        newFile = os.path.basename(__file__)
        
        if platform.system() == 'Windows':
                desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
        else:
                desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        
        while True:
                if newFile[-1] == '.':
                        newFile = newFile[:-1]
                        break
                newFile = newFile[:-1]
        newpath = desktop + '/' + newFile

        if platform.system() == 'Windows':
                updateURL = "http://helpdesk.liberty.edu/hdtools/scripts/Python/"  + newFile + '.exe'
                newpath = newpath + '.exe'
        else:
                updateURL = "http://helpdesk.liberty.edu/hdtools/scripts/Python/"  + newFile
        
        try:
                urllib.request.urlretrieve(updateURL, newpath)
        except:
                urllib.urlretrieve(updateURL, newpath)

        if platform.system() != 'Windows':
                st = os.stat(newpath)
                os.chmod(newpath, st.st_mode | stat.S_IEXEC)
        
        print('Please restart the script. It has updated!\n')
        print('  It was moved to your Desktop folder.')
        input('...') 
        os.system(newpath)
        sys.exit()

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


import _updateHandler
import _priviledgeHandler
import _glob

try:
        from msvcrt import getch,kbhit
        OS = True
except ImportError:
        OS = False
        from getch import getch
        import termios

def logo():
    clear()
    print(glob._logo)


def PR_(title_, list_ = [], program_name = glob._scriptname):
        while True:
                header()
                line()
                print(' -  ' + title_)                          #
                line()

                index = 0       

                for i, item in enumerate(list_):
                        ind = i + 1
                        print('[' + format(ind) + '] ' + item)
                line()
                itemNum = input(' -      Please choose an item and press enter: ')

                # if itemNum in listofitems:                    

                try:                                            # If input string is not a number, loop and try again
                        itemNum = int(itemNum)
                        itemNum = itemNum - 1
                except:                                         #
                        continue                                #

                if len(list_) < itemNum + 1:    # If item does not exist in list, loop and try again; else return number
                        print(' - ERROR! -')                    #
                else:                                                           #
                        header()
                        return itemNum                                  #
#} end of pr()





        
def cleanup(dir_name = 'C:\\HelpdeskTools'):
                shutil.rmtree(dir_name)
                endFooter()

def clear():
                if OS:
                        os.system('cls')
                else:
                        os.system('clear')
                return

def setup(dir_name = 'C:\\HelpdeskTools'):       
                try:
                    os.stat(dir_name)
                except:
                    os.mkdir(dir_name)

def dl_Python(file_name, dir_name = 'C:\\HelpdeskTools'):
    try:
        urllib.urlretrieve('http://helpdesk.liberty.edu/hdtools/scripts/python/' + file_name, dir_name + '\\' + file_name)
        return True
    except:
        return False

def dl_HDTool(dl_dir, file_name, dir_name = 'C:\\HelpdeskTools'):
    try:
        urllib.urlretrieve('http://helpdesk.liberty.edu/hdtools/' + dl_dir, dir_name + '\\' + file_name)
        return True
    except:
        return False
def dl_Web(url, file_name, dir_name = 'C:\\HelpdeskTools'):
                urllib.urlretrieve(url, dir_name + '\\' + file_name)

def header(program_name = _scriptname):
                clear()
                logo()
                print("----------------------------------- KB0015731 ----------------------------------")
                print('  Designed and Written for use in Liberty IT Helpdesk')
                line()
                newLine()

def endFooter(completion_color = 'a0'):
                global _reimageBool
                newLine(3)
                line()
                print('  Questions / Recommendations? Talk to a T1+')
                print('  Press any key to exit')
                if(_reimageBool == 0):
                                try:
                                        os.system('color ' + completion_color)
                                except:
                                        pass
                wait()
                sys.exit()

def line(num = 80):
                print('-' * num)

def newLine(num = 1):
                print('\n' * num)
                
def wait(string = '', clear = False):
                if clear:
                        header()
                if string == '':
                        pass
                else:
                        print(string)
                        print('\n')
                flush_input()
                if platform.system() == 'Windows': #to split the list into useable CS# / Serial#
                        return getch().decode('utf-8')
                else:
                        return getch()

def flush_input():
        try:
                while kbhit():
                        getch()
        except:
                pass

from __future__ import print_function
import os
import platform
import sys
import subprocess
import urllib.request


import _updateHandler
import _priviledgeHandler
import _glob

try:
    from msvcrt import getch,kbhit
except ImportError:
    from getch import getch
    import termios


def PR_(title_, list_ = []):
    while True:
        header()
        title(title_)

        for i, item in enumerate(list_):
            print('[' + format(i + 1) + '] ' + item)
        line()
        itemNum = input(' -      Please choose an item and press enter: ')
        
        try:    # If input string is not a number, loop and try again
            itemNum = int(itemNum) - 1
        except:
            continue
        if len(list_) < itemNum + 1:    # If item does not exist in list, loop and try again; else return number
            print(' - ERROR! -')
        else:
            header()
            return itemNum


def title(phrase):
    line()
    print(' -  ' + phrase)
    line()

        
def cleanup(dir_name = 'C:\\HelpdeskTools'):
    shutil.rmtree(dir_name)
    endFooter()


def clear():
    if platform.system() == 'Windows':
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


def header(kb = "---------"):
    clear()
    print(_glob.logo)
    print("----------------------------------- " + kb + " ----------------------------------")
    print('  Designed and Written for use in Liberty IT Helpdesk')
    line()
    newLine()


def endFooter(completion_color = 'a0', check = 0):
    newLine(3)
    line()
    print('  Questions / Recommendations? Talk to a T1+')
    print('  Press any key to exit')
    if(check == 0):
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

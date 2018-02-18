import os
import ctypes
import platform
import sys


def checkPriv():
    import ctypes, sys
    if is_admin():
        pass
    else:
        try:
            ctypes.windll.shell32.ShellExecuteW(None, u'runas', sys.executable, "", None, 1)
            sys.exit()
        except:
            pass
        raise Exception('Run the script as super user! [sudo ./script]')


def is_admin():
    if platform.system() == "Windows":
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



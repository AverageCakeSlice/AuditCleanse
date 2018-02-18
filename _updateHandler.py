from __future__ import print_function
import os
import ctypes
import platform
import sys
import subprocess
import urllib.request

import _glob

def checkVersion():
    try:
        os.remove(_glob.desktop + 'updater.exe')
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


def wUpdate():
    print('')
    print('-'*80)
    print('Update Available!')
    print('  Update? [Y/n]')
    checkChar = wait() 
    if checkChar == 'Y' or checkChar == 'y':
        os.system('cls')
        print('')
        print('UPDATING...')
        ini = open(_glob.desktop + 'u.pdate', 'w+')
        ini.write(_glob.filePath + '|')
        ini.write(_glob.scriptname + '|')
        ini.write(_glob.downloadDIR)
        ini.close()
        urllib.request.urlretrieve('http://helpdesk.liberty.edu/hdtools/scripts/Python/updater.exe', _glob.desktop + 'updater.exe')
        subprocess.Popen(_glob.desktop + 'updater.exe')
        sys.exit()
    else:
        pass



def uUpdate():
    newFile = os.path.basename(__file__)
        
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop') 
        
    while True:
        if newFile[-1] == '.':
            newFile = newFile[:-1]
            break
        newFile = newFile[:-1]
    newpath = desktop + '/' + newFile

    updateURL = "http://helpdesk.liberty.edu/hdtools/scripts/Python/"  + newFile
    
    urllib.request.urlretrieve(updateURL, newpath)

    st = os.stat(newpath)
    os.chmod(newpath, st.st_mode | stat.S_IEXEC)
        
    print('  Please restart the script. It has updated!\n')
    print('  It was moved to your Desktop folder.') 
    os.system(newpath)
    sys.exit()



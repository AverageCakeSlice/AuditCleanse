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
import _toolsHandler
import _glob

try:
        from msvcrt import getch,kbhit
        OS = True
except ImportError:
        OS = False
        from getch import getch
        import termios


'''
 ---------------------------------------
  Maintenance Variables 
 --------------------------------------- '''

_glob.version = [1, 1, 2, 'b']
_glob.scriptname = os.path.basename(__file__).split('.')[0] + '.exe'
_glob.downloadDIR = '/scripts/Python'
_glob.filePath = os.path.realpath(__file__).split('.')[0] + '.exe'





'''
 ---------------------------------------
  Logo
 --------------------------------------- '''

_glob.logo = """
--------------------   █████  ██    ██ ██████  ██ ████████  --------------------
--------------------  ██   ██ ██    ██ ██   ██ ██    ██     --------------------
--------------------  ███████ ██    ██ ██   ██ ██    ██  -----------------------
--------------------  ██   ██ ██    ██ ██   ██ ██    ██  -----------------------
-------------------   ██   ██  ██████  ██████  ██    ██  -----------------------
-----------  ██████ ██      ███████  █████  ███    ██ ███████ ███████ ----------
----------  ██      ██      ██      ██   ██ ████   ██ ██      ██      ----------
----------  ██      ██      █████   ███████ ██ ██  ██ ███████ █████ ------------
----------  ██      ██      ██      ██   ██ ██  ██ ██      ██ ██     -----------
-----------  ██████ ███████ ███████ ██   ██ ██   ████ ███████ ███████ ----------"""





'''
 ---------------------------------------
  Changelog
 --------------------------------------- '''

Changelog = """
------------------------------
AuditCleanse -- Version 1.1.2b
------------------------------
        RECENT UPDATES
        --------------
-- 1.1.2b
        Fixed duplicate issue

-- 1.1.1d
        Fixed uppercase issue

-- 1.1.1c
        Fixed immediate close
        Fixed Empty TKT update

-- 1.1.1b
        Minor fixes
"""





'''
 ---------------------------------------
  Global Variables
 --------------------------------------- '''
# NONE BROSKI #neveruseglobal


'''
 ---------------------------------------
  Main
 --------------------------------------- '''

def main():
        _priviledgeHandler.checkPriv()
        _updateHandler.checkVersion()
        _toolsHandler.header()

        AuditDictionary = {}
        #       Holds many different items based on each CS# entry
        AuditList = []
        #       Holds a list of the items on the Audit for easier handling
        totalTicketNumber = 0
        #       Holds total number of items on the Audit
        GoodScannedList = []
        #       List of items on Audit accounted for
        WronglyScannedList = []
        #       List of items that were scanned but not on the Audit




        #       -----
        #       ServiceNow Objects
        #       -----
        username, serviceNow, auditTKT = login()
        
        u_computer_supportTable = serviceNow.resource(api_path='/table/u_computer_support')
        #       Service Now object to search items in the u_computer_support table
        sys_userTable = serviceNow.resource(api_path='/table/sys_user')
        #       Service Now object to search for users and information based on their sysID
        taskTable = serviceNow.resource(api_path='/table/task')

        auditChoice, u_depot_location, u_location = auditSetup()

        AuditList, totalTicketNumber = QueryGen(auditChoice, u_depot_location, u_location, serviceNow)

        

        if auditChoice == 0 or auditChoice == 1:
                gatherer(serviceNow, AuditDictionary, AuditList, totalTicketNumber, sys_userTable, u_computer_supportTable)
                sorted(AuditList, key=lambda x: (AuditDictionary[x]['state'], AuditDictionary[x]['username']))
                repairer(serviceNow, AuditDictionary, AuditList, sys_userTable, u_computer_supportTable)
                _toolsHandler.header()
                NotScannedList = auditConsole(AuditDictionary, AuditList, GoodScannedList, WronglyScannedList)
                WronglyScannedListDict = {}

                if len(NotScannedList) > 0:
                        _toolsHanlder.header()
                        print(Fore.CYAN + '  Not Scanned Items:' + Style.RESET_ALL)
                        printer(AuditDictionary, NotScannedList)
                        print('')
                        input('  Press Enter to Continue.')

                if len(WronglyScannedList) > 0:
                        _toolsHanlder.header()
                        print(Fore.CYAN + '  Errorly Scanned Items:' + Style.RESET_ALL)
                        gatherer(serviceNow, WronglyScannedListDict, WronglyScannedList, len(WronglyScannedList), sys_userTable, u_computer_supportTable)
                        printer(WronglyScannedListDict, WronglyScannedList)
                        print('')
                        input('  Press Enter to Continue.')
        

                u_computer_supportTable = serviceNow.resource(api_path='/table/u_computer_support')
                #       Service Now object to search items in the u_computer_support table
                sys_userTable = serviceNow.resource(api_path='/table/sys_user')
                #       Service Now object to search for users and information based on their sysID

                for i,each in enumerate(GoodScannedList):
                        _toolsHanlder.header()
                        print('          Updating Tickets')
                        print('       ' + format(i) + ' / ' + format(len(GoodScannedList)))
                        updateCS(serviceNow, each, 'work_notes', username + ' verified this device is at ' + u_location + ' on the Daily Repair Audit.', u_computer_supportTable)
                
                
        else:
                _toolsHanlder.header()
                NotScannedList = auditConsole({}, AuditList, GoodScannedList, WronglyScannedList)
                if len(NotScannedList) > 0:
                        _toolsHanlder.header()
                        print(Fore.CYAN + '  Not Scanned Items:' + Style.RESET_ALL)
                        for i,each in enumerate(NotScannedList):
                                print(' ' + format(i).center(3) + ' | ' + each)
                        print('')
                        input('  Press Enter to Continue.')

                if len(WronglyScannedList) > 0:
                        _toolsHanlder.header()
                        print(Fore.CYAN + '  Errorly Scanned Items:' + Style.RESET_ALL)
                        for i,each in enumerate(WronglyScannedList):
                                print(' ' + format(i).center(3) + ' | ' + each)
                        print('')
                        input('  Press Enter to Continue.')


        taskTable = serviceNow.resource(api_path='/table/task')

        auditCloser(WronglyScannedList, NotScannedList, auditTKT, taskTable, serviceNow)
        print('')
        print(Fore.RED + '  THE PROGRAM IS NOW COMPLETE.' + Style.RESET_ALL)
        print('\n'*2)
        wait('Press any key to close.')
        sys.exit()



'''
 ---------------------------------------
  Script-Specific Function Declaration
 --------------------------------------- '''



def auditCloser(WrongList_, NotList_, audittkt, table, serviceNow):
        _toolsHanlder.header()
        print('  The Audit TKT has been updated.')
        string = ''
        if NotList_ != []:
                string += 'The following items were not found, along with the resolution to find them:\n'
                for each in NotList_:
                        string += '- ' + each + ' -  Resolution: \n'
        if WrongList_ != []:
                string += 'The following items were scanned but not on the audit, along with their resolution:\n'
                for each in WrongList_:
                        string += '- ' + each + ' -  Resolution: \n'
        if NotList_ == [] and WrongList_ == []:
                string = 'All tickets were accounted for.'
        updateCS(serviceNow, audittkt, 'description', string, table)



def login():
    import getpass
    username = input('Please input your Liberty Username: ')
    password = getpass.getpass('Please input your Liberty Password: ')
    ticket = input('Please input your Audit TKT: ')

    serviceNow = pysnow.Client(instance='Liberty', user=username, password=password)

    return username, serviceNow, ticket



def repairer(serviceNow, AuditDictionary_, AuditList_, sys_userTable, u_computer_supportTable):
    UpdatedList = []
    for ticket in AuditList_:       
        if AuditDictionary_[ticket]['state'] == 'Open':
            if AuditDictionary_[ticket]['username'] == '' and AuditDictionary_[ticket]['substate'] != 'In Queue':
                updateCS(serviceNow, ticket, 'u_substate', '489fb3f02b3c9200258f89efe8da156d', u_computer_supportTable)

            elif AuditDictionary_[ticket]['username'] != '' and AuditDictionary_[ticket]['substate'] == 'In Queue':
                updateCS(serviceNow, ticket, 'state', '2', u_computer_supportTable)
                updateCS(serviceNow, ticket, 'u_substate', '', u_computer_supportTable)
                        
            elif AuditDictionary_[ticket]['username'] != '':
                updateCS(serviceNow, ticket, 'state', '2', u_computer_supportTable)
           
            else:
                continue

            UpdatedList.append(ticket)      
    gatherer(serviceNow, AuditDictionary_, UpdatedList, len(UpdatedList), sys_userTable, u_computer_supportTable)



def updateCS(serviceNow, Ticket_, Field_, Payload_, Table_):
    update = {Field_:Payload_}
    pushUpdate = Table_.update(query={'number':Ticket_}, payload=update)
    return True
        


def printer(AuditDictionary_, subList):
    print(Style.BRIGHT + Fore.RED + '  #  |    Item     |    Assigned  To    |   State   |         Substate          ')
    print(Style.RESET_ALL + '-----|-------------|--------------------|-----------|---------------------------')
    toggle = True

    for i,k in enumerate(subList):
        if toggle:
            toggle = False
            print(Style.BRIGHT, end="")
        else:
            toggle = True
            print(Style.RESET_ALL, end="")

        print(' ' + format(i + 1)[:3].center(3), end='')
        print(' | ', end='')
        print(k[:11].center(11), end="")
        print(' | ', end='')
        print(AuditDictionary_[k]['username'][:18].center(18), end="")
        print(' | ', end='')

        if AuditDictionary_[k]['state'] == 'Closed':
            print(Style.BRIGHT, end='')
            print(Fore.YELLOW + AuditDictionary_[k]['state'].center(9), end="")
            print(Fore.RESET + ' | ', end='')
            print(Fore.YELLOW + AuditDictionary_[k]['substate'][:25].center(25))
            print(Fore.RESET, end='')
            if toggle:
                print(Style.BRIGHT, end="")
            else:
                print(Style.RESET_ALL, end="")
        
        elif AuditDictionary_[k]['state'] == 'Open' or AuditDictionary_[k]['substate'] == 'In Queue':
            print(Style.BRIGHT, end='')
            print(Fore.CYAN + AuditDictionary_[k]['state'].center(9), end="")
            print(Fore.RESET + ' | ', end='')
            print(Fore.CYAN + AuditDictionary_[k]['substate'][:25].center(25))
            print(Fore.RESET, end='')
            if toggle:
                print(Style.BRIGHT, end="")
            else:
                print(Style.RESET_ALL, end="")
        
        elif AuditDictionary_[k]['state'] == 'On Hold':
            print(Style.BRIGHT, end='')
            print(Fore.MAGENTA + AuditDictionary_[k]['state'].center(9), end="")
            print(Fore.RESET + ' | ', end='')
            print(Fore.MAGENTA + AuditDictionary_[k]['substate'][:25].center(25))
            print(Fore.RESET, end='')
            if toggle:
                print(Style.BRIGHT, end="")
            else:
                print(Style.RESET_ALL, end="")
        
        elif AuditDictionary_[k]['state'] == 'Working':
            print(Style.BRIGHT, end='')
            print(AuditDictionary_[k]['state'].center(9), end="")
            print(' | ', end='')
            print(AuditDictionary_[k]['substate'][:25].center(25))
            if toggle:
                print(Style.BRIGHT, end="")
            else:
                print(Style.RESET_ALL, end="")
        
        elif AuditDictionary_[k]['state'] == 'NULL':
            print(Style.BRIGHT, end='')
            print(Fore.RED + AuditDictionary_[k]['state'].center(9), end="")
            print(Fore.RESET + ' | ', end='')
            print(Fore.RED + AuditDictionary_[k]['substate'][:25].center(25))
            print(Fore.RESET, end='')
            if toggle:
                print(Style.BRIGHT, end="")
            else:
                print(Style.RESET_ALL, end="")
        
        else:
            print(AuditDictionary_[k]['state'].center(9), end="")
            print(' | ', end='')
            print(AuditDictionary_[k]['substate'][:25].center(25))
    
    print(Style.RESET_ALL, end='')



def auditConsole(AuditDictionary_, AuditList_, GoodScannedList_, WronglyScannedList_):

    subList = AuditList_
    while True:
        _toolsHandler.header()
                
        if AuditDictionary_ != {}:
            printer(AuditDictionary_, subList)
            print(Fore.RED + Style.BRIGHT + ' ' + format(len(subList) + 1).center(3) + ' | ' +  'END PROGRAM'.center(11))
            print(Style.RESET_ALL, end="")
            _toolsHandler.line()
            print('  Enter a CS Number or the Number of the item')
        else:
            for i,each in enumerate(subList):
                print(' ' + format(i + 1)[:3].center(3), end='')
                print(' | ', end='')
                print(each)
            print(Fore.RED + Style.BRIGHT + ' ' + format(len(AuditList_) + 1).center(3) + ' | ' + 'END PROGRAM' + Style.RESET_ALL)

        userInput = input('  > ')
                
        try:
            userInput = int(userInput)
            if userInput == len(subList) + 1:
                return subList
            userInput -= 1
            if len(subList) < userInput:
                continue
            if userInput < 0:
                continue
            GoodScannedList_.append(subList[userInput])
            subList.remove(subList[userInput])
        except:
            userInput = userInput.strip()
            userInput = userInput.upper()
            try:
                subList.remove(userInput)
                GoodScannedList_.append(userInput)
                print('\a')
            except:
                if userInput not in AuditList_:
                    if userInput not in WronglyScannedList_:
                        WronglyScannedList_.append(userInput)



def gatherer(serviceNow, Dictionary_, List_, totalTicketNumber_, sys_userTable, u_computer_supportTable):

        for i,each in enumerate(List_):
                _toolsHandler.header()
                print('    GATHERING INFORMATION')
                print('       ' + format(i) + ' / ' + format(totalTicketNumber_))
                try: 
                        username, state, substate = getDetails(each, serviceNow, u_computer_supportTable, sys_userTable)
                        Dictionary_[each] = {}
                        Dictionary_[each]['username'] = username
                        Dictionary_[each]['state'] = state
                        Dictionary_[each]['substate'] = substate
                        Dictionary_[each]['ticket'] = each
                except:
                        Dictionary_[each] = {}
                        Dictionary_[each]['username'] = 'NULL'
                        Dictionary_[each]['state'] = 'NULL'
                        Dictionary_[each]['substate'] = 'NULL'
                        Dictionary_[each]['ticket'] = each      
        _toolsHandler.header()



def QueryGen(auditChoice, u_depot_location, u_location, serviceNow):
        temporaryList = []
        if auditChoice == 0:
                qb = (
                        pysnow.QueryBuilder()
                        .field('number').starts_with('CS')
                        .AND()
                        .field('cat_item').contains('Repair')
                        .AND()
                        .field('u_depot_location').equals(u_depot_location)
                        .OR()
                        .field('location').contains(u_location)
                        .AND()
                        .field('state').equals(['1','2','11'])
                        .OR()
                        .field('u_substate').equals(['Ready for pickup', 'c4b3f3702b3c9200258f89efe8da1504'])
                )
                incident = serviceNow.resource(api_path='/table/u_computer_support')
                response = incident.get(query=qb)
                temptotal = 0
                for record in response.all():
                        temporaryList.append(record['number'])
        elif auditChoice == 1:
                qb = (
                        pysnow.QueryBuilder()
                        .field('number').starts_with('CS')
                        .AND()
                        .field('cat_item').contains('Assignment')
                        .AND()
                        .field('u_depot_location').equals(u_depot_location)
                        .OR()
                        .field('location').contains(u_location)
                        .AND()
                        .field('state').equals(['1','2','11'])
                        .OR()
                        .field('u_substate').equals(['Ready for pickup', 'c4b3f3702b3c9200258f89efe8da1504'])
                )
                incident = serviceNow.resource(api_path='/table/u_computer_support')
                response = incident.get(query=qb)
                temptotal = 0
                for record in response.all():
                        temporaryList.append(record['number'])
        else:
                while True:     #loop while person is idiot and does not copy their list properly
                        _toolsHandler.header()                                                        
                        print('  I cannot automatically gather that audit, please export')                      
                        print('  the audit as a .xlsx, then copy the items from the sheet')     
                        wait('  then press any key.     >> DO NOT PASTE THE LIST << \n')
                        try:
                                if platform.system() == 'Windows': #to split the list into useable CS# / Serial#
                                        temporaryList = pyperclip.paste().split()
                                else:
                                        temporaryList = pyperclip.paste().split()
                        except:
                                print('  I cannot get your clipboard. Paste it to a txt file, and remove newlines')
                                temporaryList = input('  Try pasting it here: ').split()
                        _toolsHandler.header()
                        for i,item in enumerate(temporaryList): #to format list as: '[x] item' where x is a numbered list
                                temporaryList[i] = item.upper()
                                print('[' + format(i + 1) + '] ' + item)

                        checkBool = wait('Is this correct? [y/n]: ')
                        if (checkBool is 'y') or (checkBool is 'Y'):
                                break;

        temporaryList.sort()
        return temporaryList, len(temporaryList)



def auditSetup():
        auditMenu = []
        auditMenu = ['Daily Repair Audit', 'Weekly Assignment Audit', 'Weekly Storage Audit', 'Weekly Loaner Audit']
        auditChoice = _toolsHandler.PR_('Which audit are you running?', auditMenu)

        locationMenu = ['Demoss Hall', 'Green Hall', 'LUCOM', 'River Ridge']
        locationChoice = _toolsHandler.PR_('Which Office are you located?', locationMenu)

        if locationChoice == 0:
                u_depot_location = '862a49f29c806d40f47c19537d850ca4'
                u_location = 'DH 2414'
        
        elif locationChoice == 1:
                u_depot_location = 'b37c34a019e0d5405af136ec3a0d0ef3'
                u_location = 'GH 1539'
        
        elif locationChoice == 2:
                u_depot_location = '1db6a5ff353fd1405af1cb6de5727f34'
                u_location = 'CMHS 3122A'

        elif locationChoice == 3:
                u_depot_location = '59ac3ca019e0d5405af136ec3a0d0e4c'
                u_location = 'RRA 171'

        return auditChoice, u_depot_location, u_location





def getUsername(sysID, serviceNow, sys_userTable):
        if sysID == 'NULL':
                return ''
        sys_user = sys_userTable.get(query={'sys_id':sysID}, fields=['name'])
        user_fullName = sys_user.one()[u'name']
        return user_fullName



def getTicketState(stateNumber):
        if stateNumber == '1':
                state_name = 'Open'
        elif stateNumber == '2':
                state_name = 'Working'
        elif stateNumber == '3':
                state_name = 'Closed'
        elif stateNumber == '7':
                state_name = 'Cancelled'
        elif stateNumber == '11':
                state_name = 'On Hold'
        else:
                state_name = 'Unknown'          
        return state_name



def getTicketSubState(substateNumber):
        try:
                substateNumber = substateNumber['value']
        except:
                substate_name = ''
                return substate_name

        if substateNumber == '':
                substate_name = ''
        #WIP
        elif substateNumber == '5747a37c2bf89200258f89efe8da1585':
                substate_name = 'External Repair Location'
        elif substateNumber == '258140052b3c9200258f89efe8da15df':
                substate_name = 'Customer Contacted'
        elif substateNumber == 'd671c4052b3c9200258f89efe8da1542':
                substate_name = 'Delivered'
        elif substateNumber == 'f94148052b3c9200258f89efe8da15c3':
                substate_name = 'Inventory Recieved'
        elif substateNumber == 'b3437f302b3c9200258f89efe8da15ac':
                substate_name = 'Laptop Recieved'
        elif substateNumber == '3a62f7302b3c9200258f89efe8da1545':
                substate_name = 'Waiting for hardware'
        #Closed
        elif substateNumber == 'ed6abde42bf426001235717bf8da15b9':
                substate_name = 'Pending Transfer'
        elif substateNumber == 'c4b3f3702b3c9200258f89efe8da1504':
                substate_name = 'Ready for Pickup'
        #Open
        elif substateNumber == '489fb3f02b3c9200258f89efe8da156d':
                substate_name = 'In Queue'
        #On Hold
        elif substateNumber == '3a62f7302b3c9200258f89efe8da1545':
                substate_name = 'Waiting for Hardware'
        elif substateNumber == '99a40c452b3c9200258f89efe8da159b':
                substate_name = 'Waiting on Customer'
        elif substateNumber == 'cb467ce92bf0d200258f89efe8da157f':
                substate_name = 'Waiting on Non-IT Resource'
        elif substateNumber == 'a83877b02b3c9200258f89efe8da15b7':
                substate_name = 'Waiting to Reformat'
        #Cancelled

        #else
        else:
                substate_name = 'Unknown'
        return substate_name



def getDetails(ticketNumber, serviceNow, table, usertable):
        ticket = table.get(query={'number':ticketNumber}, fields=['assigned_to', 'state', 'u_substate'])
        ticket_allInformation = ticket.all()
        for ticket_allInformationIterable in ticket_allInformation:
                try:
                        ticket_assigned_to_sysID = ticket_allInformationIterable[u'assigned_to'][u'value']
                        #print('good1')
                except:
                        ticket_assigned_to_sysID = 'NULL'
                try:
                        ticket_state =  ticket_allInformationIterable[u'state']
                        #print('good2')
                except:
                        ticket_state = 'NULL'
                try:
                        ticket_u_substate = ticket_allInformationIterable['u_substate']
                        #print('good3')
                except:
                        ticket_u_substate = 'NULL'
        #try:
        assigned_to = getUsername(ticket_assigned_to_sysID, serviceNow, usertable)
        #       print('this worked')
        #except:
        #       return '', '', ''
        
        state = getTicketState(ticket_state)
        substate = getTicketSubState(ticket_u_substate)

        #print(assigned_to + ' ' + state + ' ' + substate + '<<')
        #wait()
        return assigned_to, state, substate









#------------------------------------------------
# For functionality of Python
if __name__ == '__main__':
        import traceback
        try:
                main()
        except Exception as inst:
                _toolsHandler.clear()
                print("    Unexpected Error!")
                print('    -----------------')
                print("   Version: ", _glob.version[0], _glob.version[1], _glob.version[2], _glob.version[3])
                print("    -----------------")
                print(" BEGINNING ERROR REPORT:")
                print(" -----------------------")
                print(" -----------------------")
                print(" Primary Error: ", inst)
                print(" -----------------------")
                traceback.print_exc()
                print(" -----------------------")
                print(" Please go to the following to create a bug report:")
                print(" https://goo.gl/forms/oEeldwsAW98gwAEm1")
                input('\n\n  Press Enter to close!')

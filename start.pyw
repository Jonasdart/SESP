#encoding utf-8

#__author__ = Jonas Duarte, duarte.jsystem@gmail.com
#Python3
__author__ = 'Jonas Duarte'

from model import Backend
import os
import subprocess

import PySimpleGUIQt as sg





class Controller():
    def __init__(self):
        self.model = Backend()
    

    def start(self):
        try:
            computer_info = self.model.get_data.get_computer()
            #self.model.alter_date_time(self.model.get_data.get_date_time())
            #response = self.model.rename_computer(computer_inventorynumber)
            #response = self.model.force_inventory()
            tray = sg.SystemTray(filename=r'ico.ico')
            os.system('python schedule.pyw')
        except Exception as e:
            raise e
        
        #return response


if __name__ == "__main__":
    try:
        Controller().start()
    except Exception as e:
        raise e

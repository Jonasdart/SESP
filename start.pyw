#encoding utf-8

#__author__ = Jonas Duarte, duarte.jsystem@gmail.com
#Python3
__author__ = 'Jonas Duarte'

from model import Backend
from schedule import Schedule
from Atualizacoes.install import Update
import os
import subprocess


class Controller():
    def __init__(self):
        self.model = Backend()
    

    def start(self):
        try:
            computer_info = self.model.get_data.get_computer()
            #self.model.alter_date_time(self.model.get_data.get_date_time())
            #response = self.model.rename_computer(computer_inventorynumber)
            #response = self.model.force_inventory()
            #os.system('python schedule.pyw')
            Update().start()
            Schedule().start()
        except Exception as e:
            raise e
        
        #return response


if __name__ == "__main__":
    try:
        Controller().start()
    except Exception as e:
        raise e

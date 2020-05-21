import configparser
import subprocess
import requests
import json
from platform import node
from os import system


class Backend():
    def __init__(self):
        self.base_url = self.get_api_server()

    def teste(self):
        try:
            computer_info = self.get_computer()

            self.base_url = self.get_api_server()

            inventory_number = computer_info['InventoryNumber']
            self.rename_computer(inventory_number)
        except Exception as e:
            print(e)


    def get_api_server(self):
        config = configparser.ConfigParser()
        config.read('conf.cfg')

        base_url = config.get('config_api', 'base_url')

        return base_url

    def get_computer(self):
        config = configparser.ConfigParser()
        config.read('computer.cfg')

        inventory_number = config.get('computer', 'inventory_number')
        proxy_active = config.get('computer', 'proxy_active')
        proxy_server = config.get('computer', 'proxy_server')
        proxy_excessions = config.get('computer', 'proxy_excessions')


        if inventory_number == '':
            inventory_number = input('Informe a etiqueta do computador: ')

        return {
            'InventoryNumber' : inventory_number,
            'ProxyActive' : proxy_active,
            'ProxyServer' : proxy_server,
            'ProxyExcessions' : proxy_excessions
        }


    def get_computer_from_server(self, inventory_number):
        url = self.base_url+'/get_computer'

        data = json.dumps({
            "InventoryNumber" : inventory_number,
            "Database" : "GLPI"
        })

        requests.post(url=url, json=data)


    def force_four_digits(self, inventory_number):
        number_of_zeros = 4 - len(inventory_number)
        inventory_number = '0'*number_of_zeros + inventory_number

        return inventory_number

    
    def rename_computer(self, inventory_number):
        new_name = 'HAT'+self.force_four_digits(inventory_number)
        old_name = node()

        system(f'wmic computersystem where name="{old_name}" rename "{new_name}"')

        reiniciar = input('Reiniciar agora?(S/n): ').upper()
        if reiniciar == 'S':
            subprocess.run(['shutdown', '-r', '-t', '1'])

'''
if __name__ == "__main__":
    Backend()
'''
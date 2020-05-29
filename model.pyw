import configparser
import subprocess
import requests
import json
from platform import node
from os import system


class GetInfo():
    def __init__(self):
        self.base_url = self.get_api_server()


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
            config.set('computer', 'inventory_number', inventory_number)

            with open('computer.cfg', 'w') as cfg:
                config.write(cfg)

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

        response = requests.post(url=url, json=data)
        response_json = json.loads(response.content.decode())

        if response.status_code >= 400:
            raise Exception(response_json['Message']['Error'])

        return response_json


    def get_date_time(self):
        url = self.base_url+'/get_date_time'
        
        response = requests.get(url)
        response_json = json.loads(response.content.decode())
        
        if response.status_code >= 400:
            raise Exception(response_json['Message']['Error'])

        return response_json


class Backend():
    def __init__(self):
        self.get_data = GetInfo()
        computer_info = self.get_data.get_computer()
        inventory_number = computer_info['InventoryNumber']
        
        self.alter_date_time(self.get_data.get_date_time())
        
        computer_data = self.get_data.get_computer_from_server(inventory_number)
        self.rename_computer(computer_data)


    def force_four_digits(self, inventory_number):
        number_of_zeros = 4 - len(inventory_number)
        inventory_number = '0'*number_of_zeros + inventory_number

        return inventory_number

    
    def rename_computer(self, data):
        try:
            computer_name = data['Message']['1']['Name']
        except:
            raise Exception('Return incorrect')

        new_name = computer_name
        old_name = node()

        if old_name != new_name:
            alterar = input(f'Deseja alterar o nome do computador para "{new_name}" ?(S/n): ').upper()
            if alterar == 'S':
                system(f'wmic computersystem where name="{old_name}" rename "{new_name}"')
                reiniciar = input('Reiniciar agora?(S/n): ').upper()
                if reiniciar == 'S':
                    subprocess.run(['shutdown', '-r', '-t', '1'])
        else:
            print('Name is already the same as the glpi')

    
    def alter_date_time(self, data):
        print(data)

        date = data['Date']
        time = data['Time']
        
        print(date, time)

        system(f'date {date}')
        system(f'time {time}')

        return True


if __name__ == "__main__":
    try:
        Backend()
    except Exception as e:
        print(e)
        system('pause')

import configparser
import subprocess
import requests
import json as Json
from platform import node
from os import system


class GetInfo():
    def __init__(self):
        self.base_url = self.get_api_server()
        self.headers = {
            'inventory_number' : None,
            'computer_name'    : node(),
            'sesp_version'     : None
        }

    
    def get_dict_from_json(self, json):
        try:
            json = Json.loads(json)
        except Exception as e:
            raise e

        return json


    def get_json_from_dict(self, data):
        try:
            json = Json.dumps(data)
        except Exception as e:
            raise e

        return json

    
    def get_sesp_version(self):
        try:
            config = configparser.ConfigParser()
            config.read('conf.cfg')

            sesp_version = config.get('current_version', 'version')

            self.headers['sesp_version'] = sesp_version
        except Exception as e:
            raise e

        return sesp_version


    def get_api_server(self):
        try:
            config = configparser.ConfigParser()
            config.read('conf.cfg')

            base_url = config.get('config_api', 'base_url')
        except Exception as e:
            raise e

        return base_url


    def get_computer(self):
        try:
            config = configparser.ConfigParser()
            config.read('computer.cfg')

            computer_inventorynumber = config.get('computer', 'inventory_number')
            proxy_active = config.get('computer', 'proxy_active')
            proxy_server = config.get('computer', 'proxy_server')
            proxy_excessions = config.get('computer', 'proxy_excessions')

            if computer_inventorynumber == '':
                computer_inventorynumber = self.get_glpi_inventory_number_by_name()
                config.set('computer', 'inventory_number', computer_inventorynumber)
                with open('computer.cfg', 'w') as cfg:
                    config.write(cfg)

            self.headers['inventory_number'] = computer_inventorynumber

        except Exception as e:
            raise e

        return {
            'InventoryNumber' : computer_inventorynumber,
            'ProxyActive' : proxy_active,
            'ProxyServer' : proxy_server,
            'ProxyExcessions' : proxy_excessions
        }

    
    def get_glpi_inventory_number_by_name(self):
        try:
            print('\nSearching for a inventory number from GLPI, using the name of this computer...')
            base_url = self.get_api_server()
            url_request = base_url+'/computers/byname?name='+node()
            response = requests.get(url_request, headers=self.headers)

            if response.status_code == 200:
                response = self.get_dict_from_json(response.content.decode())
                computer_id = None
                count=0
                for _computer in response.values():
                    if computer_id != _computer['computer_id']:
                        computer_id = _computer['computer_id']
                        computer_inventorynumber = _computer['computer_inventorynumber']
                        count += 1
                if count < 1:
                    raise('The name of this computer does not appear in the GLPI. Thus, it was not possible to find the inventory number of the same.')
                elif count > 1:
                    raise('The name of this computer appears on more than one computer in the GLPI. Thus, it was not possible to find the inventory number of the same.')
            
                print(f'\nComputer inventory number: {computer_inventorynumber}')
                
            elif response.status_code == 404:
                raise('The name of this computer does not appear in the GLPI. Thus, it was not possible to find the inventory number of the same.')
            else:
                raise('Internal server error as occurred or the api server is not started. Please verificate.')
        except Exception as e:
            raise e
        
        
        return computer_inventorynumber


    def get_glpicomputer(self, computer_inventorynumber):
        try:
            print(f'\nSearching info of this computer in GLPI...')
            url = self.base_url+'/computers/byinventory?number='+computer_inventorynumber
            response = requests.get(url, headers=self.headers)
            
            if response.status_code >= 400:
                raise Exception(response.text)
            
            response = self.get_dict_from_json(response.content.decode())
            
        except Exception as e:
            raise e

        return response


    def get_date_time(self):
        try:
            url = self.base_url+'/get_date_time'
            
            response = requests.get(url, headers=self.headers)
            response_json = self.get_dict_from_json(response.content.decode())
            
            if response.status_code >= 400:
                raise Exception(response_json['Message']['Error'])
        except Exception as e:
            raise e

        return response_json


class Backend():
    def __init__(self):
        self.get_data = GetInfo()
        

    def alter_date_time(self, data):
        try:
            print(data)

            date = data['Date']
            time = data['Time']
            
            print(date, time)

            system(f'date {date}')
            system(f'time {time}')

        except Exception as e:
            raise e

        return True

    
    def rename_computer(self, computer_inventorynumber, rename_in_glpi=False):
        try:
            old_name = node()
            computer_info = self.get_data.get_glpicomputer(computer_inventorynumber)
            new_name = computer_info["1"]['computer_name']

            url = self.get_data.base_url+'/computers/byinventory'
            request = {
                "inventory_number": computer_inventorynumber,
                "change_name": 0,
                "force_inventory": 0,
                "schedule_reboot":0,
                "schedule_shutdown":0
            }
            
            if rename_in_glpi:
                new_name = 'HAT'+computer_inventorynumber
                request['change_name'] = new_name
                
            response = requests.put(url, json=request, headers=self.headers)
            if response.status_code != 200:
                raise Exception(response.text)

            if old_name != new_name:
                print(f'\nAplying changes from GLPI in this computer...')
                print(f'\nOld name = {old_name} | New name = {new_name}')
                system(f'wmic computersystem where name="{old_name}" rename "{new_name}"')
                subprocess.run(['shutdown', '-r', '-t', '60'])
                return response.text, True

            self.headers['computer_name'] = new_name
        except Exception as e:
            raise e
        
        return response.text, False


    def force_inventory(self, computer_inventorynumber):
        try:
            if not self.rename_computer(computer_inventorynumber)[1]:
                print(f'\nRequesting new inventory from FusionInventory...')
                url = self.get_data.base_url+'/computers/byinventory'
                request = {
                    "inventory_number": computer_inventorynumber,
                    "change_name": 0,
                    "force_inventory": 1,
                    "schedule_reboot":0,
                    "schedule_shutdown":0
                }
                response = requests.put(url, json=request, headers=self.headers)
                if response.status_code != 200:
                    raise Exception(response.text)
            else:
                raise('A reboot is necessary to apply changes from GLPI to this computer')
        except Exception as e:
            raise e

        return response        


    def force_four_digits(self, inventory_number):
        try:
            number_of_zeros = 4 - len(inventory_number)
            inventory_number = '0'*number_of_zeros + inventory_number
        except Exception as e:
            raise e

        return inventory_number


class Controller():
    def __init__(self):
        self.model = Backend()
    

    def start(self):
        try:
            computer_info = self.model.get_data.get_computer()
            computer_inventorynumber = computer_info['InventoryNumber']
            #self.model.alter_date_time(self.model.get_data.get_date_time())
            #response = self.model.rename_computer(computer_inventorynumber)
            response = self.model.force_inventory(computer_inventorynumber)
        except Exception as e:
            raise e
        
        return response


if __name__ == "__main__":
    try:
        Controller().start()
    except Exception as e:
        raise e

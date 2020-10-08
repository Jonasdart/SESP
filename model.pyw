#encoding utf-8

#__author__ = Jonas Duarte, duarte.jsystem@gmail.com
#Python3
__author__ = 'Jonas Duarte'


from pathlib import Path
import configparser
import requests
import json as Json
from platform import node
from exceptions import ComputerNameOutOfDefaults
from Atualizacoes.install import Installer

import win32con
from win32com.shell.shell import ShellExecuteEx


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
            config.read('C:\\SESP\\conf.cfg')

            sesp_version = config.get('current_version', 'version')

            self.headers['sesp_version'] = sesp_version
        except Exception as e:
            raise e

        return sesp_version


    def get_api_server(self):
        try:
            config = configparser.ConfigParser()
            config.read('C:\\SESP\\conf.cfg')

            base_url = config.get('config_api', 'base_url')
        except Exception as e:
            raise e

        return base_url


    def get_check_frequency_of_schedule(self):
        try:
            config = configparser.ConfigParser()
            config.read('C:\\SESP\\conf.cfg')

            check_frequency = config.get('schedule', 'check_frequency')
        except Exception as e:
            raise e

        return int(check_frequency)


    def get_computer(self):
        try:
            config = configparser.ConfigParser()
            config.read('C:\\SESP\\computer.cfg')

            computer_inventorynumber = config.get('computer', 'inventory_number')
            proxy_active = config.get('computer', 'proxy_active')
            proxy_server = config.get('computer', 'proxy_server')
            proxy_excessions = config.get('computer', 'proxy_excessions')

            if computer_inventorynumber == '':
                #computer_inventorynumber = self.get_glpi_inventory_number_by_name()
                computer_inventorynumber = self.get_glpi_inventory_number_by_node()
                config.set('computer', 'inventory_number', computer_inventorynumber)
                with open('C:\\SESP\\computer.cfg', 'w') as cfg:
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
            
                
            elif response.status_code == 404:
                raise('The name of this computer does not appear in the GLPI. Thus, it was not possible to find the inventory number of the same.')
            else:
                raise('Internal server error as occurred or the api server is not started. Please verificate.')
        except Exception as e:
            raise e
        
        
        return computer_inventorynumber

    
    def get_glpi_inventory_number_by_node(self):
        try:
            name = node()
            computer_inventorynumber = name.split('HAT')

            if len(computer_inventorynumber) == 2 and len(computer_inventorynumber[1]) == 4:
                computer_inventorynumber = computer_inventorynumber[1]
            else:
                raise ComputerNameOutOfDefaults

        except Exception as e:
            raise e
        
        
        return computer_inventorynumber


    def get_sesp_computer(self):
        try:
            computer_inventorynumber = self.headers['inventory_number']
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


    def fusion_install(self):
        try:
            Installer().fusion_install()

            url = self.get_data.base_url+'/computers/byinventory?status=6'
            requests.patch(url, headers=self.get_data.headers)

        except:
            raise
        

    def alter_date_time(self, data):
        try:

            date = data['Date']
            time = data['Time']
            
            ShellExecuteEx(lpFile=f'date {date}', nShow=win32con.SW_HIDE)
            ShellExecuteEx(lpFile=f'time {time}', nShow=win32con.SW_HIDE)

        except Exception as e:
            raise e

        return True

    
    def rename_computer(self, rename_in_glpi=False):
        try:
            computer_inventorynumber = self.get_data.headers['inventory_number']
            old_name = node()
            glpi_info = self.get_data.get_sesp_computer()['glpi']
            new_name = glpi_info["1"]['computer_name']

            url = self.get_data.base_url+'/computers/byinventory'
            request = {
                "change_name": 0,
                "force_inventory": 0,
                "schedule_reboot":0,
                "schedule_shutdown":0
            }
            
            if rename_in_glpi:
                new_name = 'HAT'+computer_inventorynumber
                request['change_name'] = new_name
                
            response = requests.put(url, json=request, headers=self.get_data.headers)
            if response.status_code != 200:
                raise Exception(response.text)

            if old_name != new_name:
                ShellExecuteEx(lpFile=f'wmic computersystem where name="{old_name}" rename "{new_name}"', nShow=win32con.SW_HIDE)
                return response.text, True

            self.get_data.headers['computer_name'] = new_name
        except Exception as e:
            raise e
        
        return response.text, False


    def force_inventory(self, api=False):
        try:
            if not self.rename_computer()[1]:
                if api:
                    url = self.get_data.base_url+'/computers/byinventory'
                    request = {
                        "change_name": 0,
                        "force_inventory": 1,
                        "schedule_reboot":0,
                        "schedule_shutdown":0
                    }
                    response = requests.put(url, json=request, headers=self.get_data.headers)
                    if response.status_code != 200:
                        raise Exception(response.text)
                else:
                    path = Path('C:\\Program Files (x86)\\FusionInventory-Agent')
                    
                    if not path.is_dir():
                        path = Path('C:\\Program Files\\FusionInventory-Agent')
                    try:

                        path = Path('C:\\Program Files (x86)\\FusionInventory-Agent')       
                        if not path.is_dir():
                            path = Path(')

                        ShellExecuteEx(lpFile='C:\\FusionInventory-Agent\\fusioninventory-agent.bat', nShow=win32con.SW_HIDE)

                    except Exception as e:
                        print(e)
                        url = self.get_data.base_url+'/computers/byinventory?status=2'
                        response = requests.patch(url, headers=self.get_data.headers)
                        if response.status_code != 200:
                            raise Exception(response.text)
                    else:
                        url = self.get_data.base_url+'/computers/byinventory?status=7&fusion_executed=True'
                        response = requests.patch(url, headers=self.get_data.headers)
                        
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


    def reboot(self):
        try:
            ShellExecuteEx(lpFile='shutdown -r -t 60', nShow=win32con.SW_HIDE)
        except Exception as e:
            raise e


    def shutdown(self):
        try:
            ShellExecuteEx(lpFile='shutdown -s -t 60', nShow=win32con.SW_HIDE)
        except Exception as e:
            raise e
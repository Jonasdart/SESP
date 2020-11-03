#encoding utf-8

#__author__ = Jonas Duarte, duarte.jsystem@gmail.com
#Python3
__author__ = 'Jonas Duarte'

from exceptions import VersionError, ComputerNameOutOfDefaults

from model import GetInfo, Backend
from datetime import datetime
import time
import requests
import PySimpleGUIQt as sg
from PySimpleGUI import SystemTray


class Schedule():
    def __init__(self):
        self.model = Backend()
        try:
            tray = sg.SystemTray(filename='C:\\SESP\\icone_sesp.ico', tooltip='SESP')
        except: pass
        

    def _fusion_inventory_check(self, computer):
        try:
            if computer['next_fusion_inventory'] is None:
                self.model.force_inventory(api=False)
            else:
                next_fusion_inventory = datetime.strptime(computer['next_fusion_inventory'], '%Y-%m-%d %H:%M')
                if next_fusion_inventory <= datetime.now():
                    self.model.force_inventory(api=False)
        except Exception as e:
            pass


    def _reboot_check(self, computer):
        try:
            next_reboot = datetime.strptime(computer['next_reboot'], '%Y-%m-%d %H:%M')
            if next_reboot <= datetime.now():
                self.model.reboot()
        except Exception as e:
            pass


    def _shutdown_check(self, computer):
        try:
            next_shutdown = datetime.strptime(computer['next_shutdown'], '%Y-%m-%d %H:%M')
            if next_shutdown <= datetime.now():
                self.model.shutdown()
        except Exception as e:
            pass

    
    def _fusion_inventory_install(self, computer):
        try:
            self.model.fusion_install()
            self._fusion_inventory_check(computer)
        except Exception as e:
            pass

        
    def _wallpaper_refresh(self, computer):
        try:
            wallpaper_path = computer['wallpaper']
            if wallpaper_path is None or wallpaper_path == 'default':
                wallpaper_path = '\\\\192.168.1.221\\sesp_files\\wallpapers\\default'
            
            self.model.update_wallpaper(wallpaper_path)
        except Exception as e:
            pass


    def start(self):
        try:
            while True:
                check_frequency = GetInfo().get_check_frequency_of_schedule()

                self._wallpaper_refresh({
                    'wallpaper' : 'default'
                })

                try:
                    self.model.get_data.get_computer()
                    computer = self.model.get_data.get_sesp_computer()['sesp']['1']
                except VersionError:
                    self.model.sesp_updater()
                    break
                else:
                    self._wallpaper_refresh(computer)

                if self.model.rename_computer()[1]:
                    title = 'Reinicie o computador'
                    body = 'O SESP alterou o nome do seu computador, com base no GLPI. Reinicie o computador, assim que possível.'
                    try:
                        SystemTray().notify(title, body)
                    except: pass
                else:
                    if computer['status_id'] == 2:
                        self._fusion_inventory_install(computer)
                    else:
                        self._fusion_inventory_check(computer)
                self._reboot_check(computer)
                self._shutdown_check(computer)

                time.sleep(check_frequency)
        except Exception as e:
            if e is ComputerNameOutOfDefaults:
                title = 'Erro'
                body = str(e)
                try:
                    SystemTray().notify(title, body)
                except: pass

                check_frequency = 3600

            elif 'Failed to establish a new connection' in str(e):
                check_frequency = 5
                
            else:
                check_frequency = 5

            time.sleep(check_frequency)
            self.start()
        else:
            return 'Finish'


if __name__ == "__main__":
    try:
        Schedule().start()
    except Exception as e:
        raise e

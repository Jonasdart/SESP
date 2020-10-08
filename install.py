from pathlib import Path
import configparser
import platform
import subprocess
import sys
import shutil
import time
import os
from PySimpleGUI import SystemTray
import win32com.client


class Computer():
    def __init__(self):
        self.path_of_installer_is_created=False


    def get_computer_platform(self):
        so = platform.platform()
        arch = platform.architecture()
        name = platform.node()

        return [so, arch, name]


    def create_path_of_installers(self):
        try:
            #os.system('net use W: /delete >nul')
            #os.system('net use W: \\\\192.168.0.2\\d\\TI /user:192.168.0.2\\Administrador h13a14T10x')
            response = subprocess.run(["mkdir", "C:\\installers"], shell=True)

        except Exception as e:
            raise e

        self.path_of_installer_is_created = True
        return True


    def exclude_path_of_installers(self):
        try:
            shutil.rmtree('C:\\installers')
            #os.system('net use W: /delete >nul')
        except Exception as e:
            raise e
        
        self.path_of_installer_is_created = False
        return True

    
    def get_fusion_server(self):
        try:
            config = configparser.ConfigParser()
            config.read('C:\\SESP\\conf.cfg')

            fusion_server = config.get('fusion', 'server')

        except Exception as e:
            raise e
        
        return fusion_server


class Installer():
    def __init__(self):
        self.computer_controller = Computer()


    def python_install(self):
        try:
            if not self.computer_controller.path_of_installer_is_created:
                self.computer_controller.create_path_of_installers()
            so, arch, name = Computer().get_computer_platform()
            if '64' in arch:
                path_installer = "W:\\Programas\\Programação, Imagem e Video\\Python\\Python64.exe"
            else:
                path_installer = "W:\\Programas\\Programação, Imagem e Video\\Python\\Python32.exe"
            subprocess.run(["copy", path_installer, "C:\\installers\\Python.exe"], shell=True)

            os.system('start C:\\installers\\Python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0')
        
        except Exception as e:
            raise e
        return True

    
    def install_dependencies(self):
        try:
            with open('C:\\SESP\\Atualizacoes\\requirements.bat', 'w') as bat:
                script = """
                    set HTTP_PROXY=http://sesp:Ne2715hat@192.168.0.1:8080
                    set HTTP_PROXY=https://sesp:Ne2715hat@192.168.0.1:8080
                    pip install -r C:\\SESP\\Atualizacoes\\requirements.txt
                """
                bat.write(script)
            os.system('C:\\SESP\\Atualizacoes\\requirements.bat')
        except Exception as e:
            raise e

        return True

    
    def git_install(self):
        try:
            while True:
                try:
                    self.computer_controller.exclude_path_of_installers()
                except:
                    time.sleep(2)
                else:
                    break
                    
            if not self.computer_controller.path_of_installer_is_created:
                self.computer_controller.create_path_of_installers()
            so, arch, name = Computer().get_computer_platform()
            if '64' in arch:
                path_installer = "W:\\Programas\\Programação, Imagem e Video\\Git\\Git64.exe"
            else:
                path_installer = "W:\\Programas\\Programação, Imagem e Video\\Git\\Git32.exe"

            response = subprocess.run(["copy", path_installer, "C:\\installers\\Git.exe"], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível copiar o git para a máquina')

            os.system('start C:\\installers\\Git.exe /VERYSILENT /SUPPRESSMSGBOXES')

        except Exception as e:
            raise e
        return True


    def sesp_install(self):
        try:
            while True:
                try:
                    self.computer_controller.exclude_path_of_installers()
                except:
                    time.sleep(2)
                else:
                    break
                
            self.title = 'Instalando o SESP'
            self.body = ''
            SystemTray().notify(self.title, self.body)

            response = subprocess.run(["mkdir", "C:\\.SESP"], shell=True)

            git_path = Path('C:\Program Files (x86)\Git\cmd')
            if not git_path.is_dir():
                git_path = Path('C:\Program Files\Git\cmd')

            with open('C:\\.SESP\\Sesp.bat', 'w') as bat: 
                script = f"""
                cd {git_path}
                git config --global http.proxy http://sesp:Ne2715hat@192.168.0.1:8080
                git config --global https.proxy https://sesp:Ne2715hat@192.168.0.1:8080
                git clone https://github.com/jonasdart/SESP.git C:\\SESP
                git clone -b master_version https://github.com/jonasdart/SESP.git C:\\SESP\\Atualizacoes
                """
                bat.write(script)
            
            subprocess.run(['C:\\.SESP\\Sesp.bat'], shell=True)
            
            self.create_link_to_startup()
            
        except Exception as e:
            raise e
        return True


    def create_link_to_startup(self):
        desktop = "C:\\Users\\Administrador\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        path = os.path.join(desktop, "SESP.lnk")
        target = "C:\\SESP\\start.pyw"
        icon = "C:\\SESP\\icone_sesp.ico" # not needed, but nice

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.IconLocation = icon
        shortcut.WindowStyle = 7 
        shortcut.save()


    def fusion_install(self):
        try:
            self.title = 'Instalando o Fusion Inventory Agent'
            self.body = ''
            SystemTray().notify(self.title, self.body)

            if not self.computer_controller.path_of_installer_is_created:
                self.computer_controller.create_path_of_installers()

            while True:
                try:
                    self.computer_controller.exclude_path_of_installers()
                except:
                    time.sleep(2)
                else:
                    break
                
            if not self.computer_controller.path_of_installer_is_created:
                self.computer_controller.create_path_of_installers()

            so, arch, name = Computer().get_computer_platform()
            if '64' in arch:
                path_installer = "W:\\Programas\\Internet e Rede\\Fusion Inventory\\Fusion64.exe"
            else:
                path_installer = "W:\\Programas\\Internet e Rede\\Fusion Inventory\\Fusion32.exe"
            
            subprocess.run(["copy", path_installer, "C:\\installers\\Fusion.exe"], shell=True)
            
            fusion_server = Computer().get_fusion_server()
            os.system(f'start C:\\installers\\Fusion.exe /S /acceptlicense /add-firewall-exception /execmode=Manual /httpd /httpd-trust="192.168.0.0/23" /server="{fusion_server}"')
            
            path = Path('C:\\Program Files (x86)\\FusionInventory-Agent')       
            if not path.is_dir():
                path = Path('C:\\Program Files\\FusionInventory-Agent')
            os.system(f'cacls {path}\\fusioninventory-inventory.bat /E /P Todos:F')
            
        except Exception as e:
            raise e
        finally:
            while True:
                try:
                    self.computer_controller.exclude_path_of_installers()
                except:
                    time.sleep(2)
                else:
                    break

        return True


class Update():
    def __init__(self):
        self.binds = self.get_binds()


    def start(self):
        version = self.get_version(self.binds)
        need_to_update = self.need_to_update(version)


        if need_to_update['Message'] == True:
            Installer().install_dependencies()
            self.get_archives(self.binds)
            self.save_archives()


    def get_binds(self):
        try:
            conf = configparser.ConfigParser()
            conf.read('C:\\SESP\\Atualizacoes\\conf.cfg')

            remote = conf.get('git_repo', 'remote')
            server = conf.get('git_repo' ,'server')
            branch_version = conf.get('git_repo', 'branch_version')         

            binds = {
                'Remote' : remote,
                'Server' : server,
                'BranchVersion' : branch_version
            }
            self.r = {
                    'Message' : binds
                }
        except Exception as e:
            raise e
        return self.r


    def get_version(self, binds):
        binds = binds['Message']
        try:
            remote = binds['Remote']
            branch_version = binds['BranchVersion']
            print('cd C:\\SESP\\Atualizacoes; git restore .')
            os.system('cd C:\\SESP\\Atualizacoes; git restore .')
            print('cd C:\\SESP\\Atualizacoes; git pull')
            os.system('cd C:\\SESP\\Atualizacoes; git pull')

            conf = configparser.ConfigParser()
            conf.read('C:\\SESP\\Atualizacoes\\conf.cfg')

            current_version = conf.get('current_version', 'version')

            self.r = {
                'Message' : {
                    'CurrentVersion' : current_version
                }
            }
            

            self.title = ''
            self.body = self.r['Message']['CurrentVersion']
            SystemTray().notify(self.title, self.body)

        except Exception as e:
            raise e
        return self.r


    def need_to_update(self, version):
        version = version['Message']
        try:
            #dir_path = os.path.dirname(os.path.realpath(__file__)).split('\Atualizacoes')[0]
            #dir_path = dir_path.replace('\\', '\\\\')
            conf = configparser.ConfigParser()
            conf.read('C:\\SESP\\conf.cfg')

            current_version = conf.get('current_version', 'version')
            if current_version != version['CurrentVersion']:
                self.r = {
                    'Message' : True
                }
            
        except Exception as e:
            raise e
        return self.r


    def fetch_archs(self):
        pass


    def get_archives(self, binds):
        binds = binds['Message']
        try:
            server = binds['Server']
            print(f'cd C:\\SESP\\Atualizacoes; git clone {server}')
            os.system(f'cd C:\\SESP\\Atualizacoes; git clone {server}')

            self.r = {
                'Message' : 'OK'
            }

        except Exception as e:
            raise e
        return self.r


    def save_archives(self):
        try:
            #dir_path = os.path.dirname(os.path.realpath(__file__))
            #app_path = dir_path.split('\Atualizacoes')[0]

            dir_path = 'C:\\SESP\\Atualizacoes'
            app_path = 'C:\\SESP'
                        
            subprocess.run(['copy', f'{dir_path}\\SESP\\*', app_path], shell=True)
            
            subprocess.run(['rmdir', '/Q', '/S', f'{dir_path}\\SESP'], shell=True)

            self.r = {
                'Message' : 'OK'
            }

        except Exception as e:
            raise e
        return self.r


class Controller():
    def __init__(self):
        try:
            path = 'C:\\SESP'
            path = Path(path)
            if path.is_dir():
                self.updater = Update()
                self.update()
            else:
                self.installer = Installer()
                self.install()
        except Exception as e:
            raise e
        finally:
            os.system('python C:\\SESP\\start.pyw')


    def install(self):
        try:
            self.installer.python_install()
            self.title = 'Aguardando a instalação do Python3'
            self.body = ''
            SystemTray().notify(self.title, self.body)

            self.installer.git_install()
            self.title = 'Aguardando a instalação do GIT'
            self.body = ''
            SystemTray().notify(self.title, self.body)

            self.installer.sesp_install()

            self.installer.install_dependencies()

        except Exception as e:
            raise e
        finally:
            os.system('net use W: /delete >nul')
        return True

    
    def update(self):
        try:
            self.updater.start()
        except:
            raise

if __name__ == "__main__":
    try:
        Controller()
    except Exception as e:
        print(e)
        os.system('pause')

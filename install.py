from pathlib import Path
import configparser
import platform
import subprocess
import sys
import shutil
import time
import os


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
            response = subprocess.run(["mkdir", "C:\\installers"], shell=True)
            if response.returncode != 0:
                print('Não foi preciso criar o diretório\n')
            response = subprocess.run(["mkdir", "C:\\.SESP"], shell=True)
            if response.returncode != 0:
                print('Não foi preciso criar o diretório\n')

        except Exception as e:
            raise e

        self.path_of_installer_is_created = True
        return True


    def exclude_path_of_installers(self):
        try:
            shutil.rmtree('C:\\installers')
        except Exception as e:
            raise e
        
        self.path_of_installer_is_created = False
        return True


class Installer():
    def __init__(self):
        self.computer_controller = Computer()


    def python_install(self):
        try:
            if not self.computer_controller.path_of_installer_is_created:
                self.computer_controller.create_path_of_installers()
            so, arch, name = Computer().get_computer_platform()
            if '64' in arch:
                path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Python\\Python64.exe"
            else:
                path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Python\\Python32.exe"
            response = subprocess.run(["copy", path_installer, "C:\\installers\\Python.exe"], shell=True)

            os.system('start C:\\installers\\Python.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0')
        
        except Exception as e:
            raise e
        return True

    
    def install_dependencies(self):
        try:
            os.system('pip install requirements.txt')
        except Exception as e:
            raise e

        return True

    
    def git_install(self):
        try:
            if not self.computer_controller.path_of_installer_is_created:
                self.computer_controller.create_path_of_installers()
            so, arch, name = Computer().get_computer_platform()
            if '64' in arch:
                path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Git\\Git64.exe"
            else:
                path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Git\\Git32.exe"

            response = subprocess.run(["copy", path_installer, "C:\\installers\\Git.exe"], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível copiar o git para a máquina')

            os.system('start C:\\installers\\Git.exe /VERYSILENT /SUPPRESSMSGBOXES')

        except Exception as e:
            raise e
        return True


    def sesp_install(self):
        try:
            os.system('cls')
            print('Aguardando a instalação do GIT')
            try:
                self.computer_controller.exclude_path_of_installers()
            except:
                time.sleep(2)
                self.sesp_install()
            print('Instalando o SESP')

            if not self.computer_controller.path_of_installer_is_created:
                self.computer_controller.create_path_of_installers()

            with open('C:\\.SESP\\Sesp.bat', 'w') as bat: 
                script = f"""
                cd C:\\
                git clone https://github.com/duzzsys/SESP.git
                cd C:\\SESP
                git clone -b master_version https://github.com/duzzsys/SESP.git Atualizacoes
                start start.pyw
                """
                bat.write(script)
            os.system('C:\\.SESP\\Sesp.bat')
            
            response = subprocess.run(['mklink', 'C:\\Users\\Administrador\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup', 'C:\\SESP\\start.pyw'], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível fazer a cópia da pasta atualizada')
            
            shutil.rmtree('C:\\.SESP')
            
            
        except Exception as e:
            raise e
        return True


class Update():
    def __init__(self):
        self.binds = self.get_binds()


    def start(self):
        version = self.get_version(self.binds)
        need_to_update = self.need_to_update(version)


        if need_to_update['Message'] == True:
            self.get_archives(self.binds)
            self.save_archives()


    def get_binds(self):
        try:
            conf = configparser.ConfigParser()
            conf.read('Atualizacoes\\conf.cfg')

            remote = conf.get('git_repo', 'remote')
            server = conf.get('git_repo' ,'server')
            branch_version = conf.get('git_repo', 'branch_version')

            bind = {
                'Remote' : remote,
                'Server' : server,
                'BranchVersion' : branch_version
            }
            self.r = {
                    'Message' : bind
                }
        except Exception as e:
            raise e
        return self.r


    def get_version(self, binds):
        binds = binds['Message']
        try:
            remote = binds['Remote']
            branch_version = binds['BranchVersion']

            response = subprocess.run(["git", "pull"], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível utilizar o git pull')

            conf = configparser.ConfigParser()
            conf.read('conf.cfg')

            current_version = conf.get('current_version', 'version')

            self.r = {
                'Message' : {
                    'CurrentVersion' : current_version
                }
            }
            print(self.r)
        except Exception as e:
            raise e
        return self.r


    def need_to_update(self, version):
        version = version['Message']
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__)).split('\Atualizacoes')[0]
            dir_path = dir_path.replace('\\', '\\\\')
            
            conf = configparser.ConfigParser()
            conf.read(f'{dir_path}\\conf.cfg')

            current_version = conf.get('current_version', 'version')
            if current_version != version['CurrentVersion']:
                self.r = {
                    'Message' : True
                }
            else:
                print('Already updated')
            
        except Exception as e:
            raise e
        return self.r


    def fetch_archs(self):
        pass


    def get_archives(self, binds):
        binds = binds['Message']
        try:
            server = binds['Server']

            response = subprocess.run(['git', 'clone', server], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível utilizar o git clone')

            self.r = {
                'Message' : 'OK'
            }

        except Exception as e:
            raise e
        return self.r


    def save_archives(self):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            app_path = dir_path.split('\Atualizacoes')[0]
            
            dir_path = dir_path.replace('\\', '\\\\')
            app_path = app_path.replace('\\', '\\\\')
            
            response = subprocess.run(['copy', f'{dir_path}\\SESP\\*', app_path], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível fazer a cópia da pasta atualizada')
            
            response = subprocess.run(['rmdir', '/Q', '/S', f'{dir_path}\\SESP'], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível deletar a pasta de atualização')

            self.r = {
                'Message' : 'OK'
            }

        except Exception as e:
            raise e
        return self.r


class Controller():
    def __init__(self):
        self.installer = Installer()
        self.updater = Update()

        try:
            path = 'C:\\SESP'
            path = Path(path)
            if path.is_dir():
                self.update()
            else:
                self.install()
        except Exception as e:
            raise e


    def install(self):
        try:
            self.installer.python_install()
            self.installer.git_install()
            self.installer.install_dependencies()
            self.installer.sesp_install()
        except Exception as e:
            raise e
        return True

    
    def update(self):
        try:
            self.updater.start()
        except:
            raise

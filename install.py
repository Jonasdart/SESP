import platform
import subprocess
import sys
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
            response = subprocess.run(["mkdir", "C:\\install"], shell=True)
            if response.returncode != 0:
                print('Não foi preciso criar o diretório\n')
        except Exception as e:
            raise e

        self.path_of_installer_is_created = True
        return True


    def exclude_path_of_installers(self):
        try:
            response = subprocess.run(["erase", "/q", "C:\\install\\inst.exe"], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível apagar o executável')
            response = subprocess.run(["erase", "/q", "inst.bat"], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível apagar o script')
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
            so, arch = Computer().get_computer_platform()
            if '64' in arch:
                path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Git\\python64.exe"
            else:
                path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Git\\python32.exe"
            response = subprocess.run(["copy", path_installer, "C:\\install\\inst.exe"], shell=True)
            with open('inst.bat', 'w') as bat:
                script = f"""
                cd C:\\install
                start inst.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
                """
                bat.write(script)
            response = subprocess.run(['inst.bat'])
            if response.returncode != 0:
                raise Exception('Não foi possível instalar o python para a máquina')
        except Exception as e:
            raise e
        return True

    
    def git_install(self):
        try:
            so, arch = Computer().get_computer_platform()
            if '64' in arch:
                path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Git\\Git64.exe"
            else:
                path_installer = "\\\\192.168.0.2\\d\\TI\\Programas\\Programação, Imagem e Video\\Git\\Git32.exe"

            response = subprocess.run(["copy", path_installer, "C:\\install\\inst.exe"], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível copiar o git para a máquina')

            with open('inst.bat', 'w') as bat:
                script = """
                cd C:\\install
                start inst.exe /VERYSILENT
                """
                bat.write(script)
            response = subprocess.run(['inst.bat'])
            if response.returncode != 0:
                raise Exception('Não foi possível instalar o git para a máquina')
        except Exception as e:
            raise e
        return True


    def sesp_install(self):
        try:
            with open('inst.bat', 'w') as bat: 
                script = f"""
                cd C:\\install
                git clone https://github.com/duzzsys/SESP.git
                cd SESP
                git clone -b master_version https://github.com/duzzsys/SESP.git Atualizações       
                start main.py  True
                """
                bat.write(script)
            response = subprocess.run(['inst.bat'])
            if response.returncode != 0:
                raise Exception('Não foi possível instalar o sesp para a máquina')
            Computer().exclude_path_of_installers()
            os.system('shutdown -r -t 1')
        except Exception as e:
            raise e
        return True


class Controller():
    def __init__(self):
        self.installer = Installer()


    def install(self):
        try:
            self.installer.python_install()
            self.installer.git_install()
            self.installer.sesp_install()
        except Exception as e:
            raise e
        return True
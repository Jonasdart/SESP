import configparser
import os
import subprocess
import sys


class Update():
    def __init__(self):
        binds = self.get_binds()

        version = self.get_version(binds)
        need_to_update = self.need_to_update(version)
        
        print(need_to_update['Message'])

        if need_to_update['Message'] == True:
            self.get_archives(binds)
            self.save_archives()


    def get_binds(self):
        try:
            conf = configparser.ConfigParser()
            conf.read('conf.cfg')

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
            self.r = {
                'Message' : {
                    'Error' : 'main.py get_binds ' + str(e) 
                }
            }
        return self.r


    def get_version(self, binds):
        binds = binds['Message']
        try:
            remote = binds['Remote']
            branch_version = binds['BranchVersion']

            response = subprocess.run(["git", "pull", remote, branch_version], shell=True)
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
        except Exception as e:
            self.r = {
                'Message' : {
                    'Error' : 'main.py get_version ' + str(e) 
                }
            }
        return self.r


    def need_to_update(self, version):
        version = version['Message']
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__)).split('\Atualizações')[0]
            dir_path = dir_path.replace('\\', '\\\\')
            
            conf = configparser.ConfigParser()
            conf.read(f'{dir_path}\\conf.cfg')

            current_version = conf.get('current_version', 'version')
            if current_version != version['CurrentVersion']:
                self.r = {
                    'Message' : True
                }
            else:
                raise Exception('Already updated')
            
        except Exception as e:
            self.r = {
                'Message' : {
                    'Error' : 'main.py need_to_update ' + str(e) 
                }
            }
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
            self.r = {
                'Message' : {
                    'Error' : 'main.py get_archives ' + str(e) 
                }
            }
        return self.r


    def save_archives(self):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            app_path = dir_path.split('\Atualizações')[0]
            
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
            self.r = {
                'Message' : {
                    'Error' : 'main.py save_archives ' + str(e) 
                }
            }
        return self.r


    def install_sesp(self, inventory_number):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__)).split('\Atualizações')[0]
            dir_path = dir_path.replace('\\', '\\\\')
            
            conf = configparser.ConfigParser()
            conf.read(f'{dir_path}\\computer.cfg')

            conf.set('computer', 'inventory_number', inventory_number)

            with open('computer.cfg', 'w') as cfg:
                conf.write(cfg)

            try:
                self.install_dependencies()
            except Exception as e:
                raise Exception(e)

            response = subprocess.run(['mklink', 'C:\\Users\\Administrador\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup', dir_path+'\\model.pyw'], shell=True)
            if response.returncode != 0:
                raise Exception('Não foi possível fazer a cópia da pasta atualizada')

            self.r = {
                'Message' : 'OK'
            }
            
        except Exception as e:
            self.r = {
                'Message' : {
                    'Error' : 'main.py install_sesp ' + str(e) 
                }
            }
        return self.r


    def install_dependencies(self):
        with open('DEPENDENCIES.txt', 'r') as dp:
            dependencies = dp.readlines()
            for dependencie in dependencies:
                response = subprocess.run(['pip', 'install', dependencie], shell=True)
                if response.returncode != 0:
                    raise Exception('Não foi possível fazer a cópia da pasta atualizada')

if __name__ == "__main__":
    args = sys.argv
    inventory_number = args[1]
    if len(args) == 3:
        install = args[2]
    update = Update()
    if install == 'True':
        update.install_sesp(inventory_number)

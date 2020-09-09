import configparser
import os
import subprocess
import sys


class Installer():
    def __init__(self):
        self.binds = self.get_binds()


    def install(self):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__)).split('\Atualizações')[0]
            dir_path = dir_path.replace('\\', '\\\\')
            
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
        response = subprocess.run(['pip', 'install', 'requirements.txt'], shell=True)
        if response.returncode != 0:
            raise Exception('Não foi possível fazer a instalação das dependências')


    def update(self):
        version = self.get_version(self.binds)
        need_to_update = self.need_to_update(version)
        
        print(need_to_update['Message'])

        if need_to_update['Message'] == True:
            self.get_archives(self.binds)
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


if __name__ == "__main__":
    args = sys.argv
    install = 'False'

    if len(args) == 2:
        install = args[1]

    installer = Installer()

    if install == 'True':
        installer.install()
    else:
        installer.update()

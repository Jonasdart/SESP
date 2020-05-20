import configparser
import os
import subprocess


class Update():
    def __init__(self):
        binds = self.get_binds()

        version = self.get_version(binds)
        need_to_update = self.need_to_update(version)

        if need_to_update['Message']:
            self.get_archives(binds)
            self.save_archives()
            
        print(self.r)

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
            if response.returncode == 1:
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
            conf.read(f'{dir_path}\conf.cfg')

            current_version = conf.get('current_version', 'version')

            if current_version == version['CurrentVersion']:
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
            if response.returncode == 1:
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
            if response.returncode == 1:
                raise Exception('Não foi possível fazer a cópia da pasta atualizada')
            
            response = subprocess.run(['rmdir', '/Q', '/S', f'{dir_path}\\SESP'], shell=True)
            if response.returncode == 1:
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
     Update()

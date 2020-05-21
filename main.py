import configparser
import os


class Update():
    def __init__(self):
        pass


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
        try:
            remote = binds['Remote']
            branch_version = binds['BranchVersion']

            os.system(f'git pull {remote} {branch_version}')

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


    def get_archives(self, bind):
        try:
            server = bind['Server']
            os.system(f'git clone {server}')

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
            
            
            os.system(f'copy {dir_path}\\SESP\\* {app_path}')
            os.system(f'del {dir_path}\\SESP')
            
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

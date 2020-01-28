import configparser

config = configparser.ConfigParser()
config.read('sesp.ini')
print(dict(config['version_sesp']))

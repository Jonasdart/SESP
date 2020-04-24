import configparser

config = configparser.ConfigParser()
config.read('sesp.cfg')

d = dict(config['version_sesp'])

print(d)
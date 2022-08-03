import configparser

config = configparser.ConfigParser()
config.read("config.ini")

db_username = config['db']['username']
db_pwd = config['db']['password']
db_port = config['db']['port']
db_name = config['db']['name']
db_host = config['db']['host']

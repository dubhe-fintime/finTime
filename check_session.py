from flask import render_template
import configparser
import os

# ini 정보 취득
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

domain = config['SERVER']['domain']
port = config['SERVER']['port_1']

session_fail = config['CODE']['session_fail']


def check_session(session):
    if 'username' not in session:
        print('세션이 없거나, 만료')
        return session_fail
    else:
        return None 

    

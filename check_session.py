from flask import render_template
import configparser
import os
import jwt

# ini 정보 취득
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)


key = config['SERVER']['secret_key']
domain = config['SERVER']['domain']
port = config['SERVER']['port_1']

session_fail = config['CODE']['session_fail']


def check_session(session,token):
    try:
        payload = jwt.decode(token, key, algorithms=['HS256'])
        if session.get("username") == payload.get("user_id"): 
            return False
        else:
            return session_fail
    except jwt.ExpiredSignatureError:
        return session_fail
    except jwt.InvalidTokenError:
        return session_fail
    
    

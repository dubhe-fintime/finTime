from flask import app
import datetime
import jwt
import configparser
import os

environment = os.getenv('ENVIRONMENT', 'development')
if environment == 'production':
    config_path = os.path.join(os.getcwd(), 'config.ini')
else:
    config_path = os.path.join(os.getcwd(), 'config_development.ini')
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")
key = config['SERVER']['secret_key']


def create_jwt_token(user_id):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  
    payload = {
        'user_id': user_id,
        'exp': expiration_time
    }
    token = jwt.encode(payload, key, algorithm='HS256')
    print(f"토큰 생성완료 >> {user_id}  || {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} || {token}")
    return token



from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import subprocess
import os
import configparser

# 설정 파일 읽기
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

server_host = config['SERVER']['server_host']
port4 = int(config['SERVER']['port_4'])
ssl_cert = config['SECURE']['ssl_cert']
ssl_key = config['SECURE']['ssl_key']

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # 모든 origin 허용

LOG_FILE_PATH = "/home/finTime/logs/batch_log_20250402.log"

# WebSocket에서 보낼 로그 파일
def tail_log():
    process = subprocess.Popen(['tail', '-f', LOG_FILE_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line.strip()

# WebSocket 이벤트 핸들러
@socketio.on("connect")
def handle_connect():
    print("클라이언트 WebSocket 연결됨")

@socketio.on("request_logs")
def send_logs():
    for line in tail_log():
        socketio.emit("log_update", line)

if __name__ == '__main__':
    socketio.run(app, host=server_host, port=port4, ssl_context=(ssl_cert, ssl_key), allow_unsafe_werkzeug=True)

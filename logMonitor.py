import subprocess
import os
import configparser
import time
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

# 설정 파일 읽기
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

server_host = config['SERVER']['server_host']
port2 = int(config['SERVER']['port_2'])
ssl_cert = config['SECURE']['ssl_cert']
ssl_key = config['SECURE']['ssl_key']

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE_PATH = "/home/finTime/logs/batch_log_20250402.log"

# WebSocket에서 보낼 로그 파일
def tail_log():
    """ 실시간 로그를 지속적으로 읽어오는 함수 """
    with subprocess.Popen(['tail', '-F', LOG_FILE_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        for line in process.stdout:
            if line:
                socketio.emit("log_update", line.strip())  # 클라이언트에 실시간 전송
            socketio.sleep(0.1)  # 비동기 루프 유지

# WebSocket 이벤트 핸들러
@socketio.on("connect")
def handle_connect():
    print("클라이언트 WebSocket 연결됨")

@socketio.on("request_logs")
def send_logs():
    """ 클라이언트가 로그 요청하면 `tail_log()` 실행 """
    socketio.start_background_task(target=tail_log)  # 백그라운드 태스크로 실행

if __name__ == '__main__':
    socketio.run(app, host=server_host, port=port2, ssl_context=(ssl_cert, ssl_key), allow_unsafe_werkzeug=True)

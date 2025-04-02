from flask import Flask, render_template, request, jsonify
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
port2 = int(config['SERVER']['port_2'])
ssl_cert = config['SECURE']['ssl_cert']
ssl_key = config['SECURE']['ssl_key']

LOG_DIR = "/home/finTime/logs/"

def get_log_files():
    """ 로그 디렉토리 내의 파일 목록 반환 """
    try:
        return [f for f in os.listdir(LOG_DIR) if os.path.isfile(os.path.join(LOG_DIR, f))]
    except Exception as e:
        print(f"파일 목록 불러오기 실패: {e}")
        return []

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_logs")
def get_logs():
    """ 로그 파일 목록 API """
    return jsonify(get_log_files())

@socketio.on("request_logs")
def send_logs(log_filename):
    """ 선택한 로그 파일을 실시간으로 스트리밍 """
    log_path = os.path.join(LOG_DIR, log_filename)
    
    if not os.path.exists(log_path):
        socketio.emit("log_update", f"파일을 찾을 수 없습니다: {log_filename}")
        return
    
    process = subprocess.Popen(['tail', '-f', log_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        socketio.emit("log_update", line.strip())

if __name__ == '__main__':
    socketio.run(app, host=server_host, port=port2, ssl_context=(ssl_cert, ssl_key), allow_unsafe_werkzeug=True)

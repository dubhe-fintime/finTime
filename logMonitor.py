from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import subprocess
import os
import configparser
from datetime import datetime, timedelta

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

LOG_DIR = "/home/finTime/logs/"  # 로그 파일이 저장된 폴더
is_tail_running = False  # 🟢 tail_log 실행 상태 변수

def get_latest_log_file():
    """ 오늘 날짜 로그 파일이 있으면 사용하고, 없으면 어제 로그 파일을 반환 """
    today = datetime.now().strftime("%Y%m%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

    today_log = os.path.join(LOG_DIR, f"batch_log_{today}.log")
    yesterday_log = os.path.join(LOG_DIR, f"batch_log_{yesterday}.log")

    if os.path.exists(today_log):
        return today_log
    elif os.path.exists(yesterday_log):
        return yesterday_log
    else:
        return None  # 로그 파일이 없으면 None 반환

# WebSocket에서 보낼 로그 파일
def tail_log():
    global is_tail_running
    if is_tail_running:
        return  # 🛑 이미 실행 중이면 중복 실행 방지

    log_file = get_latest_log_file()
    if not log_file:
        print("❌ 로그 파일을 찾을 수 없습니다.")
        return

    is_tail_running = True
    print(f"📂 사용 중인 로그 파일: {log_file}")

    with subprocess.Popen(['tail', '-f', log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        for line in process.stdout:
            if line:
                socketio.emit("log_update", line.strip())  # 실시간 로그 전송
            #socketio.sleep(0.1)  # 비동기 루프 유지

# WebSocket 이벤트 핸들러
@socketio.on("connect")
def handle_connect():
    print("클라이언트 WebSocket 연결됨")

@socketio.on("request_logs")
def send_logs():
    global is_tail_running
    if not is_tail_running:  # 🔥 실행 중이 아닐 때만 tail_log 실행
        socketio.start_background_task(target=tail_log)

if __name__ == '__main__':
    socketio.run(app, host=server_host, port=port2, ssl_context=(ssl_cert, ssl_key), allow_unsafe_werkzeug=True)

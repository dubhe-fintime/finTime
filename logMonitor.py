from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
import subprocess
import os
import configparser
from datetime import datetime, timedelta
from functools import partial

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

#LOG_FILE_PATH = "/home/finTime/logs/batch_log_20250402.log"
LOG_DIR = "/home/finTime/logs/"
is_tail_running = False
log_process = None  # 로그 프로세스를 관리하는 변수


# WebSocket에서 보낼 로그 파일
def tail_log(file_path):
    global is_tail_running, log_process
    if is_tail_running:
        return  # 중복 실행 방지
    LOG_FILE_PATH = file_path
    is_tail_running = True
    log_process = subprocess.Popen(
        ['tail', '-n', '100', '-F', LOG_FILE_PATH],  # 최신 100줄도 포함
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,  # 한 줄씩 버퍼링
        universal_newlines=True,  # 개행 문자 자동 변환
        text=True
    )

    try:
        for line in iter(log_process.stdout.readline, ''):
            #print(f"서버 전송 로그: {line.strip()}", flush=True)  # 즉시 출력
            socketio.emit("log_update", line.strip())
            #socketio.sleep(0.1)
    except Exception as e:
        print(f"로그 스트리밍 오류 발생: {e}")
    finally:
        is_tail_running = False
        log_process = None


# WebSocket 이벤트 핸들러
@socketio.on("connect")
def handle_connect():
    print("클라이언트 WebSocket 연결됨")


@socketio.on("disconnect")
def handle_disconnect():
    global is_tail_running, log_process
    print("🚪 클라이언트 WebSocket 연결 종료됨")
    if log_process:
        log_process.terminate()  # tail 프로세스 종료
        log_process = None
    is_tail_running = False


@socketio.on("request_logs")
def send_logs(data):
    file_path = data.get("file_path")  # 클라이언트에서 보낸 file_path 받기
    if not file_path: # 화면에서 데이터가 안들어오면 default batch_log를 읽는다.
        today = datetime.now().strftime("%Y%m%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")

        today_log = os.path.join(LOG_DIR, f"batch_log_{today}.log")
        yesterday_log = os.path.join(LOG_DIR, f"batch_log_{yesterday}.log")

        if os.path.exists(today_log):
            file_path = today_log
        elif os.path.exists(yesterday_log):
            file_path =  yesterday_log
        else:
            return None  # 로그 파일이 없으면 None 반환
    
    #if not is_tail_running:
    print("333"*1000)
    print(file_path)
    socketio.start_background_task(partial(tail_log, file_path))


if __name__ == '__main__':
    socketio.run(app, host=server_host, port=port2, ssl_context=(ssl_cert, ssl_key), allow_unsafe_werkzeug=True)

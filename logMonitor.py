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
port2 = int(config['SERVER']['port_2'])
ssl_cert = config['SECURE']['ssl_cert']
ssl_key = config['SECURE']['ssl_key']

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_FILE_PATH = "/home/finTime/logs/batch_log_20250402.log"
is_tail_running = False
log_process = None  # 🟢 로그 프로세스를 관리하는 변수


# WebSocket에서 보낼 로그 파일
def tail_log():
    global is_tail_running, log_process
    if is_tail_running:
        return  # 🛑 중복 실행 방지

    is_tail_running = True
    log_process = subprocess.Popen(
        ['tail', '-F', LOG_FILE_PATH],  # ✅ `-F`로 변경 (파일 변경 감지 가능)
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,  # ✅ 한 줄씩 버퍼링
        universal_newlines=True,  # ✅ 개행 문자 자동 변환
        text=True
    )

    try:
        for line in iter(log_process.stdout.readline, ''):  # ✅ `iter()`를 사용하여 즉시 읽기
            if line:
                socketio.emit("log_update", line.strip())  # ✅ 실시간으로 클라이언트에게 로그 전송
            #socketio.sleep(0.1)
    except Exception as e:
        print(f"🚨 로그 스트리밍 오류 발생: {e}")
    finally:
        is_tail_running = False
        log_process = None


# WebSocket 이벤트 핸들러
@socketio.on("connect")
def handle_connect():
    print("✅ 클라이언트 WebSocket 연결됨")


@socketio.on("disconnect")
def handle_disconnect():
    global is_tail_running, log_process
    print("🚪 클라이언트 WebSocket 연결 종료됨")
    if log_process:
        log_process.terminate()  # 🛑 tail 프로세스 종료
        log_process = None
    is_tail_running = False


@socketio.on("request_logs")
def send_logs():
    if not is_tail_running:
        socketio.start_background_task(target=tail_log)


if __name__ == '__main__':
    socketio.run(app, host=server_host, port=port2, ssl_context=(ssl_cert, ssl_key), allow_unsafe_werkzeug=True)

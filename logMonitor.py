from flask import Flask
from flask_sock import Sock
import subprocess

app = Flask(__name__)
sock = Sock(app)

LOG_FILE_PATH = "/home/finTime/logs/batch_log_20250402.log"

# 특정 로그 파일을 실시간으로 읽어오는 함수
def tail_log():
    process = subprocess.Popen(['tail', '-f', LOG_FILE_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line.strip()  # 개행문자 제거 후 반환

# 웹소켓을 통해 로그 스트리밍
@sock.route('/logs')
def logs(ws):
    for line in tail_log():
        ws.send(line)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084, debug=True)

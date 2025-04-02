from flask import Flask
from flask_sock import Sock
import subprocess
import ssl

app = Flask(__name__)
sock = Sock(app)

LOG_FILE_PATH = "/home/finTime/logs/batch_log_20250402.log"

# WebSocket에서 보낼 로그 파일
def tail_log():
    process = subprocess.Popen(['tail', '-f', LOG_FILE_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        yield line.strip()

@sock.route('/logs')
def logs(ws):
    for line in tail_log():
        ws.send(line)

if __name__ == '__main__':
    # SSL 설정 추가
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='/etc/letsencrypt/live/fin-time.com/fullchain.pem', keyfile='/etc/letsencrypt/live/fin-time.com/privkey.pem')  # SSL 인증서 경로 지정

    app.run(host='0.0.0.0', port=8084, debug=True, ssl_context=context)

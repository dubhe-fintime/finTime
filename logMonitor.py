from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import os
import subprocess

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

LOG_DIR = "/home/finTime/logs"

# 로그 파일 목록 반환
@app.route("/log_files", methods=["GET"])
def get_log_files():
    try:
        files = [f for f in os.listdir(LOG_DIR) if f.endswith(".log")]
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 특정 로그 파일을 실시간으로 스트리밍
@socketio.on("request_logs")
def send_logs(data=None):
    if not data or "filename" not in data:
        socketio.emit("log_update", "⚠️ 로그 파일을 선택하세요.")
        return

    filename = data["filename"]
    log_path = os.path.join(LOG_DIR, filename)

    if not os.path.exists(log_path):
        socketio.emit("log_update", f"❌ 파일 '{filename}'이 존재하지 않습니다.")
        return

    process = subprocess.Popen(["tail", "-f", log_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        socketio.emit("log_update", line.strip())

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8084, allow_unsafe_werkzeug=True)

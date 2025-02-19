import os
import signal
import subprocess
import psutil
from flask import jsonify

BATCH_SCRIPT = "batch_script.py"  # 실행할 배치 스크립트 파일명
PID_FILE = "batch_pid.txt"  # 실행된 프로세스의 PID 저장 파일

# 프로세스 PID 확인
def get_running_pid():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())

        if psutil.pid_exists(pid):  # 프로세스가 실제로 존재하는지 확인
            return pid
        else:
            os.remove(PID_FILE)  # 존재하지 않는다면 PID 파일 삭제
    return None

# 배치 스크립트 실행
def start_batch():
    if get_running_pid():
        return jsonify({"status": "already_running", "message": "배치가 이미 실행 중입니다."}), 400
    
    OUTPUT_LOG  = os.path.join("logs", "batch_output.log")
    ERROR_LOG   = os.path.join("logs", "batch_error.log")
    process = subprocess.Popen(
        ["nohup", "python3", BATCH_SCRIPT, "&"],
        stdout=open(OUTPUT_LOG, "a"),
        stderr=open(ERROR_LOG, "a"),
        preexec_fn=os.setsid  # 세션을 분리하여 독립적으로 실행
    )

    with open(PID_FILE, "w") as f:
        f.write(str(process.pid))

    return jsonify({"status": "started", "message": "배치를 실행했습니다.", "pid": process.pid}), 200

# 배치 스크립트 중지
def stop_batch():
    pid = get_running_pid()
    if not pid:
        return jsonify({"status": "already_stopped", "message": "배치가 이미 중지 상태입니다."}), 400

    os.kill(pid, signal.SIGTERM)  # 프로세스 종료
    os.remove(PID_FILE)  # PID 파일 삭제

    return jsonify({"status": "stopped", "message": "배치를 중지했습니다."}), 200

# 배치 실행 상태 확인
def check_batch_status():
    pid = get_running_pid()
    if pid:
        return jsonify({"status": "running", "pid": pid}), 200
    return jsonify({"status": "stopped"}), 200
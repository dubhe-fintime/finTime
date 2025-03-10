import os
import signal
import subprocess
import psutil
from flask import jsonify

# 실행할 배치 스크립트 파일명 및 PID 저장 파일
BATCH_SCRIPTS = {
    1: ("batch_script.py", "batch_pid.txt"),
    2: ("batch_youtube.py", "batch_pid_youtube.txt"),
    3: ("batch_naverNews.py", "batch_pid_naverNews.txt"),
    4: ("batch_pubOffStock.py", "batch_pid_pubOffStock.txt"),
}

# 프로세스 PID 확인 및 업데이트
def get_running_pid(type):
    script_file, pid_file = BATCH_SCRIPTS.get(type, (None, None))
    if not script_file:
        return None

    # 1. PID 파일이 존재하면 해당 PID를 확인
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        if psutil.pid_exists(pid):  # 실제 프로세스가 존재하는지 확인
            return pid
        else:
            os.remove(pid_file)  # 존재하지 않는다면 PID 파일 삭제

    # 2. 실행 중인 프로세스를 찾아서 PID 파일 업데이트
    for proc in psutil.process_iter(attrs=['pid', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and script_file in " ".join(cmdline):  # 실행 중인지 확인
                with open(pid_file, "w") as f:
                    f.write(str(proc.info['pid']))
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return None

# 배치 스크립트 실행
def start_batch(type):
    script_file, pid_file = BATCH_SCRIPTS.get(type, (None, None))
    if not script_file:
        return jsonify({"status": "error", "message": "잘못된 배치 유형입니다."}), 400

    if get_running_pid(type):
        return jsonify({"status": "already_running", "message": "배치가 이미 실행 중입니다."}), 400

    OUTPUT_LOG = os.path.join("logs", "batch_output.log")
    ERROR_LOG = os.path.join("logs", "batch_error.log")

    process = subprocess.Popen(
        ["nohup", "python3", script_file, "&"],
        stdout=open(OUTPUT_LOG, "a"),
        stderr=open(ERROR_LOG, "a"),
        preexec_fn=os.setsid  # 세션을 분리하여 독립적으로 실행
    )

    with open(pid_file, "w") as f:
        f.write(str(process.pid))

    return jsonify({"status": "started", "message": "배치를 실행했습니다.", "pid": process.pid}), 200

# 배치 스크립트 중지
def stop_batch(type):
    pid = get_running_pid(type)
    if not pid:
        return jsonify({"status": "already_stopped", "message": "배치가 이미 중지 상태입니다."}), 400

    os.kill(pid, signal.SIGTERM)  # 프로세스 종료
    script_file, pid_file = BATCH_SCRIPTS.get(type, (None, None))
    
    if pid_file and os.path.exists(pid_file):
        os.remove(pid_file)  # PID 파일 삭제

    return jsonify({"status": "stopped", "message": "배치를 중지했습니다."}), 200

# 배치 실행 상태 확인
def check_batch_status(type):
    pid = get_running_pid(type)
    if pid:
        return jsonify({"status": "running", "pid": pid}), 200
    return jsonify({"status": "stopped"}), 200

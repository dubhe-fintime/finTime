import os
import signal
import subprocess
import psutil
from flask import jsonify

# 금융사 이벤트
BATCH_SCRIPT = "batch_script.py"  # 실행할 배치 스크립트 파일명
PID_FILE = "batch_pid.txt"  # 실행된 프로세스의 PID 저장 파일

# 유튜브
BATCH_SCRIPT_YOUTUBE = "batch_youtube.py"  # 실행할 배치 스크립트 파일명
PID_FILE_YOUTUBE = "batch_pid_youtube.txt"  # 실행된 프로세스의 PID 저장 파일

# 네이버 뉴스
BATCH_SCRIPT_NAVERNEWS = "batch_naverNews.py"  # 실행할 배치 스크립트 파일명
PID_FILE_NAVERNEWS = "batch_pid_naverNews.txt"  # 실행된 프로세스의 PID 저장 파일

# 프로세스 PID 확인
def get_running_pid(type):
    if type == 1:
        pid_file = PID_FILE
    elif type == 2:
        pid_file = PID_FILE_YOUTUBE
    else:
        pid_file = PID_FILE_NAVERNEWS
    
    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())

        if psutil.pid_exists(pid):  # 프로세스가 실제로 존재하는지 확인
            return pid
        else:
            os.remove(pid_file)  # 존재하지 않는다면 PID 파일 삭제
    return None

# 배치 스크립트 실행
def start_batch(type):
    if type == 1:
        script_file =BATCH_SCRIPT
        pid_file = PID_FILE
    elif type == 2:
        script_file =BATCH_SCRIPT_YOUTUBE
        pid_file = PID_FILE_YOUTUBE
    else:
        script_file =BATCH_SCRIPT_NAVERNEWS
        pid_file = PID_FILE_NAVERNEWS

    if get_running_pid(type):
        return jsonify({"status": "already_running", "message": "배치가 이미 실행 중입니다."}), 400
    
    OUTPUT_LOG  = os.path.join("logs", "batch_output.log")
    ERROR_LOG   = os.path.join("logs", "batch_error.log")
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
    if type == 1:
        pid_file = PID_FILE
    elif type == 2:
        pid_file = PID_FILE_YOUTUBE
    else:
        pid_file = PID_FILE_NAVERNEWS
    pid = get_running_pid(type)
    if not pid:
        return jsonify({"status": "already_stopped", "message": "배치가 이미 중지 상태입니다."}), 400

    os.kill(pid, signal.SIGTERM)  # 프로세스 종료
    os.remove(pid_file)  # PID 파일 삭제

    return jsonify({"status": "stopped", "message": "배치를 중지했습니다."}), 200

# 배치 실행 상태 확인
def check_batch_status(type):
    pid = get_running_pid(type)
    if pid:
        return jsonify({"status": "running", "pid": pid}), 200
    return jsonify({"status": "stopped"}), 200
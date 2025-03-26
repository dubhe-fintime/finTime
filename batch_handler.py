import os
import signal
import subprocess
import psutil
import logging
from datetime import datetime
from flask import jsonify

# 로그 설정
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
ERROR_LOG = os.path.join(LOG_DIR, "batch_error.log")

logging.basicConfig(
    filename=ERROR_LOG,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 실행할 배치 스크립트 파일명 및 PID 저장 파일
BATCH_SCRIPTS = {
    1: ("batch_script.py", "batch_pid.txt"),
    2: ("batch_youtube.py", "batch_pid_youtube.txt"),
    3: ("batch_naverNews.py", "batch_pid_naverNews.txt"),
    4: ("batch_pubOffStock.py", "batch_pid_pubOffStock.txt"),
    5: ("batch_product.py", "batch_pid_product.txt"),
    6: ("batch_loanProduct.py", "batch_pid_product.txt")
}

# 프로세스 PID 확인 및 업데이트
def get_running_pid(type):
    script_file, pid_file = BATCH_SCRIPTS.get(type, (None, None))
    if not script_file:
        return None

    if os.path.exists(pid_file):
        with open(pid_file, "r") as f:
            pid = int(f.read().strip())
        if psutil.pid_exists(pid):
            return pid
        else:
            os.remove(pid_file)

    for proc in psutil.process_iter(attrs=['pid', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and script_file in " ".join(cmdline):
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

    OUTPUT_LOG = os.path.join(LOG_DIR, "batch_output.log")

    try:
        process = subprocess.Popen(
            ["nohup", "python3", script_file, "&"],
            stdout=open(OUTPUT_LOG, "a"),
            stderr=subprocess.PIPE,  # 오류 로그를 직접 가져옴
            preexec_fn=os.setsid
        )

        # 오류 로그를 별도 파일에 기록
        _, error = process.communicate()
        if error:
            logging.error(error.decode("utf-8"))

        with open(pid_file, "w") as f:
            f.write(str(process.pid))

        return jsonify({"status": "started", "message": "배치를 실행했습니다.", "pid": process.pid}), 200

    except Exception as e:
        logging.error(f"배치 실행 중 오류 발생: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 배치 스크립트 중지
def stop_batch(type):
    pid = get_running_pid(type)
    if not pid:
        return jsonify({"status": "already_stopped", "message": "배치가 이미 중지 상태입니다."}), 400

    try:
        os.kill(pid, signal.SIGTERM)
        script_file, pid_file = BATCH_SCRIPTS.get(type, (None, None))
        if pid_file and os.path.exists(pid_file):
            os.remove(pid_file)
        return jsonify({"status": "stopped", "message": "배치를 중지했습니다."}), 200
    except Exception as e:
        logging.error(f"배치 중지 중 오류 발생: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 배치 실행 상태 확인
def check_batch_status(type):
    pid = get_running_pid(type)
    if pid:
        return jsonify({"status": "running", "pid": pid}), 200
    return jsonify({"status": "stopped"}), 200

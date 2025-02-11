#####################################
#####################################
##        관리자(5000 포트)         ##
#####################################
#####################################
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import timedelta

from flask import Flask, session, request, render_template, send_file
from flask_socketio import SocketIO
from flask_cors import CORS
from flask import jsonify

import time
from datetime import datetime

import os

import json

import configparser

from check_session import check_session

from corp.assurance import kyoboLife, ablLife ,dbLife,dongyangLife,heungkuklife,kdbLife,samsungLife,hanhwaLife,miraeAssetLife
from corp.assurance import samsungFire,heungkukFire,kbInsure,nhInsure
from corp.bank import hanaBank
from corp.card import kbCard,bcCard,hanaCard,samsungCard,shinhanCard,wooriCard

from dbconn import execute_mysql_query_select, execute_mysql_query_insert, execute_mysql_query_delete, execute_mysql_query_update, execute_mysql_query_rest, execute_mysql_query_update2

# 서버 경로 취득
script_dir = os.path.dirname(os.path.abspath(__file__))

# ini 정보 취득
config_path = os.path.join(script_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")
domain = config['SERVER']['domain']
port = config['SERVER']['port_1']
real_yn = config['SERVER']['real']
server_host = config['SERVER']['server_host']
success = config['CODE']['success']
error = config['CODE']['error']
ssl_cert = config['SECURE']['ssl_cert']
ssl_key = config['SECURE']['ssl_key']

########### 로그 셋팅부 START#################
logger = logging.getLogger('admin')
loggerlevel = config['LOG']['loggerlevel']

# 로그 레벨 문자열을 대문자로 변환하여 사용
if loggerlevel == "INFO":
    logger.setLevel(logging.INFO)
elif loggerlevel == "DEBUG":
    logger.setLevel(logging.DEBUG)
elif loggerlevel == "WARNING":
    logger.setLevel(logging.WARNING)
elif loggerlevel == "ERROR":
    logger.setLevel(logging.ERROR)
elif loggerlevel == "CRITICAL":
    logger.setLevel(logging.CRITICAL)
else:
    print("유효한 로그 레벨이 아닙니다.")

# 현재 스크립트 파일이 위치한 폴더 경로 가져오기
script_dir = os.path.dirname(os.path.abspath(__file__))

# logs 폴더 경로 설정
log_dir = os.path.join(script_dir, "logs")

# logs 폴더가 없으면 생성
os.makedirs(log_dir, exist_ok=True)

# 로그 파일 경로 설정
log_file = os.path.join(log_dir, "admin.log")

# 날짜별로 로그 파일 분리 (midnight: 자정에 로그 파일 분리)
handler = TimedRotatingFileHandler(
    log_file, when="midnight", interval=1, encoding="utf-8")
handler.suffix = "%Y-%m-%d"  # 로그 파일명에 붙을 날짜 형식 설정

# 로그 메시지 포맷 설정
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# 핸들러 추가
logger.addHandler(handler)

config['CODE']['session_fail']

app = Flask(__name__)
CORS(app)
app.secret_key = config['SERVER']['secret_key']  # 필수 값 (지정 필요)

# 세션 관리를 위한 시간 설정(10분)
app.permanent_session_lifetime = timedelta(minutes=10)


#CORS(app, resources={r"/*": {"origins": "http://allowed-origin.com"}})  # 모든 엔드포인트에 대해 CORS를 활성화
socketio = SocketIO(app)
rasa_process = None

# 하나은행 배치 호출
@app.route('/test1', methods=["POST"])
async def test1():
    results = await hanaBank.get081Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "081",
        "fin_id": "T000000001", # TASK ID 지정
        "result": results     # 응답결과

    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

################## 카드사 START #############################

# BC카드
@app.route('/card1', methods=["POST"])
async def card1():
    results = await bcCard.get361Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "361",
        "fin_id": "T000000014", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 하나카드
@app.route('/card2', methods=["POST"])
async def card2():
    results = await hanaCard.get374Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "374",
        "fin_id": "T000000015", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# KB카드
@app.route('/card3', methods=["POST"])
async def card3():
    results = await kbCard.get381Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "381",
        "fin_id": "T000000016", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 삼성카드
@app.route('/card4', methods=["POST"])
async def card4():
    results = await samsungCard.get365Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "365",
        "fin_id": "T000000017", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 신한카드
@app.route('/card5', methods=["POST"])
async def card5():
    results = await shinhanCard.get366Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "366",
        "fin_id": "T000000018", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 우리카드
@app.route('/card6', methods=["POST"])
async def card6():
    results = await wooriCard.get041Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "041",
        "fin_id": "T000000019", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

################## 카드사 END ###############################


################## 보험 START #############################

# ABL생명
@app.route('/test2', methods=["POST"])
async def test2():
    results = await ablLife.get437Data()
    
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "437",
        "fin_id": "T000000002", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 교보생명
@app.route('/test3', methods=["POST"])
async def test3():
    results = await kyoboLife.get433Data()

    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "433",
        "fin_id": "T000000003", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 동양생명
@app.route('/test4', methods=["POST"])
async def test4():
    results = await dongyangLife.get402Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
       
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "402",
        "fin_id": "T000000004", # TASK ID 지정
        "result": results     # 응답결과
    }
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 한화생명
@app.route('/test5', methods=["POST"])
async def test5():
    results = await hanhwaLife.get432Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "432",
        "fin_id": "T000000005", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 흥국생명
@app.route('/test6', methods=["POST"])
async def test6():
    results = await heungkuklife.get457Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "457",
        "fin_id": "T000000006", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# KDB생명
@app.route('/test7', methods=["POST"])
async def test7():
    results = await kdbLife.get458Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "458",
        "fin_id": "T000000007", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 삼성생명
@app.route('/test8', methods=["POST"])
async def test8():
    results = await samsungLife.get452Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "452",
        "fin_id": "T000000008", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 삼성화재
@app.route('/test9', methods=["POST"])
async def test9():
    results = await samsungFire.get441Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "441",
        "fin_id": "T000000009", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 흥국화재
@app.route('/test10', methods=["POST"])
async def test10():
    results = await heungkukFire.get403Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "403",
        "fin_id": "T000000010", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# KB손해보험
@app.route('/test11', methods=["POST"])
async def test11():
    results = await kbInsure.get444Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "444",
        "fin_id": "T000000011", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 미래에셋생명
@app.route('/test12', methods=["POST"])
async def test12():
    results = await miraeAssetLife.get431Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "431",
        "fin_id": "T000000012", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# NH손해보험
@app.route('/test13', methods=["POST"])
async def test13():
    results = await nhInsure.get449Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "449",
        "fin_id": "T000000013", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response




################## 보험 END ###############################
# SET BATCH LOG
def set_batch_log(batch_id, batch_nm, task_id, task_nm, st_date, ed_date, status, result_data):
    result_data_str = json.dumps(result_data, ensure_ascii=False)
    values = (batch_id, batch_nm, task_id, task_nm, st_date, ed_date, status, result_data_str)
    execute_mysql_query_insert("Q1",values) # BATCH LOG 등록

# SET BATCH 데이터
def set_batch_rst(bank_cd, title, evt_id, startDt, endDt, thumbNail, image, noti, listURL, detailURL):
    values = (bank_cd, title, evt_id, startDt, endDt, thumbNail, image, noti, listURL, detailURL)
    #execute_mysql_query_delete('Q3', []) # BATCH 데이터 전체 삭제
    execute_mysql_query_insert("Q2",values) # BATCH 데이터 등록

# SET BATCH 데이터 삭제
def del_batch_rst(cnt):
    if cnt == 1:
        execute_mysql_query_delete('Q3', []) # BATCH 데이터 전체 삭제


# 에러코드 보는 곳
@app.errorhandler(404)
def page_not_found(e):
    return render_template('common/customError.html'), 404

# 관리자관련 수정 시작 KCR 250211
# 관리자 index 화면 호출
@app.route("/")
def adminLogin():
    return render_template("common/login.html", domain=domain, port=port)
    #return render_template("page/test.html", domain=domain, port=port)

# 관리자 로그인 화면 호출
@app.route('/adminLogin', methods=["POST"])
def adminLogin_check():
    # 로그인 시 무조건 성공 리턴
    return [success]
    # 로그인 기능 없으므로 주석 시작 kcr 250211
    # data = request.get_json()
    # username = data['id']
    # password = data['pw']
    # values = [username, password]
    # results = execute_mysql_query_select("Q1", )

    # # 관리자 아이디로 등록이 되지 않았을 경우
    # if len(results) < 1 or results[0][1] == 'N':  # N은 사용 여부
    #     # message = "접근 거부: 사용 여부 및 아이디 확인바람"
    #     message = "접근 거부: 사용 여부 및 아이디 확인바람"
    #     return [error]
    # else:

    #     # 로그인시 세션 생성
    #     session['username'] = username
    #     session['usergroup'] = results[0][2]
    #     session.permanent = True
    #     logger.info(f'Connect || ID -- {username}')

    #     temp_time = datetime.now()
    #     formatted_datetime = temp_time.strftime("%Y-%m-%d %H:%M:%S")
    #     session['start_time'] = formatted_datetime
    #     # print(session['start_time'])
    #     return [success]
    # 로그인 기능 없으므로 주석 종료 kcr 250211

# 클라이언트 로그인 API
@app.route('/clientLogin', methods=["POST"])
def clientLogin_check():
    data = request.get_json()  # 전송된 JSON 데이터 받아오기
    username = data.get("username")
    password = data.get("password")
    values = [username, password]
    results = execute_mysql_query_select("Q27", values)
    print(results)

    return results

# 관리자 메인 화면 호출
@app.route("/adminMain")
def adminMain():
    return render_template("common/LNB.html", domain=domain, port=port)
    # 로그인 기능 없으므로 주석 시작 kcr 250211
    # result = check_session(session)
    # if result == config['CODE']['session_fail']:
    #     session_data = None
    #     return render_template("common/LNB.html", domain=domain, port=port, session=session_data)
    # else:
    #     session_data = session.get('username')
    #     session_start_time = session.get('start_time')
    #     session_time = session.get('time')
    #     return render_template("common/LNB.html", domain=domain, port=port, session=session_data, starttime=session_start_time, time=session_time)
    # 로그인 기능 없으므로 주석 종료 kcr 250211

# 관리자 금융사 관리 화면 호출
@app.route("/financeManage")
def financeManage():
    return render_template("financeManage/financeManage.html", domain=domain, port=port)

# 관리자 스크래핑 데이터 관리 화면 호출
@app.route("/scrapingManage")
def scrapingManage():
    return render_template("scrapingManage/scrapingManage.html", domain=domain, port=port)

# 관리자 스크래핑 데이터 관리 화면 호출
@app.route("/contentsManage")
def contentsManage():
    return render_template("contentsManage/contentsManage.html", domain=domain, port=port)

# 로그아웃 기능
@app.route('/logout', methods=['POST'])
def logout():
    # data = request.get_json()
    # if session.get('username') == data:
    #     session.pop('username', None)
    return [success]
# 관리자관련 수정 끝 KCR 250211
# Admin main contents 노출 화면 (구글 표)
@app.route("/adminMainContents")
def adminMainContents():
    return render_template("common/adminMainContents.html", domain=domain, port=port)

# 파일 다운로드
@app.route('/fileDownload', methods=['POST'])
def download_file():
    # 클라이언트가 보낸 데이터에서 파일 경로 및 다운로드 경로 가져오기
    file_name = request.form.get('file_name', default='', type=str)
    file_path = "..//downloads//"+file_name
    # 클라이언트에게 파일 다운로드 제안
    response = send_file(file_path, as_attachment=True)
    print(response)

    return response

if __name__ == "__main__":
    while True:
        try:
            if real_yn == "Y":  # 운영 서버 여부
                # SSL 인증서 및 키 파일 경로
                # restart_rasa()
                socketio.run(app, host=server_host, port=port, ssl_context=(
                    ssl_cert, ssl_key), allow_unsafe_werkzeug=True)
            else:
                # 앱 실행
                # socketio.run(app)
                app.run(host='0.0.0.0', port=port, debug=True)
        except Exception as e:
            logging.error(f"Server Error: {e}")
        time.sleep(5)  # 서버가 중단되었을 경우 5초 후 재시작 시도

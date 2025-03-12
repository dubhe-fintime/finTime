#####################################
#####################################
##        관리자(8081 포트)         ##
#####################################
#####################################
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import timedelta

from flask import Flask, abort, session, request, render_template, send_file, send_from_directory
from flask_socketio import SocketIO
from flask_cors import CORS
from flask import jsonify

import uuid

import time
from datetime import datetime

import ipaddress

import os
import base64

import json

import configparser

from check_session import check_session

from corp.assurance import kyoboLife, ablLife ,dbLife,dongyangLife,heungkuklife,kdbLife,samsungLife,hanhwaLife,miraeAssetLife,shinhanLife
from corp.assurance import samsungFire,heungkukFire,kbInsure,nhInsure
from corp.bank import hanaBank,citiBank,imBank,kbBank,scBank,shinhanBank,wooriBank,ibkBank,kakaoBank,bnkBank,jejuBank
from corp.card import kbCard,bcCard,hanaCard,samsungCard,shinhanCard,wooriCard, lotteCard
from corp.stock import dashinStock,kbStock,yuantaStock,samsungStock,hankookStock,shinhanStock,kiwoomStock,hanaStock,miraeAssetStock

from corp.capital import shinhanCapitial

from youtube.youtube_channel_id import getChannelId
from youtube.youtube_channel import getChannelData

from util.pubOffStock import pubOffStock

from batch_handler import start_batch, stop_batch, check_batch_status

from util import getHoliday

from dbconn import execute_mysql_query_select, execute_mysql_query_insert, execute_mysql_query_delete, execute_mysql_query_update, execute_mysql_query_rest, execute_mysql_query_update2,execute_mysql_query_insert_update_bulk, execute_mysql_query_insert2

# 서버 경로 취득
script_dir = os.path.dirname(os.path.abspath(__file__))

environment = os.getenv('ENVIRONMENT', 'development')

# ini 정보 취득
if environment == 'production':
    config_path = os.path.join(script_dir, 'config.ini')
else:
    config_path = os.path.join(script_dir, 'config_development.ini')

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

ALLOWED_IPS = {"3.37.13.12", "127.0.0.1", "192.168.1.100"} # 회사, 서버로컬 IP SET (외부 IP접근 차단용)
ALLOWED_SUBNETS = [ipaddress.IPv4Network("192.168.0.0/24")]  # 192.168.0.* 대역

# def is_allowed_ip(ip):
#     # 개별 허용 IP 확인
#     if ip in ALLOWED_IPS:
#         return True

#     # 서브넷 검사
#     ip_obj = ipaddress.IPv4Address(ip)
#     return any(ip_obj in subnet for subnet in ALLOWED_SUBNETS)

# @app.before_request
# def limit_remote_addr():
#     # X-Forwarded-For에서 실제 클라이언트 IP 가져오기
#     client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    
#     # 여러 개의 IP가 있을 경우 첫 번째 IP 선택
#     if "," in client_ip:
#         client_ip = client_ip.split(",")[0].strip()

#     print(f"##### Client IP: {client_ip} | Host: {request.host} #####")

#     # 동일 서버에서 요청하는 경우 허용
#     if client_ip in ["127.0.0.1", "::1"] or request.host in ["admin.fin-time.com", "localhost"]:
#         return

#     # 특정 IP 대역 허용
#     if not is_allowed_ip(client_ip):
#         abort(403)  # 403 Forbidden 응답

# 날씨 API
async def holidayAPI():
    results = await getHoliday.API_Holiday()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "fin_id": "T000000036", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

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

# 롯데카드
@app.route('/card7', methods=["POST"])
async def card7():
    results = await lotteCard.get368Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "368",
        "fin_id": "T000000038", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

################## 카드사 END ###############################
################## 은행 START ###############################

# 씨티은행
@app.route('/bank1', methods=["POST"])
async def bank1():
    results = await citiBank.get027Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "027",
        "fin_id": "T000000020", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# IM뱅크
@app.route('/bank2', methods=["POST"])
async def bank2():
    results = await imBank.get031Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "031",
        "fin_id": "T000000021", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 국민은행
@app.route('/bank3', methods=["POST"])
async def bank3():
    results = await kbBank.get004Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "004",
        "fin_id": "T000000022", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# SC제일은행
@app.route('/bank4', methods=["POST"])
async def bank4():
    results = await scBank.get023Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "023",
        "fin_id": "T000000023", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 신한은행
@app.route('/bank5', methods=["POST"])
async def bank5():
    results = await shinhanBank.get088Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "088",
        "fin_id": "T000000024", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 우리은행
@app.route('/bank6', methods=["POST"])
async def bank6():
    results = await wooriBank.get020Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "020",
        "fin_id": "T000000025", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# IBK기업은행
@app.route('/bank7', methods=["POST"])
async def bank7():
    results = await ibkBank.get003Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "003",
        "fin_id": "T000000026", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 카카오뱅크
@app.route('/bank8', methods=["POST"])
async def bank8():
    results = await kakaoBank.get090Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "090",
        "fin_id": "T000000027", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 부산은행
@app.route('/bank9', methods=["POST"])
async def bank9():
    results = await bnkBank.get032Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "032",
        "fin_id": "T000000039", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 제주은행
@app.route('/bank10', methods=["POST"])
async def bank10():
    results = await jejuBank.get035Data()
    status = 200
    img_path = os.path.join(app.config['FILE_FOLDER'],"cor_thumb") 

    #폴더,DB 삭제부
    execute_mysql_query_delete("Q32",[])
    for exist_file in os.listdir(img_path):
        file_path = os.path.join(img_path, exist_file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for index, item in enumerate(results):
        # 에러일 경우
        if 'ERROR' in item:
            status = 500
        else:
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = uuid.uuid4().hex[:12]  
            filename = f"{now}_{unique_id}.png" 
            image_data = base64.b64decode(item["thumbNail"]) 
            total_path = os.path.join(img_path, filename) #파일저장 경로
            
            # 이미지 저장
            with open(total_path, "wb") as file:
                file.write(image_data)
                print(f">>>>>{filename} 저장 완료")
                file.close()
            
            results[index]["thumbNail"] = total_path

            #DB 추가 (배치가 하루단위라 기존데이터 삭제후 INSERT)
            values = (filename, f"jeju_thumb{index+1}.png", filename.split(".")[-1], img_path)
            execute_mysql_query_insert("Q4",values)

    # return을 for 루프 밖으로 이동
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "035",
        "fin_id": "T000000040", # TASK ID 지정
        "result": results     # 응답결과
    }

    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response


################## 은행 END ###############################
################## 증권 START #############################

# 대신증권
@app.route('/stock1', methods=["POST"])
async def stock1():
    results = await dashinStock.get267Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "267",
        "fin_id": "T000000028", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# KB증권
@app.route('/stock2', methods=["POST"])
async def stock2():
    results = await kbStock.get218Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "218",
        "fin_id": "T000000029", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 유안타증권
@app.route('/stock3', methods=["POST"])
async def stock3():
    results = await yuantaStock.get209Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "209",
        "fin_id": "T000000030", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 삼성증권
@app.route('/stock4', methods=["POST"])
async def stock4():
    results = await samsungStock.get240Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "240",
        "fin_id": "T000000031", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 한국투자증권
@app.route('/stock5', methods=["POST"])
async def stock5():
    results = await hankookStock.get243Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "243",
        "fin_id": "T000000032", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 키움증권
@app.route('/stock6', methods=["POST"])
async def stock6():
    results = await kiwoomStock.get264Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "264",
        "fin_id": "T000000033", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 신한투자증권
@app.route('/stock7', methods=["POST"])
async def stock7():
    results = await shinhanStock.get278Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "278",
        "fin_id": "T000000034", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 하나증권
@app.route('/stock8', methods=["POST"])
async def stock8():
    results = await hanaStock.get270Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "270",
        "fin_id": "T000000035", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

# 미래에셋증권
@app.route('/stock9', methods=["POST"])
async def stock9():
    results = await miraeAssetStock.get238Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "238",
        "fin_id": "T000000037", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response
################## 증권 END ###############################

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
    results = await heungkuklife.get453Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "453",
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

# NH손해보험
@app.route('/test14', methods=["POST"])
async def test14():
    results = await shinhanLife.get438Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "438",
        "fin_id": "T000000013", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

################## 보험 END ###############################
################## 캐피탈 START #############################

# 신한캐피탈
@app.route('/test15', methods=["POST"])
async def test15():
    results = await shinhanCapitial.get901Data()
    status = 200
    for item in results:
        if 'ERROR' in item:
            status = 500
    
    data_to_return = {
        "status_code": status,  # 응답코드
        "bank_cd": "901",
        "fin_id": "T000000040", # TASK ID 지정
        "result": results     # 응답결과
    }
    
    # Flask의 jsonify를 사용하여 응답 생성
    response = jsonify(data_to_return)
    response.status_code = data_to_return["status_code"]  # status_code 지정
    return response

################## 캐피탈 END ###############################
################## 관리자 업무 START ###############################

# SET HOLIDAY DATA
def set_batch_holiday(hol_date,hoi_yn,hoi_name):
    values = (hol_date, hoi_yn, hoi_name, hol_date, hoi_yn, hoi_name)
    execute_mysql_query_insert("Q18",values) # BATCH LOG 등록

# SET NAVERNEWS DATA
def set_batch_news(press_name,press_img,title,conetent,URL,search_term):
    execute_mysql_query_insert("Q23",(press_name,press_img,title,conetent,URL,search_term)) # BATCH LOG 등록

# SET BATCH LOG
def set_batch_log(batch_id, batch_nm, task_id, task_nm, st_date, ed_date, status, result_data, seq):
    result_data_str = json.dumps(result_data, ensure_ascii=False)
    values = (batch_id, batch_nm, task_id, task_nm, st_date, ed_date, status, result_data_str, seq)
    execute_mysql_query_insert("Q1",values) # BATCH LOG 등록

# SET BATCH 데이터
def set_batch_rst(bank_cd, title, evt_id, startDt, endDt, thumbNail, image, noti, listURL, detailURL):
    values = (bank_cd, title, evt_id, startDt, endDt, thumbNail, image, noti, listURL, detailURL)
    #execute_mysql_query_delete('Q3', []) # BATCH 데이터 전체 삭제
    execute_mysql_query_insert("Q2",values) # BATCH 데이터 등록
    execute_mysql_query_update("Q10",[]) # BATCH 데이터 이벤트 ID 등록

# SET BATCH 데이터 삭제
def del_batch_rst(cnt):
    if cnt == 1:
        execute_mysql_query_delete('Q3', []) # BATCH 데이터 전체 삭제

# SET USER EVENT MAPPING 등록
def set_user_mapp():
    
    results = execute_mysql_query_select("Q15",[])
    if not results:
        logger.debug("No data found from Q15")
    execute_mysql_query_delete('Q16', []) # USER EVENT MAPPING 데이터 초기화
    execute_mysql_query_delete('Q17', ['M']) # # 특정 UNIQUE_ID 데이터 초기화
    for item in results:
        values = [get_next_id("M"), item[0],item[1]]
        execute_mysql_query_insert("Q14",values) # USER EVENT MAPPING 데이터 등록

#####################
# TODO: 아이디 생성시 해당 주석에 사용 이니셜, 사용처 작성
# E: 이벤트 ID
# M : USER, EVENT MAPPING 아이디
#####################
# 고유ID 생성
def get_next_id(letter):
    # 주어진 letter에 해당하는 가장 최신 시퀀스를 조회
    
    last_sequence = execute_mysql_query_select("Q7",[letter])
    for item in last_sequence:
        last_sequence = item[0]
        
    # 기존 시퀀스가 존재하면 1 증가, 아니면 처음부터 시작
    if last_sequence:
        new_sequence = last_sequence + 1
    else:
        new_sequence = 1  # 첫 번째 ID인 경우

    # 생성할 ID 포맷: 영문자 + 9자리 숫자 (예: A000000001)
    new_id = f"{letter}{new_sequence:09d}"
    save_id(letter, new_sequence, new_id) # 고유ID 등록
    return new_id

# 고유ID 등록
def save_id(letter, sequence, new_id):
    values = [letter, sequence, new_id]
    execute_mysql_query_insert("Q8",values) # BATCH 데이터 등록

# 다건 ID 처리리
def get_next_ids(letter, count):
    """ 여러 개의 고유 ID를 생성하고 DB에 저장 """

    # 최신 시퀀스를 조회 (Q7 실행)
    last_sequence = execute_mysql_query_select("Q7", [letter])
    
    # 최신 시퀀스가 있으면 가져오고, 없으면 0으로 시작
    last_sequence = last_sequence[0][0] if last_sequence else 0  # 최신 시퀀스 없으면 0
    
    # 새로운 ID 목록 생성
    new_sequences = list(range(last_sequence + 1, last_sequence + 1 + count))
    new_ids = [f"{letter}{seq:09d}" for seq in new_sequences]

    # 고유 ID들을 한 번에 저장할 값 생성
    values = [(letter, seq, new_id) for seq, new_id in zip(new_sequences, new_ids)]

    # ✅ execute_mysql_query_insert2()를 호출할 때 values를 올바르게 전달 (다건 삽입 처리)
    execute_mysql_query_insert2("Q8", values)

    return new_ids  # 미리 생성한 ID 목록 반환





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

@app.route('/clientLogin', methods=["POST"])
def clientLogin_check():
    data = request.get_json()
    username, password = data.get("id"), data.get("pw")
    results = execute_mysql_query_select("C1", [username, password])
    if not results:
        return [error]

    target = [username, ""] if not results[0][2] else [username]
    execute_mysql_query_update("C2", target)
    return [success]




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

# 관리자 공휴일 관리 화면 호출
@app.route("/etcManage")
def etcManage():
    return render_template("etcManage/etcManage.html", domain=domain, port=port)

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


# 금융사 정보 관리 조회
@app.route("/financeManage", methods=['POST'])
def selectFinace():
    data = request.get_json()
    results = execute_mysql_query_rest("Q9", data)
    return_col_name = ["COR_NO","COR_GP","GP_NM","COR_NM","COR_NOTI","IMG_URL","THUMBNAIL_URL","USE_YN","C_DATE","U_DATE","PRI_IMG"]
    return_result = [dict(zip(return_col_name, data)) for data in results]

    return return_result


# 금융사 정보 추가
@app.route("/insertFinance", methods=['POST'])
def insertFinance():
    data = request.get_json()
    form = (
            data.get("corNoInput",""),
            data.get("corNmInput"),
            data.get("cor_gp"),
            data.get("corNotiInput",""),
            data.get("imgUrlInput",""),
            data.get("thumbUrlInput",""),
            data.get("pri_img",""),
            data.get("corNmInput"),
            data.get("cor_gp"),
            data.get("corNotiInput",""),
            data.get("imgUrlInput",""),
            data.get("thumbUrlInput",""),
            data.get("pri_img","")
            )

    results = execute_mysql_query_insert("Q11", form)
    return [success]


# 금융사 사용여부
@app.route("/changeYnFinance", methods=['POST'])
def changeYnFinance():
    try:
        data = request.get_json()
        form = (
                data.get("change_yn"),
                data.get("finance_no")
                )
        results = execute_mysql_query_insert("Q12", form)
        return [success]
    except:
        return [error]

# 공통 코드 조회 (API 호출)
@app.route('/getCommonCd', methods=["POST"])
def getCommonCdApi():
    data = request.get_json()
    results = execute_mysql_query_select("COMMON_CD", [data.get("gp_id")])
    if not results:
        return [error]

    datas = []
    for item in results:
        data = {
            'RN': item[0],
            'GP_NM': item[1],
            'CD_ID': item[2],
            'CD_NM': item[3],
            'EX_FIELD1': item[4],
            'EX_FIELD2': item[5]
        }
        datas.append(data)
    
    return jsonify(success, datas)

# 공통 코드 조회 (함수 호출)
def getCommonCdFun(gp_id):
    results = execute_mysql_query_select("COMMON_CD", [gp_id])
    if not results:
        return []

    datas = []
    for item in results:
        data = {
            'RN': item[0],
            'GP_NM': item[1],
            'CD_ID': item[2],
            'CD_NM': item[3],
            'EX_FIELD1': item[4],
            'EX_FIELD2': item[5]
        }
        datas.append(data)
    return datas
    

################## 관리자 업무 END ###############################
################## 파일 관리 START ###############################
########################
# 파일 업로드 / 다운로드 #
########################
# 업로드/다운로드 폴더 경로
UPLOAD_FOLDER = config['FILE']['UPLOAD_PATH']
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# 업로드 폴더 지정
app.config['FILE_FOLDER'] = UPLOAD_FOLDER
# 허용할 이미지 확장자
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'}
# 파일 크기 제한 (10MB)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

# 파일 목록 가져오기
@app.route('/files', methods=['GET'])
def list_files():
    results = execute_mysql_query_select("Q6",[])
    datas = []
    for item in results:
        data = {
            'file_name': item[0],
            'org_file_name': item[1],
            'file_extension': item[2],
            'file_path': item[3]
        }
        datas.append(data)
    
    # 파일업로드 경로에서 직접 목록 가져오기
    #files = os.listdir(app.config['FILE_FOLDER'])
    return jsonify(datas)

# 파일 다운로드
@app.route('/fileDownload', methods=['POST'])
def download_file():
    # 클라이언트가 보낸 데이터에서 파일 경로 및 다운로드 경로 가져오기
    file_name = request.form.get('file_name', default='', type=str)
    file_path = os.path.join(app.config['FILE_FOLDER'], file_name)
    
    # 클라이언트에게 파일 다운로드 제안
    response = send_file(file_path, as_attachment=True)

    return response

# 파일 업로드
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "파일이 없습니다."}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "파일명이 비어 있습니다."}), 400

        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()  # 확장자 추출
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = uuid.uuid4().hex[:12]  # 12자리 UUID
            filename = f"{now}_{unique_id}.{ext}" 

            file_path = os.path.join(app.config['FILE_FOLDER'], filename)
            file.save(file_path)  # 파일 저장
            
            # DB 파일 등록 처리
            values = (filename, file.filename, ext,  os.path.join(app.config['FILE_FOLDER']))
            execute_mysql_query_insert("Q4",values)
            
            return jsonify({"message": "파일 업로드 성공", "filename": filename, "original_name": file.filename}), 200
        else:
            return jsonify({"error": "허용되지 않은 파일 형식입니다."}), 400

    except Exception as e:
        # 예외 발생 시 에러 메시지 출력
        return jsonify({"error": f"파일 업로드 중 오류가 발생했습니다: {str(e)}"}), 50
# 파일 멀티 업로드
@app.route('/multiUpload', methods=['POST'])
def multiUpload():
    try:
        files = request.files.getlist('file')
        print(files)
        if not files or len(files) == 0:
            return jsonify({"error": "파일이 없습니다."}), 400

        results = []
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        for file in files:
            if file.filename == '':
                continue  # 빈 파일은 건너뜁니다.
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                unique_id = uuid.uuid4().hex[:12]
                filename = f"{now}_{unique_id}.{ext}"
                file_path = os.path.join(app.config['FILE_FOLDER'], filename)
                file.save(file_path)
                # DB 등록 처리 예시
                values = (filename, file.filename, ext, os.path.join(app.config['FILE_FOLDER']))
                execute_mysql_query_insert("Q4", values)
                results.append({
                    "filename": filename,
                    "original_name": file.filename
                })
            else:
                return jsonify({"error": f"허용되지 않은 파일 형식입니다: {file.filename}"}), 400

        return jsonify({"message": "파일 업로드 성공", "files": results}), 200

    except Exception as e:
        return jsonify({"error": f"파일 업로드 중 오류가 발생했습니다: {str(e)}"}), 500

# 파일 확장자 검증
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 파일 삭제
@app.route('/deleteFile', methods=['POST'])
def delete_file():
    try:
        # 클라이언트로부터 삭제할 파일 이름을 받음
        file_name = request.form.get('file_name', default='', type=str)
        
        if not file_name:
            return jsonify({"error": "삭제할 파일 이름이 필요합니다."}), 400
        
        file_path = os.path.join(app.config['FILE_FOLDER'], file_name)
        
        # 파일이 존재하는지 확인
        if not os.path.exists(file_path):
            return jsonify({"error": "파일이 존재하지 않습니다."}), 404
        
        # 파일 삭제
        os.remove(file_path)
        
        # DB 파일 삭제 처리
        try:
            execute_mysql_query_delete('Q5', [file_name])
        except Exception as e:
            print(e)

        return jsonify({"message": f"파일 '{file_name}' 삭제 성공"}), 200

    except Exception as e:
        return jsonify({"error": f"파일 삭제 중 오류가 발생했습니다: {str(e)}"}), 500

# 이미지 미리보기를 하기위한 파일 서빙 처리용
@app.route('/resources/<path:filename>')
def get_resource_file(filename):
    return send_from_directory(app.config['FILE_FOLDER'], filename)

# 파일관리 샘플 화면
@app.route("/uploadTest")
def uploadTest():
    return render_template("common/uploadTest.html", domain=domain, port=port)    
################## 파일 관리 END ###############################
################## 배치 관리 START ###############################
# 배치관리 화면
@app.route("/batchControl")
def batchControl():
    return render_template("common/batchControl.html", domain=domain, port=port)    

# 배치 시작
@app.route('/batchStart', methods=["POST"])
def batchStart():
    datas = request.get_json()
    result = start_batch(datas['type'])
    logger.info(str(result))
    return result

# 배치 종료
@app.route('/batchStop', methods=["POST"])
def batchStop():
    datas = request.get_json()
    result = stop_batch(datas['type'])
    logger.info(str(result))
    return result

# 배치 상태 조회
@app.route('/batchStatus', methods=["POST"])
def batchStatus():
    datas = request.get_json()
    result = check_batch_status(datas['type'])
    logger.info(str(result))
    return result

# 배치 결과 통계 조회    
@app.route('/batchResultSearch', methods=["POST"])
def batchResultSearch():
    results = execute_mysql_query_select("Q19", [])
    datas = []
    for item in results:
        data = {
            'batch_id': item[0],
            'batch_nm': item[1],
            'task_nm': item[2],
            'st_date': item[3],
            'ed_date': item[4],
            'status': item[5],
            'tot_cnt': item[6],
            'success_cnt': item[7],
            'fail_cnt': item[8],
            'result_data': item[9],
            'row_num': item[10]
        }
        datas.append(data)
    return jsonify(datas)


################## 배치 관리 END ###############################
############## 관리자 START ############################
@app.route('/batchDataList', methods=["POST"])
def batchDataList():

    corNm = request.form.get('corNm', default='', type=str)
    corSub = request.form.get('corSub', default='', type=str)
    useYn = request.form.get('useYn', default='', type=str)

    values = [corNm, corSub, useYn]

    try:
        results = execute_mysql_query_rest("A1", values)

        # if not results:
        #     return jsonify({"message": "No data found"}), 404  # 데이터가 없을 경우 404 응답

        # print("DB Query Result:", results)  # 서버 로그 출력
        # return jsonify(results)  # JSON 형식으로 응답
    
        datas = []
        for item in results:
            data = {
                'cor_no': item[0],
                'cor_nm': item[1],
                'evt_title': item[2],
                'evt_id': item[3],
                'evt_status': item[4],
                'evt_st_date': item[5],
                'evt_ed_date': item[6],
                'evt_thumbnail': item[7],
                'evt_img': item[8],
                'evt_noti': item[9],
                'evt_list_link': item[10],
                'evt_dt_link': item[11],
            }
            datas.append(data)
        
        return jsonify(datas)

    except Exception as e:
        print(f"Error: {e}")  # 에러 로그 출력
        return jsonify({"error": str(e)}), 500  # 500 Internal Server Error 응답
    
@app.route('/evtDataList', methods=["POST"])
def evtDataList():

    corNm = request.form.get('corNm', default='', type=str)
    corSub = request.form.get('corSub', default='', type=str)
    useYn = request.form.get('useYn', default='', type=str)

    values = [corNm, corSub, useYn]

    try:
        results = execute_mysql_query_rest("A5", values)

        # if not results:
        #     return jsonify({"message": "No data found"}), 404  # 데이터가 없을 경우 404 응답

        # print("DB Query Result:", results)  # 서버 로그 출력
        # return jsonify(results)  # JSON 형식으로 응답
    
        datas = []
        for item in results:
            data = {
                'cor_no': item[0],
                'cor_nm': item[1],
                'evt_title': item[2],
                'evt_id': item[3],
                'evt_st_date': item[4],
                'evt_ed_date': item[5],
                'evt_thumbnail': item[6],
                'evt_img': item[7],
                'evt_noti': item[8],
                'evt_list_link': item[9],
                'evt_dt_link': item[10],
                'use_yn': item[11],
                'c_date': item[12]
            }
            datas.append(data)
        
        return jsonify(datas)

    except Exception as e:
        print(f"Error: {e}")  # 에러 로그 출력
        return jsonify({"error": str(e)}), 500  # 500 Internal Server Error 응답

@app.route('/insertEvent', methods=["POST"])
def insertEvent():
    try:
        # FormData에서 "datas" 키 가져오기
        event_data_str = request.form.get("datas")  # str 타입 반환
        event_data = json.loads(event_data_str)  # 문자열을 리스트로 변환

        # Bulk Insert와 Bulk Update용 데이터 리스트
        bulk_values = []  # Bulk Insert용 데이터 리스트
        bulk_update_values = []  # Bulk Update용 데이터 리스트

        # evtId 목록 생성 (이 부분 수정)
        evtIds = get_next_ids('E', len(event_data))  # 여러 개의 evtId를 생성
        
        if len(evtIds) != len(event_data):
            return jsonify({"error": "evtId 생성 실패, 데이터 수와 일치하지 않음"}), 400

        # 각 이벤트 데이터 처리
        for idx, v in enumerate(event_data):
            if v == "":
                continue  # 빈 데이터는 건너뜀

            event_dict = v
            evtId = evtIds[idx]  # 생성된 evtId를 리스트에서 가져옴
            # 각 이벤트 데이터에 대한 값 구성
            values = (
                event_dict["cor_no"],
                event_dict["evt_title"],
                evtId,
                None if event_dict["evt_st_date"] == "" else event_dict["evt_st_date"],
                None if event_dict["evt_ed_date"] == "" else event_dict["evt_ed_date"],
                event_dict["evt_thumbnail"],
                event_dict["evt_img"],
                event_dict["evt_noti"],
                event_dict["evt_list_link"],
                event_dict["evt_dt_link"]
            )

            bulk_values.append(values)  # Bulk Insert 리스트에 추가
            bulk_update_values.append((evtId, event_dict["cor_no"], event_dict["evt_title"]))  # Bulk Update용 리스트 추가

        # 🔥 Bulk Insert 실행
        if bulk_values:
            execute_mysql_query_insert_update_bulk("A2", bulk_values, "A3", bulk_update_values)
        
        return jsonify({"message": "Bulk Data Inserted", "count": len(bulk_values)})

    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        return jsonify({"error": str(e)}), 500


    

@app.route('/updateEventUseYn', methods=["POST"])
def updateEventUseYn():

    try:
        # FormData에서 "datas" 키 가져오기
        event_data = request.form.get("datas")

        if not event_data:
            return jsonify({"error": "No data received"}), 400

        # JSON 문자열을 파이썬 딕셔너리로 변환
        event_dict = json.loads(event_data)
        
        values = [event_dict["change_yn"],event_dict["evt_id"]]

        execute_mysql_query_update("A4",values) # 이벤트 노출여부 업데이트(EVT_MST)

        return jsonify({"message": "Data UPDATE", "data": event_dict})

    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        return jsonify({"error": str(e)}), 500
@app.route('/updateEventDetail', methods=["POST"])
def updateEventDetail():

    try:
        # FormData에서 "datas" 키 가져오기
        event_data = request.form.get("datas")

        if not event_data:
            return jsonify({"error": "No data received"}), 400

        # JSON 문자열을 파이썬 딕셔너리로 변환
        event_dict = json.loads(event_data)

        values = [event_dict["startDt"],event_dict["endDt"],event_dict["thumbUrl"],event_dict["imgUrl"],event_dict["evtNoti"],event_dict["evtListLink"],event_dict["evtDtLink"],event_dict["evtId"]]

        execute_mysql_query_update("A6",values) # 이벤트 노출여부 업데이트(EVT_MST)

        return jsonify({"message": "Data UPDATE", "data": event_dict})

    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        return jsonify({"error": str(e)}), 500
@app.route('/delEvent', methods=["POST"])
def delEvent():

    try:
        # FormData에서 "datas" 키 가져오기
        event_data = request.form.get("datas")

        if not event_data:
            return jsonify({"error": "No data received"}), 400

        # JSON 문자열을 파이썬 딕셔너리로 변환
        event_dict = json.loads(event_data)

        values = [event_dict["evt_id"]]

        execute_mysql_query_delete("A7",values) # 이벤트 노출여부 업데이트(EVT_MST)
        
        updValues = ['',event_dict["cor_no"],event_dict["evt_title"]]
        execute_mysql_query_update("A3",updValues) # 이벤트 아이디 '' 로 업데이트(BATCH_RST)
        
        return jsonify({"message": "Data delete", "data": event_dict})

    except Exception as e:
        logger.error("에러 발생: %s", str(e))
        return jsonify({"error": str(e)}), 500

################## 관리자 END ############################
@app.route('/getEventMst', methods=["POST"])
def getEventMst():
    data = request.get_json()  # 전송된 JSON 데이터 받아오기
    id = data.get("id")
    #start = data.get("start")
    #end = data.get("end")
    values = [id, id, id, id]
    results = execute_mysql_query_select("Q13", values)
    #results = execute_mysql_query_select("Q13", [])

    datas = []
    for item in results:
        data = {
            'cor_no': item[0],
            'cor_nm': item[1],
            'evt_title': item[2],
            'evt_st_dt': item[3],
            'evt_ed_dt': item[4],
            'evt_thumbnail': item[5],
            'evt_list_link': item[6],
            'evt_dt_link': item[7],
            'cor_color': item[8],
            'cor_group': item[9],
            'cor_pri_img_url': item[10]
        }
        datas.append(data)

    return jsonify(datas)

@app.route('/getIPOStock', methods=["POST"])
def getIPOStock():
    data = request.get_json()  # 전송된 JSON 데이터 받아오기
    id = data.get("id")
    #start = data.get("start")
    #end = data.get("end")
    results = execute_mysql_query_select("Q31", [])

    datas = []
    for item in results:
        data = {
            'stock_nm': item[0],
            'sub_st_dt': item[1],
            'sub_ed_date': item[2],
            'con_pub_off_price': item[3],
            'hope_pub_off_price': item[4],
            'sub_com_rate': item[5],
            'chief_editor': item[6],
            'c_dt': item[7]
        }
        datas.append(data)

    return jsonify(datas)

#공휴일 API
@app.route('/getHoiDay', methods=["POST"])
def getHoiDay():
    results = execute_mysql_query_select("Q20", [])

    datas = []
    for item in results:
        data = {
            'hoi_date': item[0],
            'hoi_name': item[1]
        }
        datas.append(data)

    return jsonify(datas)

#뉴스 기사 API
@app.route('/getNews', methods=["POST"])
def getNews():
    results = execute_mysql_query_select("Q26", [])

    datas = []
    return_col_name = ["title","press_nm","press_img","content","link","cor_gp"]
    return_result = [dict(zip(return_col_name, data)) for data in results]

    return return_result

#유튜브 API
@app.route('/getYoutube', methods=["POST"])
def getYoutube():
    results = execute_mysql_query_select("Q28", [])

    datas = []
    return_col_name = ["cor_gp","content_title","content_url"]
    return_result = [dict(zip(return_col_name, data)) for data in results]

    return return_result


@app.route('/getSetting', methods=["POST"])
def getSetting():
    data = request.get_json()  # 전송된 JSON 데이터 받아오기
    results = execute_mysql_query_select("C3", [data.get("id"),data.get("id")])

    datas = []
    for item in results:
        data = {
            'cor_no': item[0],
            'cor_nm': item[1],
            'evt_title': item[2],
            'evt_id': item[3],
            'cor_gp': item[4],
            'group_yn': item[5],
            'evt_user_yn': item[6]
        }
        datas.append(data)

    return jsonify(datas)

@app.route('/updateSetting', methods=["POST"])
def updateSetting():
    data = request.get_json()  # 전송된 JSON 데이터 받아오기
    execute_mysql_query_delete("C4", [data.get("id")])
    results = execute_mysql_query_insert("C5", [data.get("id"),data.get("cor_no"),data.get("evt_no")])

    return [success]

################## YOUTUBE START #############################
# 금융사 유튜브 정보 가져오기
@app.route('/getYouTube', methods=["POST"])
async def getYouTube():
    youtube_key = config['SERVER']['youtube_key']
    channels = ["신한은행", "우리은행", "국민은행", "하나은행", "NH농협은행"]
    channel_ids = ["UC4E394G9WuS9y6SlBZslMsQ", "UCcQ9V6nEYVMSRWWOrvHQqLg", "UCHq8auIJ8ewo7iD2pqX22UA", "UCSHbm2TrspNZ_p_yd39kMNg", "UCmkkFJIalgnWovxFigYK2EA"]
    #test = getCommonCdFun("YOUTUBE_ID")
    results = []
    for channel in channel_ids:
        #result_id = await getChannelId(youtube_key, channel)  # 채널 ID 취득
        data = await getChannelData(youtube_key, channel)  # 비동기 함수 실행
        results.append(data)
    return jsonify({"success": True, "results": results, "corNm": channels})  # JSON 응답

# @app.route('/getYouTube', methods=["POST"])
# def getYouTube():
#     youtube_key = config['SERVER']['youtube_key']
#     results = getData(youtube_key)  # 비동기 함수 실행
#     print("#"*100)
#     print(results)
#     print("#"*100)
#     return jsonify({"success": True, "results": results, "corNm": channels})  # JSON 응답

# YOUTUBE BATCH 결과 등록
def set_batch_youtube(corNo, contentTitle, contentUrl, thumbnailUrl, priority):
    values = (corNo, contentTitle, contentUrl, thumbnailUrl, priority)
    execute_mysql_query_insert("Q24",values) # YOUTUBE BATCH 결과 등록

 # YOUTUBE BATCH 데이터 전체 삭제
def del_batch_youtube(cnt):
    if cnt == 0:
        execute_mysql_query_delete('Q25', []) # YOUTUBE BATCH 데이터 전체 삭제

################## YOUTUBE END #############################

# 공모주 정보 가져오기기
@app.route('/getPubOffStockData', methods=["POST"])
async def getPubOffStockData():
    try:
        # pubOffStock() 호출
        response = await pubOffStock()  # Response 객체 반환
        return response
    except Exception as e:
        # 오류 처리
        return jsonify({"success": False, "error": str(e)})



# SET NAVERNEWS DATA
def set_batch_pubOffStock(stock_nm,st_date,ed_date,con_pub_off_price,hope_pub_off_price,sub_com_rate, chief_deitor):
    execute_mysql_query_insert("Q30",(stock_nm,st_date,ed_date,con_pub_off_price,hope_pub_off_price,sub_com_rate, chief_deitor)) # BATCH LOG 등록

if __name__ == "__main__":
    while True:
        try:
            if real_yn == "Y":  # 운영 서버 여부
                # SSL 인증서 및 키 파일 경로
                # restart_rasa()
                #socketio.run(app, host=server_host, port=port, ssl_context=(ssl_cert, ssl_key), allow_unsafe_werkzeug=True)
                app.run(host=server_host, port=port, debug=True)    
            else:
                # 앱 실행
                # socketio.run(app)
                app.run(host='0.0.0.0', port=port, debug=True)
        except Exception as e:
            logging.error(f"Server Error: {e}")
        time.sleep(5)  # 서버가 중단되었을 경우 5초 후 재시작 시도

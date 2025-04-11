# snsLogin.py

import requests
import urllib.parse
from dbconn import execute_mysql_query_select, execute_mysql_query_insert, execute_mysql_query_delete, execute_mysql_query_update, execute_mysql_query_rest, execute_mysql_query_update2,execute_mysql_query_insert_update_bulk, execute_mysql_query_insert2, execute_multi_update
from flask import redirect, session, request
from datetime import datetime, timedelta
from util.session_manage import set_login_session

import os
import configparser
import secrets
import uuid
import jwt

# 서버 경로 취득
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, ".."))  # 한 단계 위로 올라감

# 환경 설정에 따라 ini 파일 선택
environment = os.getenv('ENVIRONMENT', 'development')

if environment == 'production':
    config_path = os.path.join(base_dir, 'config.ini')
else:
    config_path = os.path.join(base_dir, 'config_development.ini')

# config 읽기
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

success = config['CODE']['success']
domain = config['SERVER']['domain']
# 네이버 앱 등록 정보
naver_client_id = config['NAVER']['client_id']
naver_client_secret = config['NAVER']['client_secret']
naver_auth_host = config['NAVER']['auth_host']
naver_api_host = config['NAVER']['api_host']
# 카카오 앱 등록 정보
kakao_client_id = config['KAKAO']['client_id']
kakao_client_secret = config['KAKAO']['client_secret']
kakao_auth_host = config['KAKAO']['auth_host']
kakao_api_host = config['KAKAO']['api_host']
#### 네이버 시작 ####
def naverLogin():
    
    state = secrets.token_urlsafe(16)  # CSRF 방지용 임의값
    naver_redirect_uri = domain+'/naverCallback'
    naver_auth_url = (
        f"{naver_auth_host}/authorize?"
        f"response_type=code&client_id={naver_client_id}"
        f"&redirect_uri={urllib.parse.quote(naver_redirect_uri)}"
        f"&state={state}"
    )
    return redirect(naver_auth_url)

def naverCallback():
    
    code = request.args.get("code")
    state = request.args.get("state")

    # 1. 액세스 토큰 요청
    token_url = f"{naver_auth_host}/token"
    token_params = {
        "grant_type": "authorization_code",
        "client_id": naver_client_id,
        "client_secret": naver_client_secret,
        "code": code,
        "state": state
    }

    token_res = requests.get(token_url, params=token_params).json()
    
    access_token = token_res.get("access_token")
    refresh_token = token_res.get("refresh_token")
    # expires_in은 문자열로 들어오니까 int로 변환
    expires_in = int(token_res.get("expires_in"))  
    issued_at = datetime.now()
    # 60초 버퍼 줌(토큰발행시점 dbinsert 시점 차이로)
    access_token_expire = issued_at + timedelta(seconds=int(expires_in) - 60)
    # 1년 = 365일
    refresh_token_expire = issued_at + timedelta(days=365)

    # 2. 사용자 프로필 요청
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_res = requests.get(f"{naver_api_host}/me", headers=headers).json()
    profile = profile_res["response"]
    
    sns_id = profile["id"]
    name = profile.get("name", "")

    if not sns_id :
        # TODO::: 회원연동실패 처리 필요 
        return f"회원연동 실패"

    # 3. 사용자 존재 여부 확인
    snsVal = (sns_id, 'NAVER')
    user = execute_mysql_query_select("C7",snsVal)
    for item in user:
        userId = item[0]  
        useYn = item[1]

    # 4. 없으면 INSERT (추후 의사 물어보는 단계 필요)
    if not user:
        userId = generate_user_id()
        values = (userId,'',name,'','','','','Y',sns_id,'NAVER')
        execute_mysql_query_insert("C6",values)
        # Insert client_auth
        authValues = (userId,'NAVER',sns_id,access_token,access_token_expire,refresh_token,refresh_token_expire)
        execute_mysql_query_insert("C10",authValues)
        
    # 4-1. 있으면
    else :
        # userId = userId
        # 연동해제 후 재연동 시 처리
        update_items = []
        if useYn == 'N':
            update_items.append(("C14", ('Y', sns_id, 'NAVER')))
            update_items.append(("C12", ('Y', access_token, access_token_expire, refresh_token, refresh_token_expire, sns_id, 'NAVER')))

        # 마지막 로그인일시 갱신 (조건 상관없이 항상 추가)
        update_items.append(("C8", (sns_id, 'NAVER')))
        update_items.append(("C11", (sns_id, 'NAVER')))

        # 최종 업데이트 실행
        execute_multi_update(update_items)
    
    # 5.세션처리
    set_login_session(userId, 'NAVER')

    return [00000]

# 네이버 연동해제 
def naverDisconnect(userId) :
    
    userId = userId
    result = execute_mysql_query_select("C13",[userId])
    item = result[0]
    refresh_token = item[12]
    sns_id = item[6]
    # 네이버 연동해제시 refresh_token 으로 access_token 갱신 필요
    # access token 갱신
    # {naver_auth_host}/token?grant_type=refresh_token&client_id=CLIENT_ID&client_secret=CLIENT_SECRET&refresh_token=REFRESH_TOKEN
    token_url = f"{naver_auth_host}/token"
    refresh_token_params = {
        "grant_type": "refresh_token",
        "client_id": naver_client_id,
        "client_secret": naver_client_secret,
        "refresh_token": refresh_token
    }    
    refresh_token_res = requests.get(token_url, params=refresh_token_params).json()
    access_token = refresh_token_res.get("access_token")
    # 연동해제
    # {naver_auth_host}/token?grant_type=delete&client_id=ugZD9QSKdWFTAls9nqfF&client_secret=hj6cr1Ypf5&access_token=AAAANVp7taKfZSlTXvQsLscm_GKF7jcyINeTCW0bff78Ro1EZmCrlJbCgebTkfKxyAbdzBdGSaJ9jQWHyk_oA4cvIUo
    delete_token_params = {
        "grant_type": "delete",
        "client_id": naver_client_id,
        "client_secret": naver_client_secret,
        "service_provider":'NAVER',
        "access_token": access_token             # 
    }    

    del_token_res = requests.get(token_url, params=delete_token_params).json()
    
    update_items = []
    update_items.append(("C14", ('N', sns_id, 'NAVER')))
    update_items.append(("C12", ('N', '', None,'',None, sns_id, 'NAVER')))
    
    execute_multi_update(update_items)
    
    return [success]
#### 네이버 종료 ####
#### 카카오 시작 ####
def kakaoLogin():
    
    state = secrets.token_urlsafe(16)  # CSRF 방지용 임의값
    kakao_redirect_uri = domain+'/kakaoCallback'
    kakao_auth_url = (
        f"{kakao_auth_host}/oauth/authorize?"
        f"response_type=code&client_id={kakao_client_id}"
        f"&redirect_uri={urllib.parse.quote(kakao_redirect_uri)}"
        f"&state={state}"
    )
    return redirect(kakao_auth_url)

def kakaoCallback():
    code = request.args.get("code")
    state = request.args.get("state")

    # 1. 액세스 토큰 요청
    token_url = f"{kakao_auth_host}/oauth/token"
    token_params = {
        "grant_type": "authorization_code",
        "client_id": kakao_client_id,
        "client_secret": kakao_client_secret,
        "code": code,
        "state": state
    }

    token_res = requests.get(token_url, params=token_params).json()
    access_token = token_res.get("access_token")
    refresh_token = token_res.get("refresh_token")
    issued_at = datetime.now()
    # 60초 버퍼 줌(토큰발행시점 dbinsert 시점 차이로)
    expires_in = token_res.get("expires_in")
    refresh_token_expires_in = token_res.get("refresh_token_expires_in")
    access_token_expire = issued_at + timedelta(seconds=int(expires_in) - 60)
    refresh_token_expire = issued_at + timedelta(seconds=refresh_token_expires_in)

    id_token = token_res.get("id_token")
    # TODO ::: 공개키로 서명 검증 -카카오의 공개키 JWKS(JSON Web Key Set) 엔드포인트를 사용
    # https://kauth.kakao.com/.well-known/jwks.json
    payload = jwt.decode(id_token, options={"verify_signature": False})

    sns_id = payload["sub"]
    # email = profile["email"]
    name = payload.get("nickname", "")

    if not sns_id :
        # TODO::: 회원연동실패 처리 필요 
        return f"회원연동 실패"

    # 3. 사용자 존재 여부 확인
    snsVal = (sns_id, 'KAKAO')
    user = execute_mysql_query_select("C7",snsVal)
    for item in user:
        userId = item[0]  

    # # 4. 없으면 INSERT (추후 의사 물어보는 단계 필요?)
    if not user:
        userId = generate_user_id()
        values = (userId,'',name,'','','','','Y',sns_id,'KAKAO')
        execute_mysql_query_insert("C6",values)
        # Insert client_auth
        authValues = (userId,'KAKAO',sns_id,access_token,access_token_expire,refresh_token,refresh_token_expire)
        execute_mysql_query_insert("C10",authValues)
        
    # # 4-1. 있으면 마지막 LOGIN 업데이트
    else :
        values = (sns_id ,'KAKAO')
        execute_mysql_query_update("C8",values)
        execute_mysql_query_update("C11",values)
    
    # # 5.세션처리
    set_login_session(userId, 'KAKAO')

    return [00000]

def kakaoDisconnect(userId):
    userId
    return
#### 카카오 종료 ####
def generate_user_id():
    return f"user_{uuid.uuid4().hex[:12]}"
# snsLogin.py

import requests
import urllib.parse
from dbconn import execute_mysql_query_select, execute_mysql_query_insert, execute_mysql_query_delete, execute_mysql_query_update, execute_mysql_query_rest, execute_mysql_query_update2,execute_mysql_query_insert_update_bulk, execute_mysql_query_insert2
from flask import redirect, session, request

import secrets

# 네이버 앱 등록 정보 (TODO::: CONFIG 등록필요 )
NAVER_CLIENT_ID = 'ugZD9QSKdWFTAls9nqfF'
NAVER_CLIENT_SECRET = 'hj6cr1Ypf5'
NAVER_REDIRECT_URI = 'http://127.0.0.1:8082/naverCallback'

def naverLogin():
    
    state = secrets.token_urlsafe(16)  # CSRF 방지용 임의값
    # session['state'] = state

    naver_auth_url = (
        "https://nid.naver.com/oauth2.0/authorize?"
        f"response_type=code&client_id={NAVER_CLIENT_ID}"
        f"&redirect_uri={urllib.parse.quote(NAVER_REDIRECT_URI)}"
        f"&state={state}"
    )
    return redirect(naver_auth_url)

def naverCallback():
    
    code = request.args.get("code")
    state = request.args.get("state")

    # 1. 액세스 토큰 요청
    token_url = "https://nid.naver.com/oauth2.0/token"
    token_params = {
        "grant_type": "authorization_code",
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "code": code,
        "state": state
    }

    token_res = requests.get(token_url, params=token_params).json()
    print('token_res')
    print(token_res)
    #{'access_token': 'AAAANVp7taKfZSlTXvQsLscm_GKF7jcyINeTCW0bff78Ro1EZmCrlJbCgebTkfKxyAbdzBdGSaJ9jQWHyk_oA4cvIUo', 'refresh_token': 'bGtot0zONwcwMu5T5aYvWSgzEtipqLFCuphf7xPLxXQymWHmnwBJVk56DvgqPpoj16tL82jipka0isn8NcwIb6Lcb7A6TDAAPuWAKRc6sW4zxAie', 'token_type': 'bearer', 'expires_in': '3600'}
    access_token = token_res.get("access_token")

    # 2. 사용자 프로필 요청
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_res = requests.get("https://openapi.naver.com/v1/nid/me", headers=headers).json()
    profile = profile_res["response"]
    print('profile')
    print(profile)
    #{'id': 'hD74cIF8ntZQ00SvvExlLmEEJVyAM1Pq6JheV__o3mE', 'email': 'crzzzz@naver.com', 'name': '김초록'}
    sns_id = profile["id"]
    email = profile["email"]
    name = profile.get("name", "")

    if not email :
        # TODO::: 회원연동실패 처리 필요 
        return f"회원연동 실패"

    # 3. 사용자 존재 여부 확인
    snsVal = (sns_id, 'NAVER')
    user = execute_mysql_query_select("C7",snsVal)

    # 4. 없으면 INSERT (의사 물어보는 단계 필요?)
    if not user:
        values = (email,'',name,'','','','','Y',sns_id,'NAVER')
        execute_mysql_query_insert("C6",values)

    # 4-1. 있으면 마지막 LOGIN 업데이트
    else :
        values = (sns_id ,'NAVER')
        execute_mysql_query_update("C8",values)
    
    # TODO:::  5.세션처리

    return redirect("http://127.0.0.1:8081/main")

def naverDisconnect() :

    # 회원 가입 시 access_token / refresh_token 저장 필요 
    # TODO::: 기존 client_user 컬럼 추가 할지 별도의 테이블을 가져가야 하는지 결정 필요 고민 중
    # 
    # 네이버 연동해제시 refresh_token 으로 access_token 갱신 필요
    # access token 갱신
    # https://nid.naver.com/oauth2.0/token?grant_type=refresh_token&client_id=CLIENT_ID&client_secret=CLIENT_SECRET&refresh_token=REFRESH_TOKEN
    token_url = "https://nid.naver.com/oauth2.0/token"
    refresh_token_params = {
        "grant_type": "refresh_token",
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "refresh_token": ''             # 
    }    
    refresh_token_res = requests.get(token_url, params=refresh_token_params).json()
    print('refresh_token_res')
    print(refresh_token_res)
    # 연동해제
    # https://nid.naver.com/oauth2.0/token?grant_type=delete&client_id=ugZD9QSKdWFTAls9nqfF&client_secret=hj6cr1Ypf5&access_token=AAAANVp7taKfZSlTXvQsLscm_GKF7jcyINeTCW0bff78Ro1EZmCrlJbCgebTkfKxyAbdzBdGSaJ9jQWHyk_oA4cvIUo
    delete_token_params = {
        "grant_type": "delete",
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "service_provider":'NAVER',
        "access_token": ''             # 
    }    

    del_token_res = requests.get(token_url, params=delete_token_params).json()
    print('del_token_res')
    print(del_token_res)

    # TODO::: DB작업 CLIENT_USER USE_YN 변경 
    return f"회원연동 해제"
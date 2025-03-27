# snsLogin.py

import requests
import urllib.parse
from dbconn import execute_mysql_query_select, execute_mysql_query_insert, execute_mysql_query_delete, execute_mysql_query_update, execute_mysql_query_rest, execute_mysql_query_update2,execute_mysql_query_insert_update_bulk, execute_mysql_query_insert2
from flask import redirect, session, request

import secrets

# 네이버 앱 등록 정보
NAVER_CLIENT_ID = 'ugZD9QSKdWFTAls9nqfF'
NAVER_CLIENT_SECRET = 'hj6cr1Ypf5'
NAVER_REDIRECT_URI = 'http://127.0.0.1:8082/naverCallback'

def naverLogin():
    """네이버 로그인 URL 생성 → 네이버 로그인 페이지로 redirect"""
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
    """네이버 콜백 처리 → 사용자 정보 받아와서 DB 처리"""
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
    access_token = token_res.get("access_token")

    # 2. 사용자 프로필 요청
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_res = requests.get("https://openapi.naver.com/v1/nid/me", headers=headers).json()
    profile = profile_res["response"]

    sns_id = profile["id"]
    email = profile["email"]
    name = profile.get("name", "")

    if not email :
        return f"회원연동 실패"

    # 3. 사용자 존재 여부 확인
    snsVal = (sns_id, 'NAVER')
    user = execute_mysql_query_select("C7",snsVal)

    # 4. 없으면 INSERT
    if not user:
        values = (email,'',name,'','','','','Y',sns_id,'NAVER')
        execute_mysql_query_insert("C6",values)

    # 4-1. 있으면 마지막 LOGIN 업데이트
    else :
        values = (sns_id ,'NAVER')
        execute_mysql_query_update("C8",values)
    
    # 세션처리

    return redirect("http://127.0.0.1:8081/main")

from flask import session
from datetime import datetime
from util import makeJwt

# 공통 로그인 세션 설정 함수
# param user_id: 내부 사용자 ID
# param auth_type: 로그인 방식 ('PASSWORD', 'NAVER', 'KAKAO', 'GOOGLE' 등)
def set_login_session(user_id, auth_type='PASSWORD'):
    print(makeJwt.__file__)
    session.permanent = True
    session['userId'] = user_id
    session['authType'] = auth_type.upper()
    session['token'] = makeJwt.create_jwt_token(user_id)
    session['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def clear_session():
    # 로그아웃 시 세션 초기화
    session.clear()

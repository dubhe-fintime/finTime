import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 키움증권
# 금융사코드 : 264
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : X 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
# 썸네일 다운로드 URL
##############################

##############################
# Service URL = "https://www1.kiwoom.com/e/common/event/SIngEventListAjax"
# Method = POST
# 양식데이터라 header
##############################

async def get264Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://www1.kiwoom.com/e/common/event/SIngEventListAjax"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 목록 URL 
    list_domain =  "https://www1.kiwoom.com/h/customer/event/VIngEventView"
    # 이미지 URL 
    img_url =  "https://www.samsungpop.com/common.do?cmd=down&amp;saveKey=event.file&amp;fileName="
    # 이미지 URL 
    detail_domain =  "https://www1.kiwoom.com/h/common/event/VEventMainView?eventCode="
    ######### 기초 설정 END ##############

    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "gds_tp": "",  
            "mdia_tp": "H",
            "_reqAgent": "ajax",
            "LK5Hew": "48a0dadfbfd48787971c038c72b7e0bdefbaa2044d45499f58ccecab754543fc5318c2ab9d36a3ca6725c9d8f83882031d64502f3394fa96aabd75f5d878837545ca74d67c5242264ada7990a196fb3f19f14deab0c37eb551ef9dcc90b2eeb38f02d44650a7fd1db2b8782647be476f3c5b230bed656099614a997a0587634b7682fd77fe2f204801f6e4eb3cda840299644b444c9c502d51bf751d31d158f09125f20957582c4dcc67a6bd3822a6231e9e202b36e059c3b0ba1783d165d1317de136988f4071f95677523e4ee91c8834eb79973025b455f48552317e545e81be3277217d35b554fca6c6ad63b399ab246396f289a33496673490147b13351a64688868f85f87c09d76aae174c2f9f36e0807f60250ae1e60bfeb0eb7fd89090393aa9bbbaac960d5bfc8f8d865704645630c867157a2203b972995f3eeb1e474ad5f4fee57233c77e8aad99637d91ffad94bbe195d8e4f9224f2859224e837c8bbc50d302b76fe1253c11c214f9c52351b7e2257a8c3d6b64f3f0ceb2f1147",
            "Rfb86Os1z": "N1mGw0mPpcxjpiucVieqw09oS0hJS0wQpfufSc9Pw0xqwU9Gr2QGp8ZGk2EMNk40pfpfZ0ghw06CpUxCSkgFS1wbVi6QSUpcpiJESkLJN1mGB0d6p8sGr2EcpfwCS060w0wESkxqSk4qwfSJSkFcw19qwc40SfJySbEMNBEFaTEBN1mGZkwbZqgcw0pcpcxCZ1gTZk4yVksCZk4qpkJoS0s0wieGr2EcZfmqkywPnm%3D%3D"
        }

        # 웹페이지 요청
        response = requests.post(url,headers=headers,data=data)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()["ingList"]
        for element in target_data:
            start_date, end_date = [re.sub(r"(\d{4})(\d{2})(\d{2}).*$", r"\1-\2-\3", x) for x in [element['startday'], element['endday']]]

            event_list.append({
                "title": element['evnt_nm'],
                "startDt": start_date,
                "endDt": end_date,
                "listURL": list_domain,
                "detailURL": detail_domain+element["evnt_cd"]+"&dummyVal=0"
            })

        print(f"키움증권 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list

    except Exception as e:
        print(f"키움증권 오류 발생: {e}")
        return [{"ERROR": str(e)}]





import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 미래에셋생명
# 금융사코드 : 431
# 방식 : API 
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################


##############################
# Service URL = "https://life.miraeasset.com/online/event/getEventList.do"
# Method = POST
        # headers = {
        #     "Accept": "application/json, text/javascript, */*; q=0.01"
        # }
        # body = {
        # "pageNo":1
        # }
##############################


async def get431Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://life.miraeasset.com/online/event/getEventList.do"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 이미지 파일 URL 기본값
    img_domain =  "https://life.miraeasset.com/pool_img/"
    #목록 URL
    list_domain = "https://life.miraeasset.com/online/directPage.do?_OC_=4266&cp=MO-DR-040100-000000#MO-DR-040100-000000"
    ######### 기초 설정 END ##############

    try:
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01"
        }
        data = {"pageNo":1}
        # 웹페이지 요청
        response = requests.post(url, headers=headers,json=data)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()["data"]["rst"]
        for element in target_data:
            start_date, end_date = [re.sub(r"(\d{4})(\d{2})(\d{2})", r"\1-\2-\3", x) for x in [element['eventStartDtm'], element['eventEndDtm']]]

            #  확인용
            # print(f"제목 : {element['bbsTitle']}")
            # print(f"시작 : {start_date}")
            # print(f"종료 : {end_date}")
            # print(f"썸네일URL : {img_domain+element['eventBanner']}")
            # print(f"이벤트목록URL : {list_domain}")
            # print("-")

            event_list.append({
                "title": element['bbsTitle'],
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": img_domain+element['eventBanner'],
                "listURL": list_domain
            })

        print(f"미래에셋생명 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list
    
    except Exception as e:
        print(f"미래에셋생명 오류 발생: {e}")
        return [{"ERROR": str(e)}]






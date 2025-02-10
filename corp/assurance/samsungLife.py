import re
import requests


##############################
# 제목 : 삼성생명
# 금융사코드 : 452
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

##############################
# 삼성생명: 동적페이지
# Service URL = "https://www.samsunglife.com/gw/api/display/event/ing/list"
# Method = POST
        # headers = {
        #     "User-Agent": "Mozilla/5.0"
        #     ,"Content-Type": "application/x-www-form-urlencoded"
        #     ,"Cookie":"WMONID=zA_dF3eh6g9; m1JSESSIONID=KhvUVJaOukdFrbAVGnqnMf_YZD5lLLpOYEp0uAMl5SjG7pfFuQ96!-450219573!-749097412"
        #     }
        # data = {
        #     "g":"/xY+zQt2jWkBC9Tba/qyU36r/7cEjANen4DGYhcE69cB97JxCx0dmhcat9F12qtZc9sq+qhGisKSAbM0",
        #     "b":"NGFiMjM3NGI2MDQ5NDVjMjgyMWFhODA3ZDRiNjc3NjGORB3PUhHsQkcJ6N418IheC/Du4R3FB36O3qdRBwTD3GfHnE02cgDtZRSF9i7u8S9I8i33tjedyc4K4hU="
        # }
##############################


async def get452Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://www.samsunglife.com/gw/api/display/event/ing/list"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 목록 URL 기본값
    list_domain =  "https://www.samsunglife.com/individual/display/event/PDP-IFEVT010000M/0"
    ######### 기초 설정 END ##############
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
            ,"Content-Type": "application/x-www-form-urlencoded"
            ,"Cookie":"WMONID=zA_dF3eh6g9; m1JSESSIONID=KhvUVJaOukdFrbAVGnqnMf_YZD5lLLpOYEp0uAMl5SjG7pfFuQ96!-450219573!-749097412"
            }
        data = {
            "g":"/xY+zQt2jWkBC9Tba/qyU36r/7cEjANen4DGYhcE69cB97JxCx0dmhcat9F12qtZc9sq+qhGisKSAbM0",
            "b":"NGFiMjM3NGI2MDQ5NDVjMjgyMWFhODA3ZDRiNjc3NjGORB3PUhHsQkcJ6N418IheC/Du4R3FB36O3qdRBwTD3GfHnE02cgDtZRSF9i7u8S9I8i33tjedyc4K4hU="
        }
        # 요청
        response = requests.post(url, headers=headers,data=data)
        response.raise_for_status()  # 오류 발생 시 예외 처리

        #데이터 가공
        target_data= response.json()["response"]
        for element in target_data:
            start_date= re.search(r'\d{4}-\d{2}-\d{2}', element['evtStrDtm']).group()
            end_date= re.search(r'\d{4}-\d{2}-\d{2}', element['evtEndDtm']).group()

            #상세 URL이 없는것도 있음
            if element['hpgLnkUrl'].index("/") != 0:
                detail_url = ""
            else:
                detail_url = domain+element['hpgLnkUrl']

            # 확인용
            # print(f"제목 : {element['evtNm'].replace('<br>','')}")
            # print(f"시작 : {start_date}")
            # print(f"종료 : {end_date}")
            # print(f"썸네일URL: {element['fileDownUrl']}")
            # print(f"이벤트목록URL: {list_domain}")
            # print(f"상세URL: {detail_url}") 
            
            event_list.append({
                "title": element['evtNm'].replace('<br>',''),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": element['fileDownUrl'],
                "listURL": list_domain,
                "detailURL": detail_url
            })
        
        print(f"삼성생명 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list       

    except Exception as e:
        print(f"삼성생명 오류 발생: {e}")
        return [{"ERROR": str(e)}]

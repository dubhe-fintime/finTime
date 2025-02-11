import re
import requests

##############################
# 제목 : 삼성화재
# 금융사코드 : 441
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : X | 종료일 : X | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################


##############################
# Service URL = "https://direct.samsungfire.com/resources/json/benefit_event.json"
# Method = GET
##############################


async def get441Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://direct.samsungfire.com/resources/json/benefit_event.json"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 목록 URL 기본값
    list_domain =  "https://direct.samsungfire.com/helpdesk/PP060701_001.html"
    ######### 기초 설정 END ##############

    try:
        # 웹페이지 요청
        response = requests.get(url)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()['list']

        for element in target_data:
            event_list.append({
                "title": element['lTitle'].replace('<br>',''),
                "thumbNail": domain+element['thumb'],
                "listURL": list_domain,
                "detailURL": domain+element['pcLink']
            })

            # 확인용
            # print(f"제목 : {element['lTitle'].replace('<br>','')}")
            # print(f"썸네일URL: {domain+element['thumb']}")
            # print(f"이벤트목록URL: {list_domain}")
            # print(f"상세페이지URL: {domain+element['pcLink']}")
            # print("-")


        print(f"삼성화재 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list

    except Exception as e:
        print(f"삼성화재 오류 발생: {e}")
        return [{"ERROR": str(e)}]






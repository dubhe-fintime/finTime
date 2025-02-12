import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : NH손해보험
# 금융사코드 : 449
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

def get449Data():
    ######### 기초 설정 Start #############

    # return 값 넣을 리스트
    event_list = []

    url = "https://www.nhfire.co.kr/event/event/retrieveProgressEventList.nhfire"

    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)

    ######### 기초 설정 END ##############
    # 요청
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()  # 오류 발생 시 예외 처리
    soup = BeautifulSoup(response.text, 'html.parser')

    # 요소 찾기 
    container = soup.find("ul" ,class_="eventList")

    for element in container.find_all("li"):
        print("@@@@@@@@@@@@@@@@@@@@")
        print(f"{element}")
        print("@@@@@@@@@@@@@@@@@@@@")

        # 확인용

    print(f"NH손해보험 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
    return event_list

get449Data()   


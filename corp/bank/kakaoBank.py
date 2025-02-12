import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 카카오뱅크
# 금융사코드 : 090
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O  
##############################

async def get090Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # URL
    url = "https://m.kakaobank.com/Events"
    ######### 기초 설정 END ##############

    try:
        # 웹페이지 요청
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        container = soup.find("ul", class_="list-event")
        print(container)
        for element in container.find_all("li",class_="item"):
            start_date,end_date = [time["datetime"] for time in element.find("span").find_all("time")]

            event_list.append({
                "title": element.find("div",class_="tit-area").text.strip(),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": element.find("img")["src"],
                "listURL": url,
                "detailURL": element.find("a")["href"]
            })

        print(f"카카오뱅크 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list

    except Exception as e:
        print(f"카카오뱅크 오류 발생: {e}")
        return [{"ERROR": e}]
    


import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 우리은행
# 금융사코드 : 020
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

async def get020Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # URL
    url = "https://spot.wooribank.com/pot/Dream?withyou=EVEVT0001"
    ######### 기초 설정 END ##############

    try:
        # 웹페이지 요청
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        container = soup.find("div", class_="list-thumbnail")
        for element in container.find_all("dl",class_="list-set"):
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', element.find("dd",class_="contl-opt").text.strip().replace(".","-"))

            event_list.append({
                "title": element.find("a").text.strip(),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": element.find("img")["src"].replace(" ","%20"),
                "listURL": url
            })

        print(f"우리은행 완료 | 이벤트 개수 : {len(event_list)}")

    except Exception as e:
        print(f"우리은행 오류 발생 : {e}")
        return [{"ERROR": str(e)}]

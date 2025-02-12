import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 국민은행
# 금융사코드 : 004
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

async def get004Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # URL
    url = "https://omoney.kbstar.com/quics?page=oevent"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    ######### 기초 설정 END ##############

    try:
        # 웹페이지 요청
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        container = soup.find("div", class_="eventListArea")
        for element in container.find_all("li"):
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', element.find("dd",class_="date").text.replace(".","-"))
            print(element.find("dt").text)
            print(start_date)
            print(end_date)
            print(element.find("img")["src"])

            event_list.append({
                "title": element.find("dt").text,
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": element.find("img")["src"],
                "listURL": url
            })

        print(f"국민은행 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list
    
    except Exception as e:
        print(f"국민은행 오류 발생: {e}")
        return [{"ERROR": e}]
    


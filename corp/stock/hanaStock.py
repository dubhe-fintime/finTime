import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 하나증권
# 금융사코드 : 270
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get270Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # URL
    url = "https://www.hanaw.com/corebbs5/eventIng/list/list.cmd"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    ######### 기초 설정 END ##############
    try:
        # 웹페이지 요청
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        container = soup.find("div", class_="evt_list")
        for element in container.find_all("li"):
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', element.find("span",class_="date").text.strip().replace(".","-"))

            event_list.append({
                "title": element.find("img")["alt"],
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": domain+element.find("img")["src"],
                "listURL": url,
                "detailURL":domain+element.find("a")["href"]
            })

        print(f"하나증권 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list
        
    except Exception as e:
        print(f"하나증권 오류 발생: {e}")
        return [{"ERROR": str(e)}]

import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : IBK기업은행
# 금융사코드 : 003
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################   

async def get003Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # URL
    url = "https://www.ibk.co.kr/event/ingListEvent.ibk?pageId=CM01060100&evnt_dscd=H"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    ######### 기초 설정 END ##############

    try:
        # 웹페이지 요청
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        container = soup.find("ul", class_="event_ing")
        for event_img,event_info in zip(container.find_all("span",class_="event_banner"),container.find_all("div",class_="event_info")):
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', event_info.find("li").text.strip().replace(".","-"))
            
            event_list.append({
                "title": event_info.find("a").text.strip(),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": domain+event_img.find("img")["src"],
                "listURL": url,
                "detailURL": domain+event_img.find("a")["href"]
            })

        print(f"IBK기업은행 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list

    except Exception as e:
        print(f"IBK기업은행 오류 발생: {e}")
        return [{"ERROR": e}]
    


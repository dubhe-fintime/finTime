import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime

##############################
# 제목 : ABL생명보험
# 금융사코드 : 437
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : X | 종료일 : X | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get437Data():

    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    #URL
    url = "https://www.abllife.co.kr/st/custDesk/events?page=index"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    ######### 기초 설정 END ##############

    try:
        # 웹페이지 요청
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 이벤트 목록 찾기
        events = soup.find_all("div", class_="article_box thumb")
        for event in events:
            title_tag = event.find("a", class_="subject")  # 제목 태그 찾기
            date_tag = event.find("span", class_="date")  # 날짜 태그 찾기
            link_tag = event.find("a", class_="subject")  # 링크 태그 찾기

            if title_tag and date_tag and link_tag:
                title = title_tag.text.strip()  # 이벤트 제목
                date = date_tag.text.strip()  # 이벤트 기간
                link = link_tag["href"]  # 이벤트 상세 링크

                ##TODO: 등록날짜는 있어서, 혹시몰라서 내비둠 
                date_obj = datetime.strptime(date.replace(",", "").strip(), "%m월 %d일 %Y").strftime("%Y-%m-%d")

                event_list.append({
                    "title": title,
                    "thumbNail": domain+event.find('img')['src'],
                    "listURL": url,
                    "detailURL": domain+link
                })
                # 확인용
                # print(f"제목 : {title}")
                # print(f"썸네일URL : {domain+event.find('img')['src']}")
                # print(f"목록URL : {url}")
                # print(f"상세URL: {domain+link}") 

            print(f"ABL생명 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
            print("최종 결과 >>")
            print(event_list)
            return event_list       
        
    except Exception as e:
        print(f"ABL생명 오류 발생: {e}")
        return [{"ERROR": str(e)}]
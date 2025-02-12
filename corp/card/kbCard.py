import requests
import re
from bs4 import BeautifulSoup

##############################
# 제목 : KB카드
# 금융사코드 : 381
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get381Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # 목록 URL 기본값
    url = "https://card.kbcard.com/BON/DVIEW/HBBMCXCRVNEC0002" 
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    detail_domain =  "https://card.kbcard.com/BON/DVIEW/HBBMCXCRVNEC0002?mainCC=a&eventNum="
    ######### 기초 설정 END ##############
    try:
        # 웹페이지 요청
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        #요소 찾기
        events = soup.find_all("div", class_="eventListWrap")
        for event in events:
            li_tags = event.find_all("li")
            for li in li_tags:
                title = li.find("span", class_="store").text.strip() + " " + li.find("span", class_="subject").text.strip() # 이벤트 제목
                
                start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', li.find("span", class_="date").text.strip().replace(".","-"))
                
                filtering_temp = re.search(r"goDetail\('(.+?)'\)", li.find("a")["href"])
                if filtering_temp:
                    return_detail = detail_domain+filtering_temp.group(1)

                event_list.append({
                    "title": title,
                    "startDt": start_date,
                    "endDt": end_date,
                    "thumbNail": li.find('img')['src'],
                    "listURL": url,
                    "detailURL": return_detail
                })
                # 확인용
                # print(f"제목: {title}")
                # print(f"시작: {start_date}")
                # print(f"종료: {end_date}")
                # print(f"썸네일 : {li.find('img')['src']}")
                # print(f'목록URL : {url}')
                # print(f"상세URL: {return_detail}")

        print(f"KB카드 크롤링 완료 | 이벤트 개수 : {len(event_list)}")         
        return event_list
    except Exception as e:
        print(f"KB카드 오류 발생: {e}")
        return [{"ERROR": str(e)}]


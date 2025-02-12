import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 대신증권
# 금융사코드 : 209
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get209Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # URL
    url = "https://www.myasset.com/myasset/hello/event/CU_0203000_T1.cmd"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    ######### 기초 설정 END ##############

    try:
        # 웹페이지 요청
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        events = soup.find_all("div", class_="eventListWrap")
        for event in events:
            li_tags = event.find_all("li")
            for li in li_tags:
                title = li.find("p", class_="tit").text.strip() 
                date = li.find("em").text.strip()  
                link = li.find("a")["href"]  
                thumbnail = domain + li.find('img')['src'] if li.find('img')['src'] else "" 
                link = domain + li.find("a")["href"]  
                if "javascript" in link.lower():  
                    link = ""

                start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', date.replace("/","-"))

                event_list.append({
                                "title": title,
                                "startDt": start_date,
                                "endDt": end_date,
                                "thumbNail": thumbnail,
                                "listURL": url,
                                "detailURL": link
                            })
            print(f"유안타증권 크롤링 완료 | 이벤트 개수 : {len(event_list)}")     
            return event_list
    
    except Exception as e:
        print(f"유안타증권 오류 발생: {e}")
        return [{"ERROR": str(e)}]
    

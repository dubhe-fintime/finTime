import requests
from bs4 import BeautifulSoup

async def get081Data():
    # 하나은행 이벤트 페이지 URL
    url = "https://www.kebhana.com/cont/news/news02/index.jsp"

    # 웹페이지 요청
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")

    #print(soup)
    # 이벤트 목록 찾기 (예제: 특정 클래스명을 기준으로 검색)
    events = soup.find_all("div", class_="evt_list")

    # 이벤트 정보 출력
    event_list = []  # 이벤트 데이터를 담을 리스트
    for event in events:
        print(event)
        li_tags = event.find_all("li")
        #print(li_tags)
        print(f"이벤트 개수: {len(li_tags)}")  # 몇 개의 이벤트가 검색되는지 확인
        for li in li_tags:
            title = li.find("p").text.strip()  # 이벤트 제목
            date = li.find("span").text.strip()  # 이벤트 기간
            link = li.find("a")["href"]  # 이벤트 상세 링크
            #print(f"이벤트명: {title}")
            #print(f"이벤트 기간: {date}")
            #print(f"자세히 보기: {link}\n")
            event_list.append({
                        "title": title,
                        "date": date,
                        "link": link
                    })
        
        return event_list

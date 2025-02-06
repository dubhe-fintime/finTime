import requests
from bs4 import BeautifulSoup

async def get437Data():
    # ABL생명 이벤트 페이지 URL
    url = "https://www.abllife.co.kr/st/custDesk/events?page=index"

    # 웹페이지 요청
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")

    # 이벤트 목록 찾기
    events = soup.find_all("div", class_="article_box thumb")

    # 이벤트 정보 리스트
    event_list = []
    print(f"이벤트 개수: {len(events)}")  # 몇 개의 이벤트가 검색되는지 확인
    for event in events:
        title_tag = event.find("a", class_="subject")  # 제목 태그 찾기
        date_tag = event.find("span", class_="date")  # 날짜 태그 찾기
        link_tag = event.find("a", class_="subject")  # 링크 태그 찾기
        
        if title_tag and date_tag and link_tag:
            title = title_tag.text.strip()  # 이벤트 제목
            date = date_tag.text.strip()  # 이벤트 기간
            link = link_tag["href"]  # 이벤트 상세 링크

            event_list.append({
                "title": title,
                "date": date,
                "link": link
            })

            print(f"이벤트명: {title}")
            print(f"이벤트 기간: {date}")
            print(f"자세히 보기: {link}\n")

    return event_list
import requests
from bs4 import BeautifulSoup
import time

##############################
# 제목 : 미래에셋증권
# 금융사코드 : 238
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

# 실제 URL에서 페이지 번호를 쿼리 파라미터로 변경
BASE_URL = "https://securities.miraeasset.com/hki/hki7000/r05.do?currentPage={}&cs_ecis_id=#"

# User-Agent 추가 (403 Forbidden 방지)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 이벤트 리스트를 저장할 리스트
event_list = []


def get238Data():
    # 페이지 탐색 시작
    page = 1
    list_domain = "https://securities.miraeasset.com/hki/hki7000/r05.do"  # 리스트 URL
    detail_domain = "https://securities.miraeasset.com/event/view/"  # 상세 이벤트 URL

    global event_list
    while True:
        url = BASE_URL.format(page)
        
        try:
            # 웹 페이지 요청
            response = requests.get(url, headers=HEADERS)

            if response.status_code != 200:
                break

            # BeautifulSoup으로 HTML 파싱
            soup = BeautifulSoup(response.text, "html.parser")

            # 이벤트 리스트 찾기
            events = soup.select("ul.split.col3.eventLstWrap li.colSec")

            if not events:
                break  # 이벤트가 없으면 종료

            for event in events:
                title = event.select_one("dd.evTit").text.strip()  # 제목
                date = event.select_one("dd.evDate").text.strip()  # 날짜
                img_url = event.select_one("dt a img")["src"]  # 이미지 URL

                # 날짜 파싱 (날짜 범위로 시작일과 종료일 분리)
                start_date, end_date = date.split(" ~ ") if " ~ " in date else (date, date)

                # 링크 파싱 (javascript:doView('202502007','5','') 형태 처리)
                raw_link = event.select_one("dt a")["href"]
                if "javascript:doView" in raw_link:
                    try:
                        event_id = raw_link.split("'")[1]  # 이벤트 ID 추출
                        event_link = f"{detail_domain}{event_id}&dummyVal=0"  # 상세 링크 생성
                    except IndexError:
                        event_link = "#"
                else:
                    event_link = raw_link  # 일반적인 URL이라면 그대로 사용

                # 데이터 추가
                event_data = {
                    "title": title,
                    "startDt": start_date,
                    "endDt": end_date,
                    "listURL": list_domain,
                    "thumbNail": "https://securities.miraeasset.com" + img_url,
                    "detailURL": event_link
                }
                event_list.append(event_data)

            # 다음 페이지로 이동
            page += 1
            time.sleep(1)  # 서버 부하 방지를 위해 1초 대기
            

        except requests.exceptions.RequestException as e:
            print(f"미래에셋증권권 요청 오류 발생: {e}")
            return [{"ERROR": str(e)}]
        except Exception as e:
            print(f"미래에셋증권권 크롤링 오류 발생: {e}")
            return [{"ERROR": str(e)}]
    
    print(f"미래에셋증권권 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
    return event_list
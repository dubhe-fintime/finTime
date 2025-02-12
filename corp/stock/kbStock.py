import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : KB증권
# 금융사코드 : 218
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get218Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # URL
    url = "https://www.kbsec.com/cs/notice/jsp/CUST_09_0003.jsp"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    ######### 기초 설정 END ##############
    try:
        # 웹페이지 요청
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        events = soup.find_all("div", class_="eventWrap")
        for event in events:
            li_tags = event.find_all("li")
            for li in li_tags:
                # 요소 찾기 (None 방지)
                title_span = li.find("span", class_="itxtTy8")
                title_subj = li.find("a", class_="subj")

                # 제목이 없을 경우 대비하여 기본값 설정
                title_text = title_span.text.strip() if title_span else ""
                subj_text = title_subj.text.strip() if title_subj else ""
                
                title = f"{title_text} {subj_text}".strip()  # 이벤트 제목
                date = li.find("dd", class_="date").text.strip()  # 이벤트 기간
                thumbnail = li.find('img')['src'] if li.find('img')['src'] else "" # 썸네일 이미지 링크
                link = domain + li.find("a")["href"]  # 이벤트 상세 링크
                if "javascript" in link.lower():  # 대소문자 구분 없이 검사
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
            print(f"KB증권 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
            return event_list
        
    except Exception as e:
        print(f"KB증권 오류 발생: {e}")
        return [{"ERROR": str(e)}]


import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 한국투자증권
# 금융사코드 : 243
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get243Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # URL
    url = "https://www.truefriend.com/main/customer/notice/Event.jsp?gubun=i"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    ######### 기초 설정 END ##############
    try:
        # 웹페이지 요청
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        container = soup.find("div", class_="event_box")
        for element in container.find_all("li"):

            #날짜데이터 가공
            cleaned_text = re.sub(r"\s+", " ", element.find("span",class_="letter_0").text).strip().replace(".","-")
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', cleaned_text)

            #상세URL 
            filtering_temp = re.search(r"doView\('(\d+)'", element.find("a")["href"])
            event_nm = filtering_temp.group(1) if filtering_temp else ""
            detail_domain = f"{domain}/main/customer/notice/Event.jsp?gubun=i&cmd=TF04gb010002&num={event_nm}&from=&currentPage=1&CUSTGUBUN=00&focusYN=&userRowsPerPage=10&searchColumn=all&searchValue="

            event_list.append({
                "title": element.find("p",class_="title").text,
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": element.find("img")["src"],
                "listURL": url,
                "detailURL": detail_domain
            })
        print(f"한국투자증권 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list
        
    except Exception as e:
        print(f"한국투자증권 오류 발생: {e}")
        return [{"ERROR": str(e)}]
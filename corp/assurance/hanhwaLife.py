import requests
import re
from bs4 import BeautifulSoup

##############################
# 제목 : 한화생명
# 금융사코드 : 432
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get432Data():

    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    
    # 크롤링URL
    url = "https://www.hanwhalife.com/main/benefit/event/BS_EQEV000_P10000.do" 
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    ######### 기초 설정 END ##############
    try:
        # 웹페이지 요청
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        print(response.encoding)
        response.raise_for_status()  # 오류 발생 시 예외 처리
        soup = BeautifulSoup(response.text, 'html.parser')

        # 요소 찾기
        container = soup.find("div", class_="eventList")
        for element in container.find_all("li"):
            start_date, end_date = "", ""
            # start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', element.find_all("dd")[-1].text)

            #상세페이지 (a태그중 마지막 &가  "¤" 잘못 인코딩 될 경우)
            detail = "/".join([
                domain,
                "main",
                "benefit",
                "event",
                str(element.find("a")["href"].lstrip('./')).replace("¤","&")
            ])

            event_list.append({
                "title": element.find('p', class_='tit').text.strip(),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": element.find('img')['src'],
                "listURL": url,
                "detailURL": detail
            })

            # 확인용
            # print(f"제목 : {element.find('p', class_='tit').text.strip()}")
            # print(f"시작 : {start_date}")
            # print(f"종료 : {end_date}")
            # print(f"썸네일URL : {element.find('img')['src']}")
            # print(f"목록URL : {url}")
            # print(f"상세URL: {detail}") 
            # print("-")

        print(f"한화생명 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list            
        
    except Exception  as e:
        print(f"흥국생명 오류 발생: {e}")
        return e


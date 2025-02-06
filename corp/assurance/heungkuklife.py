import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : 흥국생명
# 금융사코드 : 453
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

async def get457Data():

    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    
    # 크롤링URL
    url = "https://www.heungkuklife.co.kr/front/help/eventList.do" 
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)

    ######### 기초 설정 END ##############
    try:
        # 웹페이지 요청
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # 오류 발생 시 예외 처리
        
        # BeautifulSoup 기초 설정 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #전체 html 찍어볼 경우
        #print(soup)

        # 페이지 제목 
        title = soup.title.string if soup.title else "제목 없음"
        print(f"페이지 제목: {title}\n")

        # class값 찾는법
        container = soup.find("ul" ,class_="img_list")

        for element in container.find_all("li"):
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', element.find('p').text)

            event_list.append({
                "title": element.find('span',class_='ib_title').text.strip(),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": domain+element.find('img')['src'],
                "listURL": url
            })

            # 확인용
            # print(f"제목 : {element.find('span',class_='ib_title').text.strip()}")
            # print(f"시작 : {start_date}")
            # print(f"종료 : {end_date}")
            # print(f"썸네일URL : {domain+element.find('img')['src']}")
            # print(f"목록URL : {url}")
            # print("-")


        print(f"흥국생명 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list
    
    except requests.exceptions.RequestException as e:
        print(f"흥국생명 오류 발생: {e}")
        return "Fail"


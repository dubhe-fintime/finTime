import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : NH손해보험
# 금융사코드 : 449
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

async def get449Data():
    ######### 기초 설정 Start #############

    # return 값 넣을 리스트
    event_list = []

    url = "https://www.nhfire.co.kr/event/event/retrieveProgressEventList.nhfire"

    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)

    ######### 기초 설정 END ##############
    try:
        # 요청
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # 오류 발생 시 예외 처리
        soup = BeautifulSoup(response.text, 'html.parser')

        # 요소 찾기 
        container = soup.find("ul" ,class_="eventListArea")
        for element in container.find_all("li",class_=""):
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', element.find('li',class_='infoText fl').text.strip())

            event_list.append({
                "title": element.find('li',class_='eventTit').text.strip(),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": domain+element.find('img')['src'],
                "listURL": url
            }) 

            # 확인용
            # print(f"제목 : {element.find('li',class_='eventTit').text.strip()}")
            # print(f"시작 : {start_date}")
            # print(f"종료 : {end_date}")
            # print(f"썸네일URL : {domain+element.find('img')['src']}")
            # print(f"목록URL : {url}")        

        print(f"NH손해보험 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list

    except Exception as e:
        print(f"NH손해보험 오류 발생: {e}")
        return [{"ERROR": e}]




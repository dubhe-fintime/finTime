import re
import requests
from bs4 import BeautifulSoup

##############################
# 제목 : DB생명
# 금융사코드 : 457
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

async def get457Data():
    ######### 기초 설정 Start #############

    # return 값 넣을 리스트
    event_list = []
    # 목록 URL 기본값
    url = "https://www.idblife.com/support/notice/event" 
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)

    ######### 기초 설정 END ##############
    try:
        # 요청
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # 오류 발생 시 예외 처리

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 요소 찾기 
        container = soup.find("ul" ,class_="banner_lst")
        print(f"이벤트 개수 : {len(container.find_all('li'))}")
        for element in container.find_all("li"):
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', element.find('span',class_='date').text.strip())

            event_list.append({
                "title": element.find("dd",class_="tit").text.strip(),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": domain + element.find('img')['src'],
                "listURL": url
            })

        print(f"DB생명 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list

    except requests.exceptions.RequestException as e:
        print(f"DB생명 오류 발생: {e}")
        return "Fail"


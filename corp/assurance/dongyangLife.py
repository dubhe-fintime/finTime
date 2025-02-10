import requests
import re
from bs4 import BeautifulSoup

##############################
# 제목 : 동양생명
# 금융사코드 : 402
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : X 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
# 특이사항 : 이미지가 다운로드 URL
##############################

async def get402Data():
    ######### 기초 설정 Start #############

    # return 값 넣을 리스트
    event_list = []
    # 목록 URL 기본값
    url = "https://online.myangel.co.kr/lounge/event.e1004" 
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 상세페이지 URL 기본값
    detail_domain =  "https://online.myangel.co.kr/lounge/eventDetl.e1004?EVNT_SEQNO="

    ######### 기초 설정 END ##############
    try:
        # 요청
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # 오류 발생 시 예외 처리
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 요소 찾기 
        container = soup.find_all("div" ,class_="list-item")
        for element in container:
            print(element.find("span", class_=""))
            temp_date = element.find("span", class_="").text.replace('.', '-')  if element.find("span", class_="") else ""
            if temp_date != "":
                start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', temp_date)
            else:
                start_date, end_date = element.find("span", class_=""), element.find("span", class_="").text

            detail = detail_domain +element.find("a")["onclick"].split('(')[1].split(')')[0]

            #확인용pyyth
            # print(f"제목 :{element.find('h4').text}")
            # print(f"시작 :{start_date}")
            # print(f"종료 :{end_date}")
            # print(f"이미지URL :{domain+element.find('img')['src']} ")
            # print(f"목록URL :{url}")
            # print(f"상세URL :{detail}")

            event_list.append({
                "title": element.find('h4').text.strip(),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": domain+element.find('img')['src'],
                "listURL": url,
                "detailURL": detail
            })

        print(f"동양생명 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list
        
    except Exception as e:
        print(f"동양생명 오류 발생: {e}")
        #return [{"ERROR": e}]
        return [{"ERROR": str(e)}] 



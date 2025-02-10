import requests
import re
from bs4 import BeautifulSoup

##############################
# 제목 : 흥국화재
# 금융사코드 : 403
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

async def get403Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    
    # 크롤링URL
    url = "https://www.heungkukfire.co.kr/FRW/companyIntro/eventCurrent.do" 
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)

    ######### 기초 설정 END ##############
    try:
        # 웹페이지 요청
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # 오류 발생 시 예외 처리
        soup = BeautifulSoup(response.text, 'html.parser')

        # 요소 찾기
        container = soup.find("div" ,class_="event_list")
        for tr_tag in container.find_all("tr"):
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', tr_tag.find("span",class_="event_date").text.strip().replace(".","-"))

            event_list.append({
                "title": tr_tag.find("li",class_="event_tit").text.strip(),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": domain+tr_tag.find("img")["src"],
                "listURL": url,
                "detailURL": domain+tr_tag.find("a")["href"]
            })

        #     확인용
        #     print(f'제목 : {tr_tag.find("li",class_="event_tit").text.strip()}')
        #     print(f'시작 : {start_date}')
        #     print(f'종료 : {end_date}')
        #     print(f'썸네일 : {domain+tr_tag.find("img")["src"]}')
        #     print(f'상세 : {domain+tr_tag.find("a")["href"]}')
        
        print(f"흥국화재 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list

    except Exception as e:
        print(f"흥국화재 오류 발생: {e}")
        return [{"ERROR": str(e)}]


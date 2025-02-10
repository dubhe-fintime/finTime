import requests
import re
from bs4 import BeautifulSoup

##############################
# 제목 : KB손해보험
# 금융사코드 : 444
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get444Data():
    ######### 기초 설정 Start #############

    # return 값 넣을 리스트
    event_list = []
    # 목록 URL 기본값
    url = "https://www.kbinsure.co.kr/CG701010001.ec" 
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    ######### 기초 설정 END ##############
    try:
        # 웹페이지 요청
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # 오류 발생 시 예외 처리
        soup = BeautifulSoup(response.text, 'html.parser')
        

        # 요소 찾기
        container = soup.find("table" ,class_="tb_eventList")
        for tr_tag in container.find_all("tr"):
            
            #상세URL 가공
            filtering_temp = re.search(r"content\('(.+?)'\)", tr_tag.find("a")["href"])
            if filtering_temp:
                detail_domain = filtering_temp.group(1)

            #시작,종료 가공
            first_li = tr_tag.find("ul", class_="Gray_bul").find("li")
            for strong_tag in first_li.find_all("strong"):
                strong_tag.decompose()
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', first_li.get_text(strip=True))

            event_list.append({
                "title": tr_tag.find("p",class_="eventSubject").text.strip(),
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": domain+tr_tag.find("img")["src"],
                "listURL": url,
                "detailURL": domain+"/"+detail_domain
            })
            #확인용
            # print(f'제목 : {tr_tag.find("p",class_="eventSubject").text.strip()}')
            # print(f"시작 :{start_date}")
            # print(f"종료 :{end_date}")
            # print(f'썸네일 : {domain+tr_tag.find("img")["src"]}')
            # print(f'상세URL : {domain+"/"+detail_domain}')

        print(f"KB손해보험 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list

    except Exception as e:
        print(f"KB손해보험 오류 발생: {e}")
        return [{"ERROR": e}]




import re
import requests
import ssl
from bs4 import BeautifulSoup

##############################
# 제목 : 하나카드
# 금융사코드 : 374
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get374Data():

    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # 크롤링URL
    url = "https://www.hanacard.co.kr/OPP35000000D.web" 
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 상세페이지 URL 기본값
    detail_domain =  "https://www.hanacard.co.kr/OPP35000001D.web?schID=ncd&mID=OPP35000001D&EVN_SEQ="
    ######### 기초 설정 END ##############

    try:
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'

        # 또는 직접 SSL 컨텍스트를 설정해서 요청
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT:@SECLEVEL=1')
        # 웹페이지 요청
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"},verify=False)
        response.raise_for_status()  # 오류 발생 시 예외 처리 
        soup = BeautifulSoup(response.text, 'html.parser')

        # 찾기
        container = soup.find("ul" ,class_="thumb_ty")
        for element in container.find_all("li"):
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', element.find("div",class_="txt").find("p",class_="s2").text.replace(".","-"))

            filtering_temp = re.search(r"goView\('(\d+)'", element.find("a")["href"])
            if filtering_temp:
                detail_target = filtering_temp.group(1)
            else:
                detail_target = ""

            event_list.append({
                "title": element.find("div",class_="txt").find("dt").text,
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": domain+element.find("img")["src"],
                "listURL": url,
                "detailURL": detail_domain+detail_target
            })

        print(f"하나카드 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list
    
    except Exception as e:
        print(f"하나카드 오류 발생: {e}")
        return [{"ERROR": str(e)}]


import re
import requests
import urllib3

# 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

##############################
# 제목 : 제주은행
# 금융사코드 : 035
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get035Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://www.jejubank.co.kr/hmpg/csct/evnt.doax"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 목록 URL 
    list_domain =  "https://www.jejubank.co.kr/hmpg/csct/evnt.do"
    ######### 기초 설정 END ##############

    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    params = {
        "viewCount" : 9,
        "isMore": 0 ,
        "moreIdx" :"",
        "lastId" :"",
        "evntSttus" :"progress",
        "titlVal" :""
    }

    try:
        # 웹페이지 요청
        response = requests.get(url,headers=header,params=params,verify=False)
        print(requests.__url__)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()['data']

        #/hmpg/csct/evnt.do?mode=detail&evntId=EVNT_bd3eebae6ad84200ba0bc822c87376a2

        for element in target_data:
            start_date, end_date = [re.sub(r"(\d{4})-(\d{2})-(\d{2}).*$", r"\1-\2-\3", x) for x in [element['evntStrtDttm'], element['evntEndDttm']]]

            event_list.append({
                "title": element['titlVal'],
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": element['thumbImg']['encodedImg'],
                "listURL": list_domain,
                "detailURL": domain+'/hmpg/csct/evnt.do?mode=detail&evntId='+element['evntId']
            })

        print(f"제주은행 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list
        
    except Exception as e:
        print(f"제주은행 오류 발생: {e}")
        return [{"ERROR": str(e)}]




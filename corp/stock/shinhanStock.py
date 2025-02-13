import re
import requests

##############################
# 제목 : 신한투자증권
# 금융사코드 : 278
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
# 썸네일 다운로드 URL
##############################

##############################
# Service URL = "https://bbs2.shinhansec.com/bbs/list/giEvent.do?v=1739402505528&curPage=1&startPage=1&searchText=7A==&searchType=VARIABLE_FIELD2"
# Method = GET
##############################

async def get278Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://bbs2.shinhansec.com/bbs/list/giEvent.do"
    # 목록 URL 
    list_domain =  "https://www.shinhansec.com/siw/customer-center/event/giEvent1/view.do"
    ######### 기초 설정 END ##############

    try:
        params = {
            "v": "1739402505528",
            "curPage": "1",
            "startPage": "1",
            "searchText": "7A==",
            "searchType": "VARIABLE_FIELD2"
        }

        # 웹페이지 요청
        response = requests.get(url,params=params)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()['list']
        for element in target_data:
            start_date, end_date = [re.findall(r'\d{4}-\d{2}-\d{2}', element[f].replace("/","-"))[0] for f in ['f6', 'f7']]

            event_list.append({
                "title": element['f1'],
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": element['f10'],
                "listURL": list_domain,
                "detailURL": element['f9']
            })

        print(f"신한투자증권 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list

    except Exception as e:
        print(f"신한투자증권 오류 발생: {e}")
        return [{"ERROR": str(e)}]
import re
import requests

##############################
# 제목 : 삼성증권
# 금융사코드 : 240
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
# 썸네일 다운로드 URL
##############################

##############################
# Service URL = "https://www.samsungpop.com/ux/kor/customer/guide/eventguide/eventList.do"
# Method = POST
##############################

async def get240Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://www.samsungpop.com/ux/kor/customer/guide/eventguide/eventList.do"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 목록 URL 
    list_domain =  "https://www.samsungpop.com/?MENU_CODE=M1231757773125"
    # 이미지 URL 
    img_url =  "https://www.samsungpop.com/common.do?cmd=down&amp;saveKey=event.file&amp;fileName="
    ######### 기초 설정 END ##############

    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded"
            }
        body = {
            "currentPage": 1,
            "rowsPerPage": 10,
            "Search": 1,
            "SearchText": "",
            "searchStartDate": "",
            "searchEndDate": "",
            "tabIndex": 0,
            "todayEnd": 0,
            "searchType": 0,
            "CustNo1": "",
            "CustNo2": "",
            "CustNo3": "",
            "CustNm": "",
            "siteGubun": "KF",
            "searchStartDate2": "",
            "searchEndDate2": "",
            "MENU_CODE": "M1231757773125",
            "af_auto_index": "",
            "ajaxQuery": 1
        }
        # 웹페이지 요청
        response = requests.post(url,headers=headers,data=body)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()['list']
        for element in target_data:
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', element['period'])

            event_list.append({
                "title": element['ntcTitle1'],
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": img_url+element['ImgFileNm']+"&amp;inlineYn=N",
                "listURL": list_domain
            })

        print(f"삼성증권 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list

    except Exception as e:
        print(f"삼성증권 오류 발생: {e}")
        return [{"ERROR": str(e)}]





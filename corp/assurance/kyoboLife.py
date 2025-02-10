import re
import requests

##############################
# 제목 : 교보생명
# 금융사코드 : 436
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################


##############################
# Service URL = "https://www.kyobo.com/dte/event/find-ingEndEvent"
# Method = POST
# body = {
#  "searchEvtStat": "Y",
#  "searchTxt": "",
#  "sortDt": "시작일순",
#  "offsetIdx": 0,
#  "searchTypeItem": "S",
#  "limitIdx": 10,
#  "dgt_intn_exsr_yn": "Y"
# }
##############################


async def get433Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://www.kyobo.com/dte/event/find-ingEndEvent"
    # 이미지 파일 URL 기본값
    img_domain =  "https://www.kyobo.com/file/ajax/display-img?fName="
    # 상세페이지 URL 기본값
    detail_domain =  "https://www.kyobo.com/dgt/web/event/event-detail"
    # 목록 URL 기본값
    list_domain =  "https://www.kyobo.com/dgt/web/event/event-ongoing"
    ######### 기초 설정 END ##############

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        data = {
            "searchEvtStat": "Y",
            "searchTxt": "",
            "sortDt": "시작일순",
            "offsetIdx": 0,
            "searchTypeItem": "S",
            "limitIdx": 10,
            "dgt_intn_exsr_yn": "Y",
        }
        # 웹페이지 요청
        response = requests.post(url, headers=headers,json=data)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()["body"]["list"]

        for element in target_data:
            start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', element["evtPrd"])
            #썸네일 
            thumbNail = "/".join([
                img_domain,
                element['moDgtAtcFlDtyDvCd'],
                element['moThemRegDate'],
                element['moThemTmpFileNm']
            ])
            #상세페이지 
            detail = "/".join([
                detail_domain,
                str(element['dgtEvntBubdSeqtId'])
            ])

            event_list.append({
                "title": element['dgtEvntBubdTitlNm'],
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": thumbNail,
                "listURL": list_domain,
                "detailURL": detail
            })

            # 확인용
            # print(f"제목 : {element['dgtEvntBubdTitlNm']}")
            # print(f"시작 : {start_date}")
            # print(f"종료 : {end_date}")
            # print(f"썸네일URL: {thumbNail}")
            # print(f"상세페이지URL: {detail}")
            # print(f"이벤트목록URL: {url}")
            # print("-")

        print(f"교보생명 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list

    except requests.exceptions.RequestException as e:
        print(f"교보생명 오류 발생: {e}")
        return [{"ERROR": str(e)}]





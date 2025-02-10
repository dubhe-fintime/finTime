import re
import requests

##############################
# 제목 : KDB생명보험
# 금융사코드 : 458
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################


##############################
# Service URL = "https://www.kdblife.com/ajax.do?scrId=HCSCT010M01P&isJson=1"
# Method = POST
#         headers = {
#            "User-Agent": "Mozilla/5.0",
#            "Content-Type": "application/x-www-form-urlencoded",
#            "Cookie":"JSESSIONID=hiwLV1sAN4bUAktw1xorXpACj9UvJpInnS41oDT74t71R6kxvUlcRNkoS8WkYZiV.Y3NwX2RvbWFpbi9jc3BfaWNzMTE=; WMONID=ggQ0F1fut9b"
#            } 
##############################


async def get458Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://www.kdblife.com/ajax.do?scrId=HCSCT010M01P&isJson=1"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 상세페이지 URL 기본값
    detail_domain =  "https://www.kdblife.com/ajax.do?scrId=HCSCT010M02P"
    # 목록 URL 기본값
    list_domain =  "https://www.kdblife.com/ajax.do?scrId=HCSCT010M01P"
    ######### 기초 설정 END ##############
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie":"JSESSIONID=hiwLV1sAN4bUAktw1xorXpACj9UvJpInnS41oDT74t71R6kxvUlcRNkoS8WkYZiV.Y3NwX2RvbWFpbi9jc3BfaWNzMTE=; WMONID=ggQ0F1fut9b"
            }
        data = {
            "paramJson": f"%7B%22scrId%22%3A%22HCSCT010M01P%22%2C%22reqInfo%22%3A%7B%22currentDate%22%3A%222025-02-05%22%7D%2C%22pagingInfo%22%3A%7B%22recordCountPerPage%22%3A12%2C%22pageSize%22%3A10%7D%7D"
        }
        # 웹페이지 요청
        response = requests.post(url, headers=headers,data=data)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()["resultList"]
        for element in target_data:
            thumbnail = "/".join([
                domain,
                "nKumhoFiles",
                "event",
                str(element['SYS_IMG_NAME'])
            ])

            detail = "&".join([
                detail_domain,
                f"EVENT_IDX={element['EVENT_IDX']}",
                f"ISING={element['ISING']}"
            ])

            event_list.append({
                "title": element['TITLE'],
                "startDt": element['START_DATE'],
                "endDt": element['END_DATE'],
                "thumbNail": thumbnail,
                "listURL": list_domain,
                "detailURL": detail
            })
            
            # 확인용
            # print(f"제목 :{element['TITLE']}")
            # print(f"시작 :{element['START_DATE']}")
            # print(f"종료: {element['END_DATE']}")
            # print(f"목록URL: {list_domain}")
            # print(f"썸네일URL: {thumbnail}")
            # print(f"상세URL: {detail}")

        print(f"KDB생명 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print("최종 결과 >>")
        print(event_list)
        return event_list

    except Exception as e:
        print(f"KDB생명 오류 발생: {e}")
        return [{"ERROR": e}]

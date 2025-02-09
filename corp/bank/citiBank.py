import requests
import asyncio
import re
##############################
# 제목 : 시티은행
# 금융사코드 : 027
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

##############################
# Service URL = "https://www.citibank.co.kr/PbnEvntCnts0100.jct"
# Method = POST
##############################
# 목록
# {
#     "NOW_PAGE":"1",
#     "REC_SZE":"10",
#     "TYPE_CODE":"ING",
#     "SRCH_DSCD":"00"
# }
##############################

async def get027Data():
        
    event_list = []
    apiUrl = "https://www.citibank.co.kr/PbnEvntCnts0100.jct"
    listUrl = "https://www.citibank.co.kr/PbnEvntCnts0100.act?MENU_TYPE=left&MENU_C_SQNO=M5_004110&TYPE_CODE=ING"
    imgUrl = "https://www.citibank.co.kr/download/cms/evt/NEW_EVENT_BBS/"
    try :
        # 요청에 보낼 데이터 (JSON 형식)
        data = {
                    "NOW_PAGE":"1",
                    "REC_SZE":"10",
                    "TYPE_CODE":"ING",
                    "SRCH_DSCD":"00"
                }

        # 요청 헤더 (JSON 데이터 전송)
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

        # POST 요청 보내기
        response = requests.post(apiUrl, json=data, headers=headers)

        response.raise_for_status()  
        # 응답 출력
        # if response.status_code == 200:
        #     print("응답 데이터:", response.json())  # JSON 응답 출력
        # else:
        #     print(f"오류 발생: {response.status_code}", response.text)

        target_data = response.json()["REC"]

        for element in target_data:

            title = element.get("SUBJECT", "")
            startDt = element.get("EVNT_SYMD", "")
            endDt = element.get("EVNT_EYMD", "")
            thumbNail = f"{imgUrl}{element.get('FILENAME1', '')}"
            
            event_list.append({
                "title": title,
                "startDt": startDt,
                "endDt": endDt,
                "thumbNail": thumbNail,
                "listURL": listUrl
            })
    
        print(f"CITI은행 완료 | 이벤트 개수 : {len(event_list)}")
        # print("최종 결과 >>")
        print(event_list)
        return event_list
        
    except requests.exceptions.RequestException as e:
        print(f"CITI 오류 발생: {e}")
        return "Fail"


if __name__ == "__main__":
    asyncio.run(get027Data())
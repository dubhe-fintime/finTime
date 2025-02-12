import requests
import asyncio
import re
##############################
# 제목 : SC제일은행
# 금융사코드 : 023
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

##############################
# Service URL = "https://www.standardchartered.co.kr/np/kr/cm/et/selectEventStartList"
# Method = POST
##############################
# 목록
# {
#     "serviceID": "HP_AM_EV_EventBoard.selectEventStartList3",
#     "task": "com.scfirstbank.web.am.ev.task.HP_AM_EV_EventBoardTask",
#     "action": "selectEventStartList3",
#     "BULLTN_FLG_CD": "Z00001",
#     "START_NUM": "1",
#     "END_NUM": "100",
#     "SCH_FLAG": "",
#     "KEYWORD": ""
# }
##############################

async def get023Data():

    ######### 기초 설정 Start #############
    event_list = []
    apiUrl = "https://www.standardchartered.co.kr/np/kr/cm/et/selectEventStartList"
    listUrl = "https://www.standardchartered.co.kr/np/kr/cm/et/EventOngoingList.jsp"
    domainUrl = "https://www.standardchartered.co.kr"
    ######### 기초 설정 END ##############
    try :
        # 요청에 보낼 데이터 (JSON 형식)
        data = {
                    "serviceID": "HP_AM_EV_EventBoard.selectEventStartList3",
                    "task": "com.scfirstbank.web.am.ev.task.HP_AM_EV_EventBoardTask",
                    "action": "selectEventStartList3",
                    "BULLTN_FLG_CD": "Z00001",
                    "START_NUM": "1",
                    "END_NUM": "100",
                    "SCH_FLAG": "",
                    "KEYWORD": ""
                }

        # 요청 헤더 (JSON 데이터 전송)
        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }

        # POST 요청 보내기
        response = requests.post(apiUrl, json=data, headers=headers)

        response.raise_for_status()  
        # 응답 출력
        # if response.status_code == 200:
        #     print("응답 데이터:", response.json())  # JSON 응답 출력
        # else:
        #     print(f"오류 발생: {response.status_code}", response.text)

        target_data = response.json()["vector"]

        for element in target_data:

            output_data = element.get("OUTPUT", {})  # OUTPUT 키 가져오기 (없으면 빈 딕셔너리 반환)
            title = output_data.get("TTL", "제목 없음")
            startDt = "-".join(re.findall(r"\d+", output_data.get("BULLTN_DT", "")))
            endDt = "-".join(re.findall(r"\d+", output_data.get("END_DT", "")))
            thumbNail = f"{domainUrl}{output_data.get('BNNR_IMG_NM', '')}"
            
            # print(f"시작일 : {element['STRT_DT']}")
            # print(f"종료일 : {element['END_DT']}")
            # print(f"썸네일 : {thumbNail}")

            event_list.append({
                "title": title,
                "startDt": startDt,
                "endDt": endDt,
                "thumbNail": thumbNail,
                "listURL": listUrl
            })
    
        print(f"SC제일은행 완료 | 이벤트 개수 : {len(event_list)}")
        # print("최종 결과 >>")
        # print(event_list)
        return event_list
        
    except Exception as e:
        print(f"SC제일은행 오류 발생: {e}")
        return [{"ERROR": str(e)}]


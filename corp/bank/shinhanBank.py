import re
import requests

##############################
# 제목 : 신한은행
# 금융사코드 : 088
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

##############################
# Service URL = "https://www.shinhan.com/serviceEndpoint/httpDigital"
# Method = POST
##############################
# 목록
# {
#   "dataBody": {
#     "ricInptRootInfo": {
#       "serviceType": "TG",
#       "serviceCode": "THO0056",
#       "nextServiceCode": "",
#       "pkcs7Data": "",
#       "signCode": "",
#       "signData": "",
#       "useSign": "",
#       "useCert": "",
#       "permitMultiTransaction": "",
#       "keepTransactionSession": "",
#       "skipErrorMsg": "",
#       "mode": "",
#       "language": "ko",
#       "exe2e": "",
#       "hideProcess": "",
#       "clearTarget": "",
#       "callBack": "shbObj.fncDoTHO0056_Callback",
#       "exceptionCallback": "",
#       "requestMessage": "",
#       "responseMessage": "",
#       "serviceOption": "",
#       "pcLog": "",
#       "preInqForMulti": "",
#       "makesum": "",
#       "removeIndex": "",
#       "redirectUrl": "",
#       "preInqKey": "",
#       "_multi_transfer_": "",
#       "_multi_transfer_count_": "",
#       "_multi_transfer_amt_": "",
#       "userCallback": "",
#       "menuCode": "",
#       "certtype": "",
#       "fromMulti": "",
#       "fromMultiIdx": "",
#       "isRule": "Y",
#       "webUri": "/hpe/index.jsp",
#       "gubun": "",
#       "tmpField2": ""
#     },
#     "PAGE_CNT": "10",
#     "PAGE": "",
#     "EVNT_STAT_CD": "006_01",
#     "SCH_KEY": "",
#     "SCH_WORD": "",
#     "EVNT_GUBUN": ""
#   },
#   "dataHeader": {
#     "trxCd": "RSHRC0206A07",
#     "language": "ko",
#     "subChannel": "47",
#     "channelGbn": "D0"
#   }
# }
##############################

async def get088Data():
    ######### 기초 설정 Start #############
    event_list = []
    apiUrl = "https://www.shinhan.com/serviceEndpoint/httpDigital"
    listUrl = "https://www.shinhan.com/hpe/index.jsp#902304010000"
    ######### 기초 설정 END ##############

    try :
        # 요청에 보낼 데이터 (JSON 형식)
        data = {
                    "dataBody": {
                        "ricInptRootInfo": {
                        "serviceType": "TG",
                        "serviceCode": "THO0056",
                        "nextServiceCode": "",
                        "pkcs7Data": "",
                        "signCode": "",
                        "signData": "",
                        "useSign": "",
                        "useCert": "",
                        "permitMultiTransaction": "",
                        "keepTransactionSession": "",
                        "skipErrorMsg": "",
                        "mode": "",
                        "language": "ko",
                        "exe2e": "",
                        "hideProcess": "",
                        "clearTarget": "",
                        "callBack": "shbObj.fncDoTHO0056_Callback",
                        "exceptionCallback": "",
                        "requestMessage": "",
                        "responseMessage": "",
                        "serviceOption": "",
                        "pcLog": "",
                        "preInqForMulti": "",
                        "makesum": "",
                        "removeIndex": "",
                        "redirectUrl": "",
                        "preInqKey": "",
                        "_multi_transfer_": "",
                        "_multi_transfer_count_": "",
                        "_multi_transfer_amt_": "",
                        "userCallback": "",
                        "menuCode": "",
                        "certtype": "",
                        "fromMulti": "",
                        "fromMultiIdx": "",
                        "isRule": "Y",
                        "webUri": "/hpe/index.jsp",
                        "gubun": "",
                        "tmpField2": ""
                        },
                        "PAGE_CNT": "10",
                        "PAGE": "",
                        "EVNT_STAT_CD": "006_01",
                        "SCH_KEY": "",
                        "SCH_WORD": "",
                        "EVNT_GUBUN": ""
                    },
                    "dataHeader": {
                        "trxCd": "RSHRC0206A07",
                        "language": "ko",
                        "subChannel": "47",
                        "channelGbn": "D0"
                    }
                }

        # 요청 헤더 (JSON 데이터 전송)
        headers = {
            "Content-Type": "application/json"
        }

        # POST 요청 보내기
        response = requests.post(apiUrl, json=data, headers=headers)
        response.raise_for_status()  

        target_data = response.json()["dataBody"]["RESULT"]

        for element in target_data:
            start_date, end_date = [re.sub(r"(\d{4})(\d{2})(\d{2}).*$", r"\1-\2-\3", x) for x in [element['STRT_DT'], element['END_DT']]]

            event_list.append({
                "title": element['TITLE'],
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": element['H_ICON'],
                "listURL": listUrl
            })
    
        print(f"신한은행 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list
        
    except Exception as e:
        print(f"신한은행 오류 발생: {e}")
        return [{"ERROR": str(e)}]


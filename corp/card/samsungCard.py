import re
import requests

##############################
# 제목 : 삼성카드
# 금융사코드 : 365
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

##############################
# Service URL = "https://www.samsungcard.com/frontservice/SHPPBE1401S02"
# Method = POST
##############################

async def get365Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://www.samsungcard.com/frontservice/SHPPBE1401S02"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 목록 URL 
    list_domain =  "https://www.samsungcard.com/personal/event/ing/UHPPBE1401M0.jsp"
    # 상세 URL 
    detail_domain =  "https://www.samsungcard.com/personal/event/ing/UHPPBE1403M0.jsp?cms_id="
    ######### 기초 설정 END ##############

    try:
        body = {
            "cmpId": "M171028654",
            "query": "",
            "cmpCtgId": "100",
            "pgeNo": 0,
            "enddtAdvtYn": 0,
            "onGoing": "1",
            "common": {
                "scrnId": "UHPPBE1401M0",
                "stdEtxtCrtSysNm": "P2585108",
                "stdEtxtSn": "09180421900002",
                "stdEtxtPrgDvNo": 0,
                "stdEtxtPrgNo": 0,
                "usid": "USERID0"
            }
        }
        # 웹페이지 요청
        response = requests.post(url,json=body)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()["listPeiHPPPrgEvnInqrDVO"]
        
        for element in target_data:
            start_date, end_date = [re.sub(r"(\d{4})(\d{2})(\d{2})", r"\1-\2-\3", x) for x in [element['cmsCmpStrtdt'], element['cmsCmpEnddt']]]

            event_list.append({
                "title": element['cmpTitNm'],
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": 'https:'+element['newMblThmnlImgNm'],
                "listURL": list_domain,
                "detailURL": detail_domain+str(element['cmsId'])
            })

            #  확인용
            # print(f"제목 : {element['cmpTitNm']}")
            # print(f"시작 : {start_date}")
            # print(f"종료 : {end_date}")
            # print(f"썸네일 : {'https:'+element['newMblThmnlImgNm']}")
            # print(f"목록URL : {list_domain}")
            # print(f"상세URL : {detail_domain+str(element['cmsId'])}")

        print(f"삼성카드 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list

    except Exception as e:
        print(f"삼성카드 오류 발생: {e}")
        return [{"ERROR": str(e)}]





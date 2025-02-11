import re
import requests

##############################
# 제목 : 신한카드
# 금융사코드 : 366
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################


##############################
# Service URL = "https://www.shinhancard.com/logic/json/evnPgsList01.json"
# Method = GET
##############################


async def get366Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    #url =  "https://www.shinhancard.com/logic/json/evnPgsList01.json?v=1739230112327"
    url =  "https://www.shinhancard.com/logic/json/evnPgsList01.json"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 목록 URL 기본값
    list_domain =  "https://www.shinhancard.com/mob/MOBFM026N/MOBFM026C01.shc"
    ######### 기초 설정 END ##############

    try:
        # 웹페이지 요청
        response = requests.get(url)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()['root']['evnlist']
        
        for element in target_data:
            event_list.append({
                "title": element['mobWbEvtNm'],
                "thumbNail": domain+element['hpgEvtCtgImgUrlAr'],
                "startDt": element['mobWbEvtStd'],
                "endDt": element['mobWbEvtEdd'],
                "listURL": list_domain,
                "detailURL": domain+element['hpgEvtDlPgeUrlAr']
            })

        print(f"신한카드 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list

    except Exception as e:
        print(f"신한카드 오류 발생: {e}")
        return [{"ERROR": e}]






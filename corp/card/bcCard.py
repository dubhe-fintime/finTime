import re
import requests

##############################
# 제목 : BC카드
# 금융사코드 : 361
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

##############################
# Service URL = "https://web.paybooc.co.kr/web/evnt/lst-evnt-data?reqType=init&inqrDv=ING&evntMrktTypCd=&ordering=RECENT&inqrDvMonth=&_=1739234504857"
# Method = "GET"
##############################

async def get361Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://web.paybooc.co.kr/web/evnt/lst-evnt-data"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 목록 URL 
    list_domain =  "https://web.paybooc.co.kr/web/evnt/main#link"
    # 상세 URL 
    detail_domain =  "https://web.paybooc.co.kr/web/evnt/evnt-dts?pybcUnifEvntNo="
    ######### 기초 설정 END ##############

    try:
        params = {
            "reqType": "init",
            "inqrDv": "ING",
            "evntMrktTypCd": "",
            "ordering": "RECENT",
            "inqrDvMonth": "",
            "_": "1739234504857"
        }
        # 웹페이지 요청
        response = requests.get(url,params=params)
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()["data"]["evntInqrList"]
        for element in target_data:
            start_date, end_date = [re.sub(r"(\d{4})(\d{2})(\d{2}).*$", r"\1-\2-\3", x) for x in [element['evntBltnStrtDtm'], element['evntBltnEndDtm']]]

            title = " ".join([
                element['pybcUnifEvntNm1'],
                element['pybcUnifEvntNm2'],
                element['pybcUnifEvntNm3']
            ])

            event_list.append({
                "title": title,
                "startDt": start_date,
                "endDt": end_date,
                "thumbNail": element['evntBsImgUrlAddr'],
                "listURL": list_domain,
                "detailURL": detail_domain+str(element['pybcUnifEvntNo'])
            })

            #  확인용
            # print(f"제목 : {title}")
            # print(f"시작 : {start_date}")
            # print(f"종료 : {end_date}")
            # print(f"썸네일 : {element['evntBsImgUrlAddr']}")
            # print(f"목록URL : {list_domain}")
            # print(f"상세URL : {detail_domain+str(element['pybcUnifEvntNo'])}")

        print(f"BC카드 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list

    except Exception as e:
        print(f"BC카드 오류 발생: {e}")
        return [{"ERROR": str(e)}]




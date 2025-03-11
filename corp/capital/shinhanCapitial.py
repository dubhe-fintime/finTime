import requests

##############################
# 제목 : 신한캐피탈
# 금융사코드 : 901
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

async def get901Data():
    ######### 기초 설정 Start #############
    event_list = []
    apiUrl_2 = "https://www.shcap.co.kr/cc/CC030101R01.do"
    listUrl = "https://www.shcap.co.kr/cc/CC030101.do"
    imgUrl = "https://www.shcap.co.kr/util/loadImg.do?propertyKey=BOARD_PATH&partFilePath="
    ######### 기초 설정 END ##############
    try :

        # 요청 헤더 (JSON 데이터 전송)
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://www.shcap.co.kr",
            "Referer": "https://www.shcap.co.kr/cc/CC030101.do",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
        }

        data= {"MENU_ID_DVCD": "MO010016","currentPage": 1,"pageUnit": 4}

        # POST 요청 보내기
        response = requests.post(apiUrl_2, headers=headers,json=data)
        file_path = response.json()["result"]["filePath"]
        target_data = response.json()["result"]["rstData"]

        for element in target_data:
            event_list.append({
                "title": element['BULL_TTL'],
                "startDt": element["BULL_STRN_DT"],
                "endDt": element["BULL_END_DT"],
                "thumbNail": imgUrl+file_path+"&fileName="+element['ATFL_NM3'],
                "listURL": listUrl
            })
    
        print(f"신한캐피탈 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list
        
    except Exception as e:
        print(f"신한캐피탈 오류 발생: {e}")
        return [{"ERROR": str(e)}]

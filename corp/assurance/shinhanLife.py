import requests

##############################
# 제목 : 신한라이프생명보험
# 금융사코드 : 438
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

async def get438Data():
    event_list = []
    url = "https://www.shinhanlife.co.kr/hp/fav/selectListEvnt.pwkjson"

    headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Content-Type": "application/json; charset=UTF-8",
    "Cookie": "WMONID=s9BBeNcKuIa; JSESSIONID=J5zFEQ3GP4gSw3staUcL1tzwzXWLo9THeykOvGsH889iphF3vktq6k1NOsFKGLWg.ZG1fY2RjL21zX2NkY0NkaDIx; frstDpCnntLogId=202503619076690; _ga=GA1.1.695658526.1741651746; TS01feae25=01f905587f9d6c497e8c3db2bcc3d6bc76878b8c0f22e1f44fc5c756737fe57ee2b977c6b14b241d41fced138d26ed38303921d136; _ga_6C7W34G0K8=GS1.1.1741651745.1.1.1741652125.0.0.0",
    "Host": "www.shinhanlife.co.kr",
    "Origin": "https://www.shinhanlife.co.kr",
    "Proworks-Body": "Y",
    "Proworks-Lang": "ko",
    "Referer": "https://www.shinhanlife.co.kr/hp/cdhg0020.do",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "X-AJAX-CALL": "true",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows"
    }
    
    payload = {
        "elData": {
            "pageSize": 6,
            "pageIndex": 1,
            "prstCd": "01",
            "appliDutjCd": "DH1",
            "scrnId": "cdhg0020"
        },
        "userHeader": {
            "scrnId": "cdhg0020",
            "appliDtptDutjCd": "DH"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
        data = response.json()
        events = data.get("elData", {}).get("evntVoList", [])
        for event in events:
            event_list.append({
                "title": event.get("evntTitlNm", ""),
                "startDt": event.get("evntStrtDt", ""),
                "endDt": event.get("evntEndDt", ""),
                "thumbNail": f"https://www.shinhanlife.co.kr/{event.get('evntImagUrlAddr', '')}",
                "listURL": "https://www.shinhanlife.co.kr/hp/cdhg0020.do",
                "detailURL": f"https://www.shinhanlife.co.kr/hp/cdhg0030.do?dpEvntId={event.get('dpEvntId', '')}"
            })
        
        print(f"신한라이프 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        print(event_list)
        return event_list
    
    except requests.exceptions.RequestException as e:
        print(f"신한라이프 요청 오류 발생: {e}")
        return [{"ERROR": str(e)}]

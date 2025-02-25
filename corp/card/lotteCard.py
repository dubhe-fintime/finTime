import requests
from bs4 import BeautifulSoup

async def get368Data():
    url = "https://www.lottecard.co.kr/app/LPBNFDA_A100.lc"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://www.lottecard.co.kr",
        "Referer": "https://www.lottecard.co.kr/app/LPBNFDA_V100.lc",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    data = {
        "pageNo": "3",
        "bigTabGubun": "2",
        "tabGubun": "9999",
        "evnBultSeq": "",
        "finishYn": "N",
        "sort": "EVN_BULT_SDT",
        "evnTc": "",
        "evnCtgSeq": "9999"
    }

    cookies = {
        "TLTSID": "0015C8ECF31410F332DFAC490F16600D",
        "TLTUID": "0015C8ECF31410F332DFAC490F16600D",
        "COHSESSIONID": "-BEk8XVtaZWpy0PKjOqgZ0N39uaKPM30Lz_OOxWS.locaid",
        "WHATAP": "z14dv73plhek6i",
        "_ga": "GA1.1.816780266.1740445299",
        "wcs_bt": "s_1f0b82dcd5c7:1740445299"
    }

    try:
        response = requests.post(url, headers=headers, data=data, cookies=cookies)

        if response.status_code == 200:
            response_data = response.json()
            soup = BeautifulSoup(response_data["Content"], "html.parser")
            
            events = []
            
            # 이벤트 정보 추출
            for li in soup.find_all("li"):
                event_list = {}
                title_tag = li.find("b")
                date_tag = li.find("span", class_="date")
                img_tag = li.find("img")
                a_tag = li.find("a", href=True)
                
                event_list["title"] = title_tag.text.strip() if title_tag else "제목 없음"
                event_list["startDt"], event_list["endDt"] = date_tag.text.strip().split(" ~ ") if date_tag else ("알 수 없음", "알 수 없음")
                event_list["thumbNail"] = img_tag["src"] if img_tag else "이미지 없음"
                event_list["thumbNail"] = "https:"+event_list["thumbNail"]

                # event_cd 추출 부분 수정
                event_url = a_tag["href"] if a_tag else ""
                if event_url:
                    try:
                        event_list["event_cd"] = event_url.replace("javascript:tlfLoad(", "").split(",")[2].strip("'")
                    except IndexError:
                        event_list["event_cd"] = "URL 없음"
                else:
                    event_list["event_cd"] = "URL 없음"
                
                event_list["listURL"] = "https://www.lottecard.co.kr/app/LPBNFDA_V100.lc"
                event_list["detailURL"] = f"https://www.lottecard.co.kr/app/LPBNFDA_V300.lc?evnBultSeq={event_list['event_cd']}&evnCtgSeq=9999&bigTabGubun=2"
                
                events.append(event_list)  # 이벤트 리스트에 추가

            print(events)
            print(f"롯데카드 크롤링 완료 | 이벤트 개수 : {len(events)}")
            return events
        else:
            print(f"롯데카드 오류 발생: {response.status_code}")
            return [{"ERROR": "접속불가"}]
    except Exception as e:
        print(f"롯데카드 오류 발생: {e}")
        return [{"ERROR": str(e)}]

# 호출
get368Data()

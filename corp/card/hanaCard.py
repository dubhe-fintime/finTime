import re
import requests
import ssl
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

##############################
# 제목 : 하나카드
# 금융사코드 : 374
# 방식 : BeautifulSoup
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : O
##############################

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")  # 보안 수준 낮춤
        context.check_hostname = False  # SSL 인증서 검증 비활성화
        kwargs["ssl_context"] = context
        super().init_poolmanager(*args, **kwargs)

async def get374Data():

    ######### 기초 설정 Start #############
    event_list = []
    url = "https://www.hanacard.co.kr/OPP35000000D.web"  # 크롤링 대상 URL
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    detail_domain = "https://www.hanacard.co.kr/OPP35000001D.web?schID=ncd&mID=OPP35000001D&EVN_SEQ="
    ######### 기초 설정 END ##############

    try:
        session = requests.Session()
        session.mount("https://", TLSAdapter())  # HTTPS 요청에 TLSAdapter 적용

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        # 웹페이지 요청
        response = session.get(url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()  # 응답 오류 발생 시 예외 처리
        soup = BeautifulSoup(response.text, 'html.parser')

        # 찾기
        container = soup.find("ul", class_="thumb_ty")
        if not container:
            raise ValueError("목록을 찾을 수 없습니다. HTML 구조가 변경되었을 가능성이 있습니다.")

        for element in container.find_all("li"):
            try:
                date_text = element.find("div", class_="txt").find("p", class_="s2").text.replace(".", "-")
                start_date, end_date = re.findall(r'\d{4}-\d{2}-\d{2}', date_text)

                filtering_temp = re.search(r"goView\('(\d+)'", element.find("a")["href"])
                detail_target = filtering_temp.group(1) if filtering_temp else ""

                event_list.append({
                    "title": element.find("div", class_="txt").find("dt").text.strip(),
                    "startDt": start_date,
                    "endDt": end_date,
                    "thumbNail": domain + element.find("img")["src"],
                    "listURL": url,
                    "detailURL": detail_domain + detail_target
                })
            except AttributeError:
                print("일부 항목을 찾을 수 없습니다. 건너뜁니다.")

        print(f"하나카드 크롤링 완료 | 이벤트 개수: {len(event_list)}")
        return event_list

    except requests.exceptions.RequestException as e:
        print(f"하나카드 요청 오류 발생: {e}")
    except Exception as e:
        print(f"하나카드 크롤링 오류 발생: {e}")

    return [{"ERROR": str(e)}]

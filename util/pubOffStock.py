import ssl
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
from flask import Flask, jsonify

app = Flask(__name__)

# 기본 URL
base_url = "https://www.38.co.kr/html/fund/index.htm?o=k&page="

# 요청 헤더 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

async def pubOffStock():
    try:
        # 데이터 리스트
        ipo_list = []

        # 페이지 번호
        page = 1
        while True:
            url = base_url + str(page)
            
            # SSL context 설정
            ssl_context = ssl.create_default_context()
            ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')  # 보안 레벨 낮추기

            async with aiohttp.ClientSession() as session:
                # ssl_context를 session에 전달
                async with session.get(url, headers=headers, ssl=ssl_context) as response:
                    if response.status != 200:
                        break  # HTTP 오류 발생 시 종료
                    html = await response.text()

            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", summary="공모주 청약일정")

            if not table:
                break  # 더 이상 데이터가 없으면 중지

            rows = table.find_all("tr")[2:]  # 첫 번째 헤더와 구분선 제외
            if not rows:
                break  # 더 이상 데이터가 없으면 중지
            
            page_data = []
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 6:
                    # 공모주 일정 분리 및 년도 추가
                    date_range = cols[1].text.strip()
                    start_date, end_date = date_range.split("~") if "~" in date_range else (date_range, "")
                    start_date = start_date.strip()
                    end_date = end_date.strip()

                    # 종료일에 년도 추가 (시작일의 년도를 기준으로 설정)
                    if end_date and len(end_date) == 5:  # MM.DD 형식일 경우
                        year = start_date.split(".")[0]  # 시작일에서 년도 추출
                        end_date = f"{year}.{end_date}"

                    # 금액에서 , 제거
                    confirmed_price = cols[2].text.strip().replace(",", "")
                    desired_price = cols[3].text.strip().replace(",", "")

                    data = {
                        "STOCK_NM": cols[0].text.strip(),  # 종목명
                        "SUB_ST_DATE": start_date,  # 청약 시작일
                        "SUB_ED_DATE": end_date,  # 청약 종료일
                        "CON_PUB_OFF_PRICE": confirmed_price,  # 확정 공모가
                        "HOPE_PUB_OFF_PRICE": desired_price,  # 희망 공모가
                        "SUB_COM_RATE": cols[4].text.strip(),  # 청약 경쟁률
                        "CHIEF_EDITOR": cols[5].text.strip(),  # 주간사
                    }

                    page_data.append(data)

            if not page_data:
                break  # 페이지에 데이터가 없으면 중지

            ipo_list.extend(page_data)
            page += 1

        # JSON 변환
        json_data = json.dumps(ipo_list, ensure_ascii=False, indent=4)

        return json_data
    except Exception as e:
        print(f"청약공모주 오류 발생: {e}")
        return [{"ERROR": str(e)}]
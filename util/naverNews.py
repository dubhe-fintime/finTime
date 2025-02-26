import sys
import os
import re
import requests
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import dbconn

##############################
# 제목 : 네이버 기사 수집
# 방식 : API (GET)
# 수집 데이터
# 언론사 이름 | 언론사 썸네일 | 기사 제목 | 기사 첫줄 | 기사 URL
##############################


async def get_recent_news(targets: list):
    session = requests.Session()
    cor_gp = dbconn.execute_mysql_query_select("Q22",(targets))
    event_list = []
    url = "https://search.naver.com/search.naver"
    pattern = r"(?<=[\uac00-\ud7af])\."
    # try:
    for target in targets:
        client_id = "BXpwyrG2dsvqVniOAIBI"
        client_secret = "dc9cDMiTL3"

        header = {
            "X-Naver-Client-Id":client_id,
            "X-Naver-Client-Secret":client_secret
        }

        params = {
            "where": "news",
            "query": target
        }
        # 웹페이지 요청
        response = requests.get(url, params=params,headers=header)
        soup = BeautifulSoup(response.text, "html.parser")
        container = soup.find("ul", class_="list_news")

        for element in container.find_all("li", class_="bx")[:5]:
            result = re.split(pattern, element.find("div", class_="dsc_wrap").text.strip())
            content_data = result[1] if len(result[0]) < 10 else result[0]

            cor_no = next((item[0] for item in cor_gp if item[1] == target), None)

            event_list.append({
                "press_name": element.find("a", class_=["info", "press"]).text,
                "press_img": element.find("img")["data-lazysrc"],
                "article_title": element.find("a", class_="news_tit").text,
                "article_content": content_data,
                "URL": element.find("a", class_="news_tit")["href"],
                "search_term": cor_no
            })
            
    return event_list


        


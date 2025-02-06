from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

async def get433Data():
    url = "https://www.kyobo.com/dgt/web/event/event-ongoing"

    # 브라우저 설정 (백그라운드 실행)
    options = Options()
    options.add_argument("--headless")  # 창을 띄우지 않음
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Selenium WebDriver 실행
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(1)  # JavaScript가 데이터를 로드할 시간을 줌

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # 브라우저 닫기

    # 이벤트 리스트 찾기
    event_list_html = soup.find(id="ingEventList")
    print("HTML 내용: " + str(event_list_html))
    if not event_list_html:
        print("이벤트 리스트를 찾을 수 없습니다.")
        return []

    events = event_list_html.find_all("li")

    event_list = []
    print(f"이벤트 [433] 개수 : {len(events)}")

    for event in events:
        title_tag = event.find("strong", class_="tit")
        date_tag = event.find("div", class_="period")
        img_tag = event.find("div", class_="thumb").find("img")

        if title_tag and date_tag and img_tag:
            title = title_tag.text.strip()
            date = date_tag.text.strip()
            img_url = img_tag.get("src")

            event_list.append({
                "title": title,
                "date": date,
                "img_url": img_url
            })

            print(f"이벤트명: {title}")
            print(f"이벤트 기간: {date}")
            print(f"이미지 URL: {img_url}")
            print("-")

    return event_list
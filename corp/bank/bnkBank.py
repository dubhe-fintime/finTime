from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# 크롬 드라이버 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저를 띄우지 않고 실행
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 크롬 드라이버 실행
service = Service("/usr/bin/chromedriver")  # Chromedriver 경로 수정 필요
driver = webdriver.Chrome(service=service, options=chrome_options)

# 페이지 이동할 URL
BASE_URL = "https://www.busanbank.co.kr/ib20/mnu/BHPBKI393002005"
driver.get(BASE_URL)

# 크롤링할 데이터 리스트
events = []
page = 1
prev_event_list = set()  # 이전 페이지 이벤트 저장용

while True:
    print(f"📌 페이지 {page} 크롤링 중...")

    # 페이지 소스 가져오기
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # 이벤트 리스트 추출
    event_list = soup.select("ul.event-list > li")

    # 현재 페이지 이벤트를 집합(set)으로 변환하여 비교
    current_event_set = set(event.text.strip() for event in event_list)

    if not event_list:
        print("✅ 모든 페이지 크롤링 완료!")
        break  # 더 이상 데이터가 없으면 종료

    # 이전 페이지와 데이터가 같으면 크롤링 종료
    if prev_event_list == current_event_set:
        print("✅ 같은 데이터가 반복됨! 크롤링 종료")
        break

    # 현재 이벤트 데이터를 저장
    prev_event_list = current_event_set

    for event in event_list:
        try:
            title_tag = event.select_one("a.tit")
            date_tag = event.select_one("span.term")
            img_tag = event.select_one("img")
            seq = title_tag["seq"] if title_tag else "알 수 없음"

            event_data = {
                "title": title_tag.text.strip() if title_tag else "제목 없음",
                "startDt": date_tag.text.split(" ~ ")[0].split("이벤트기간 : ")[1] if date_tag else "알 수 없음",
                "endDt": date_tag.text.split(" ~ ")[1] if date_tag else "알 수 없음",
                "thumbNail": "https://www.busanbank.co.kr" + img_tag["src"] if img_tag else "이미지 없음",
                "detailURL": f"https://www.busanbank.co.kr/event/detail?seq={seq}"
            }

            events.append(event_data)
        except Exception as e:
            print("❌ 오류 발생:", e)

    # 다음 페이지 버튼 클릭
    try:
        next_button = driver.find_element(By.CLASS_NAME, "direction.next")
        if "disabled" in next_button.get_attribute("class"):
            print("✅ 마지막 페이지 도달! 크롤링 종료")
            break
        next_button.click()
        time.sleep(2)  # 페이지 로드 대기
    except:
        print("✅ 더 이상 다음 페이지가 없습니다.")
        break

    page += 1  # 다음 페이지로 이동

# 드라이버 종료
driver.quit()

print(f"🎉 총 {len(events)}개의 이벤트 데이터를 수집 완료!")

# 결과 출력
for event in events:
    print(event)

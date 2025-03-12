import asyncio
import time
import datetime
import schedule
import os
import random
from main import set_batch_news, set_batch_log, del_batch_rst, app
from util import naverNews
from dbconn import execute_mysql_query_delete

BATCH_ID = "B000000003"  # 유튜브 배치 ID
BATCH_NM = "네이버 뉴스 최신 기사 수집"

# 비동기 작업 함수
async def naver_batch_job():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)  # logs 폴더가 없으면 생성

    today = datetime.datetime.now().strftime("%Y%m%d")
    log_file_path = os.path.join(log_dir, f"naver_batch_log_{today}.log")

    now = datetime.datetime.now()
    random_number = random.randint(100000, 999999)
    print(f"[{now}] 네이버뉴스 배치 작업 실행 중... 함수번호[{random_number}]")

    try:
        with app.app_context():
            results = await naverNews.get_recent_news(["신한은행","하나은행","우리은행","국민은행","신한카드","신한투자증권","신한캐피탈"])  # <<<<< 원하는 은행,증권사 오타없이
            task_time = datetime.datetime.now()
            
            if results :
                status = "SUCCESS"
                cnt = 0  # 정상 처리된 데이터 개수
                execute_mysql_query_delete("Q27","")
                for data in results:
                    set_batch_news(
                        data.get('press_name', ""),
                        data.get('press_img', ""),
                        data.get('article_title', ""),
                        data.get('article_content', ""),
                        data.get('URL', ""),
                        data.get('search_term', "")
                    )
                    cnt += 1
            else:
                status = "FAIL"

            # 배치 로그 저장
            set_batch_log(BATCH_ID, BATCH_NM, "TN00000001", "getNaverNews", now, task_time, status, str(results),random_number)

            # 로그 파일 저장
            log_message = f"[{task_time}] getNaverNews 실행 완료 - 상태: {status}, 데이터 개수: {cnt}"
            with open(log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(log_message + "\n")

    except Exception as e:
        error_message = f"[{now}] 네이버뉴스 배치 실행 중 오류 발생: {e}"
        print(error_message)
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(error_message + "\n")

# 배치 실행 함수
def run_naver_batch_job():
    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(naver_batch_job())  # 비동기 실행

    except Exception as e:
        print(f"네이버뉴스 배치 작업 실행 중 오류 발생: {e}")

# 매일 03:00에 실행
schedule.every().day.at("11:00").do(run_naver_batch_job)
# schedule.every(1).minutes.do(run_naver_batch_job)

print(f"네이버뉴스 배치 작업이 스케줄링되었습니다. (매일 03:00 실행)")

# 무한 루프 실행 (배치 스케줄 유지)
while True:
    schedule.run_pending()
    time.sleep(60)  # 1분마다 체크

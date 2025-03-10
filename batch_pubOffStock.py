import asyncio
import time
import datetime
import schedule
import os
import random
from main import set_batch_pubOffStock, set_batch_log,  app
from main import getPubOffStockData
from dbconn import execute_mysql_query_delete

BATCH_ID = "B000000004"  # 공모주일정
BATCH_NM = "공모주 일정 수집"

# 비동기 작업 함수
async def pubOffStock_batch_job():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)  # logs 폴더가 없으면 생성

    today = datetime.datetime.now().strftime("%Y%m%d")
    log_file_path = os.path.join(log_dir, f"pubOffStock_batch_log_{today}.log")

    now = datetime.datetime.now()
    random_number = random.randint(100000, 999999)
    print(f"[{now}] 공모주 정보 배치 작업 실행 중... 함수번호[{random_number}]")

    try:
        with app.app_context():
            results = await getPubOffStockData()
            task_time = datetime.datetime.now()
            
            if results :
                res = results.json()
                status = "SUCCESS"
                cnt = 0  # 정상 처리된 데이터 개수
                ############################################## 여기까지 했음
                execute_mysql_query_delete("Q29","")
                for data in res:
                    set_batch_pubOffStock(
                        data.get('STOCK_NM', ""),
                        data.get('SUB_ST_DATE', ""),
                        data.get('SUB_ED_DATE', ""),
                        data.get('CON_PUB_OFF_PRICE', ""),
                        data.get('HOPE_PUB_OFF_PRICE', ""),
                        data.get('SUB_COM_RATE', ""),
                        data.get('CHIEF_EDITOR', "")
                    )
                    cnt += 1
            else:
                status = "FAIL"

            # 배치 로그 저장
            set_batch_log(BATCH_ID, BATCH_NM, "TP00000001", "pubOffStock", now, task_time, status, str(results),random_number)

            # 로그 파일 저장
            log_message = f"[{task_time}] pubOffStock 실행 완료 - 상태: {status}, 데이터 개수: {cnt}"
            with open(log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(log_message + "\n")

    except Exception as e:
        error_message = f"[{now}] 공모주 정보 배치 실행 중 오류 발생: {e}"
        print(error_message)
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(error_message + "\n")

# 배치 실행 함수
def run_pubOffStock_batch_job():
    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(pubOffStock_batch_job())  # 비동기 실행

    except Exception as e:
        print(f"공모주 정보 배치 작업 실행 중 오류 발생: {e}")

# 매일 03:00에 실행
schedule.every().day.at("03:00").do(run_pubOffStock_batch_job)
# schedule.every(1).minutes.do(run_naver_batch_job)

print(f"공모주 정보 배치 작업이 스케줄링되었습니다. (매일 03:00 실행)")

# 무한 루프 실행 (배치 스케줄 유지)
while True:
    schedule.run_pending()
    time.sleep(60)  # 1분마다 체크

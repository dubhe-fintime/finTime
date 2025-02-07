import asyncio
import time
import datetime
import schedule
import os
from main import test, test2, test3, test4, test5, test6, app  # Flask 앱을 임포트

# 비동기 작업 함수
async def my_batch_job():
    # logs 폴더 경로 설정 (현재 실행 경로의 한 단계 위)
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)  # logs 폴더가 없으면 생성

    log_file_path = os.path.join(log_dir, "batch_log.txt")
    now = datetime.datetime.now()
    print(f"[{now}] 배치 작업 실행 중...")

    # 실행할 작업 정의
    tasks = {
        "test": test(),
        "test2": test2(),
        "test3": test3(),
        "test4": test4(),
        "test5": test5(),
        "test6": test6()
    }

    try:
        with app.app_context():
            # 비동기 작업 실행
            task_futures = {name: asyncio.create_task(func) for name, func in tasks.items()}
            responses = await asyncio.gather(*task_futures.values(), return_exceptions=True)

            # 응답 처리 및 로그 기록
            for (task_name, response) in zip(task_futures.keys(), responses):
                task_time = datetime.datetime.now()

                if isinstance(response, Exception):
                    log_message = f"[{task_time}] {task_name} 실행 실패: {response}"
                else:
                    res = response.get_json()
                    status = "SUCCESS" if res['status_code'] == 200 else "FAIL"
                    log_message = f"[{task_time}] {task_name} 실행 완료 - 상태: {status}, 응답: {res['result']}"

                print(log_message)

                # 로그 파일 저장
                with open(log_file_path, "a", encoding="utf-8") as log_file:
                    log_file.write(log_message + "\n")

    except Exception as e:
        print(f"[{now}] 배치 실행 중 오류 발생: {e}")

def run_batch_job():
    try:
        loop = asyncio.get_event_loop()

        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(my_batch_job())  # 비동기 함수 실행
    except Exception as e:
        print(f"배치 작업 실행 중 오류 발생: {e}")

# 매일 1분마다 실행하도록 설정
schedule.every(1).minutes.do(run_batch_job)

print("배치 작업이 스케줄링되었습니다. (매일 1분마다 실행)")

# 무한 루프 실행 (배치 스케줄 유지)
while True:
    schedule.run_pending()
    time.sleep(1)  # 1초마다 스케줄 체크

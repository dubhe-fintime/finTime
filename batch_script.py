import asyncio
import time
import datetime
import schedule
from main import test, test2, app  # Flask 앱을 임포트

# 비동기 작업 함수
async def my_batch_job():
    now = datetime.datetime.now()
    print(f"[{now}] 배치 작업 실행 중...")

    try:
        # Flask 애플리케이션 컨텍스트 설정
        with app.app_context():
            # 비동기 작업을 병렬로 실행
            tasks = [
                asyncio.create_task(test()),
                asyncio.create_task(test2())
            ]

            # 모든 비동기 작업이 끝날 때까지 대기
            responses = await asyncio.gather(*tasks)

            # 응답 처리
            for response in responses:
                res = response.get_json()  # 응답에서 JSON 데이터 추출
                print(res)

                if res['status_code'] == 200:
                    print(f"[{now}] 배치 실행 성공: {res['result']}")
                else:
                    print(f"[{now}] 배치 실행 실패 (Status Code: {res['status_code']})")

                # 실행 로그 저장
                with open("batch_log.txt", "a", encoding="utf-8") as log_file:
                    log_file.write(f"[{now}] 배치 실행 완료 - 응답: {res['result']}\n")

    except Exception as e:
        print(f"[{now}] 배치 실행 중 오류 발생: {e}")

def run_batch_job():
    """배치 작업을 비동기적으로 실행하는 함수"""
    try:
        loop = asyncio.get_event_loop()

        # 이벤트 루프가 닫혔을 경우 새로운 루프 생성
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(my_batch_job())  # 비동기 함수 실행
    except Exception as e:
        print(f"배치 작업 실행 중 오류 발생: {e}")


# 매일 10분마다 실행하도록 설정
schedule.every(1).minutes.do(run_batch_job)

print("배치 작업이 스케줄링되었습니다. (매일 1분마다 실행)")

# 무한 루프 실행 (배치 스케줄 유지)
while True:
    schedule.run_pending()
    time.sleep(1)  # 1초마다 스케줄 체크

import asyncio
import time
import datetime
import schedule
import os
import random
from main import set_batch_youtube, set_user_mapp, set_batch_log, app
from main import getYouTube  # 유튜브 데이터 가져오는 함수 임포트

BATCH_ID = "B000000002"  # 유튜브 배치 ID
BATCH_NM = "유튜브 데이터 수집 배치"

# 비동기 작업 함수
async def youtube_batch_job():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)  # logs 폴더가 없으면 생성

    today = datetime.datetime.now().strftime("%Y%m%d")
    log_file_path = os.path.join(log_dir, f"youtube_batch_log_{today}.log")

    now = datetime.datetime.now()
    random_number = random.randint(100000, 999999)
    print(f"[{now}] 유튜브 배치 작업 실행 중... 함수번호[{random_number}]")

    try:
        with app.app_context():
            response = await getYouTube()  # 유튜브 데이터 가져오기
            
            if callable(response.json):
                response_json = response.json()
            else:
                response_json = response.json

            if not isinstance(response_json, dict):
                raise ValueError(f"예상치 못한 데이터 형식: {type(response_json)}, 데이터: {response_json}")

            success = response_json.get("success", False)
            results = response_json.get("results", [])
            corNm = response_json.get("corNm", [])

            if not isinstance(results, list):
                raise TypeError(f"results 데이터 형식 오류: {type(results)}")
            
            # 결과를 펼치는 로직 추가
            flat_results = []
            for item in results:
                if isinstance(item, list):  # 리스트 내부 리스트가 있으면 펼치기
                    flat_results.extend(item)
                elif isinstance(item, dict):  # 올바른 dict라면 추가
                    flat_results.append(item)
                else:
                    raise TypeError(f"잘못된 데이터 형식: {type(item)}, 데이터: {item}")

            task_time = datetime.datetime.now()
            
            if success:
                status = "SUCCESS"
                cnt = 0  # 정상 처리된 데이터 개수
                print(flat_results)

                for channel in flat_results:
                    if not isinstance(channel, dict):
                        raise TypeError(f"채널 데이터 형식 오류: {type(channel)}, 데이터: {channel}")

                    corNo = corNm[cnt // 5] if cnt // 5 < len(corNm) else "None"
                    set_batch_youtube(
                        corNo,
                        channel.get('title', ""),
                        channel.get('video_url', None),
                        channel.get('thumbnail', None),
                        cnt+1
                    )
                    cnt += 1
            else:
                status = "FAIL"

            # 배치 로그 저장
            set_batch_log(BATCH_ID, BATCH_NM, "TU00000001", "getYouTube", now, task_time, status, str(flat_results), random_number)

            # 로그 파일 저장
            log_message = f"[{task_time}] getYouTube 실행 완료 - 상태: {status}, 데이터 개수: {cnt}"
            with open(log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(log_message + "\n")

    except Exception as e:
        error_message = f"[{now}] 유튜브 배치 실행 중 오류 발생: {e}"
        print(error_message)
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(error_message + "\n")

# 배치 실행 함수
def run_youtube_batch_job():
    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(youtube_batch_job())  # 비동기 실행

        set_user_mapp()  # 사용자 이벤트 매핑 정보 등록
    except Exception as e:
        print(f"유튜브 배치 작업 실행 중 오류 발생: {e}")

# 매일 01:00에 실행
#schedule.every().day.at("13:00").do(run_youtube_batch_job)
delayTime = 1
schedule.every(delayTime).minutes.do(run_youtube_batch_job)

print(f"유튜브 배치 작업이 스케줄링되었습니다. (매일 {delayTime} 실행)")

# 무한 루프 실행 (배치 스케줄 유지)
while True:
    schedule.run_pending()
    time.sleep(1)  # 1초마다 체크

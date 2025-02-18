import asyncio
import time
import datetime
import schedule
import os
import json
from main import set_batch_log, set_batch_rst, del_batch_rst, set_user_mapp, set_batch_holiday, set_batch_end_log, app  # Flask 앱을 임포트
from main import test1, test2, test3, test4, test5, test6,test7,test8,test9,test10,test11,test12,test13
from main import card1,card2,card3,card4,card5,card6
from main import bank1,bank2,bank3,bank4,bank5,bank6,bank7,bank8
from main import stock1,stock2,stock3,stock4,stock5,stock6,stock7,stock8
from main import holidayAPI

BATCH_ID = "B000000001"
BATCH_NM = "이벤트 메인 배치"

# 비동기 작업 함수
async def my_batch_job():
    # logs 폴더 경로 설정 (현재 실행 경로의 한 단계 위)
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)  # logs 폴더가 없으면 생성

    # 날짜별로 로그 파일 이름 설정 (현재 날짜 형식: YYYYMMDD)
    today = datetime.datetime.now().strftime("%Y%m%d")
    log_file_path = os.path.join(log_dir, f"batch_log_{today}.txt")
    
    now = datetime.datetime.now()
    print(f"[{now}] 배치 작업 실행 중...")

    # 실행할 작업 정의
    tasks = {

        "api_holiday":holidayAPI(),

        "hana_bank": test1(),
        "abl_life": test2(),
        "kyobo_life": test3(),
        "dongnyang_life": test4(),
        "hanhwa_life": test5(),
        "heungkuk_life": test6(),
        "kdb_life": test7(),
        "samsung_life": test8(),
        "samsung_fire": test9(),
        "heungkuk_fire": test10(),
        "kb_insurance": test11(),
        "miraeasset_life": test12(),
        "nh_insurance": test13(),

        "bc_card":card1(),
        "hana_card":card2(),
        "kb_card":card3(),
        "samsung_card":card4(),
        "shinhan_card":card5(),
        "woori_card":card6(),

        "citi_bank":bank1(),
        "im_bank":bank2(),
        "kb_bank":bank3(),
        "sc_bank":bank4(),
        "shinhan_bank":bank5(),
        "woori_bank":bank6(),
        "ibk_bank":bank7(),
        "kakao_bank":bank8(),

        "dasin_stock":stock1(),
        "kb_stock":stock2(),
        "yuanta_stock":stock3(),
        "samsung_stock":stock4(),
        "hankook_stock":stock5(),
        "kiwoom_stock":stock6(),
        "shinhan_stock":stock7(),
        "hana_stock":stock8(),
    }

    try:
        with app.app_context():
            # 비동기 작업 실행
            task_futures = {name: asyncio.create_task(func) for name, func in tasks.items()}
            responses = await asyncio.gather(*task_futures.values(), return_exceptions=True)
            cnt = 0  # 배치 결과 정상 처리 건수
            
            # 응답 처리 및 로그 기록
            for (task_name, response) in zip(task_futures.keys(), responses):
                task_time = datetime.datetime.now()

                if isinstance(response, Exception):
                    log_message = f"[{task_time}] {task_name} 실행 실패: {response}"
                    # 배치 로그 DB 저장
                    set_batch_log(BATCH_ID , BATCH_NM, '', task_name, now, task_time, "FAIL", str(response))
                else:
                    res = response.get_json()
                    status = "SUCCESS" if res['status_code'] == 200 else "FAIL"
                    log_message = f"[{task_time}] {task_name} 실행 완료 - 상태: {status}, 응답: {res['result']}"
                    
                    if res['status_code'] == 200:
                        if isinstance(res['result'], list) and len(res['result']) > 0:
                            if(task_name == "api_holiday"):
                                for event in res['result']:
                                    set_batch_holiday(
                                        event.get("locdate"),
                                        event.get("isHoliday"),
                                        event.get("dateName")
                                    )
                            else:
                                cnt += 1
                                # 스크레핑 결과 정보 DB 삭제(cnt = 1 일때)
                                del_batch_rst(cnt)

                                # 스크레핑 결과 정보 DB 저장
                                for event in res['result']:
                                    set_batch_rst(
                                        res['bank_cd'],
                                        event.get('title', ""),
                                        "",
                                        event.get('startDt', None) or None,
                                        event.get('endDt', None) or None,
                                        event.get('thumbNail', ""),
                                        event.get('image', ""),
                                        event.get('noti', ""),
                                        event.get('listURL', ""),
                                        event.get('detailURL', "")
                                    )

                        # 배치 로그 DB 저장
                        set_batch_log(BATCH_ID , BATCH_NM, res['fin_id'], task_name, now, task_time, status, res['result'])

                # 로그 파일 저장
                with open(log_file_path, "a", encoding="utf-8") as log_file:
                    log_file.write(log_message + "\n")
            
            # 사용자 , 이벤트 맵핑 정보 등록
            set_user_mapp() 

            # 배치 종료 로그 등록
            e_now = datetime.datetime.now()
            set_batch_end_log(BATCH_ID, now, e_now) 
            
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
schedule.every(5).minutes.do(run_batch_job)

print("배치 작업이 스케줄링되었습니다. (매일 5분마다 실행)")

# 무한 루프 실행 (배치 스케줄 유지)
while True:
    schedule.run_pending()
    time.sleep(1)  # 1초마다 스케줄 체크

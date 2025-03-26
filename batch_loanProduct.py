import asyncio
import time
import datetime
import schedule
import os
import random
from main import set_batch_log, del_loan_product, setLoanFinProd, getCorNo, app
from main import loanProduct1, loanProduct2

BATCH_ID = "B000000006"  # 대출 배치 ID
BATCH_NM = "상품정보(대출) 수집"

# 비동기 작업 함수
async def loan_product_batch_job():
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)  # logs 폴더가 없으면 생성

    today = datetime.datetime.now().strftime("%Y%m%d")
    log_file_path = os.path.join(log_dir, f"loan_product_batch_log_{today}.log")

    now = datetime.datetime.now()
    random_number = random.randint(100000, 999999)
    print(f"[{now}] 상품정보(대출) 배치 작업 실행 중... 함수번호[{random_number}]")

# 실행할 작업 정의
    tasks = {
        "loanProduct1": loanProduct1,
        "loanProduct2": loanProduct2,        
    }
    try:
        with app.app_context():
            # 비동기 작업 실행
            task_futures = {name: asyncio.create_task(func()) for name, func in tasks.items()}
            responses = await asyncio.gather(*task_futures.values(), return_exceptions=True)
            cnt = 0  # 배치 결과 정상 처리 건수

            # 응답 처리 및 로그 기록
            for (task_name, response) in zip(task_futures.keys(), responses):
                task_time = datetime.datetime.now()

                if isinstance(response, Exception):
                    log_message = f"[{task_time}] {task_name} 실행 실패: {response}"
                    # 배치 로그 DB 저장
                    set_batch_log(BATCH_ID , BATCH_NM, '', task_name, now, task_time, "FAIL", str(response), random_number)
                else:
                    res = response.get_json()
                    status = "SUCCESS" if res['status_code'] == 200 else "FAIL"
                    log_message = f"[{task_time}] {task_name} 실행 완료 - 상태: {status}, 응답: {res['result']}"
                    
                    if res['status_code'] == 200:
                        if isinstance(res['result'], list) and len(res['result']) > 0:
                            cnt += 1
                            # 스크레핑 결과 정보 DB 삭제(cnt = 1 일때)
                            del_loan_product(cnt)
                            
                            cor_no_mapping = getCorNo()
                            
                            new_product_list = []

                            for product in res['result']:
                                bank_name = product.get("bank_name")
                                cor_no = cor_no_mapping.get(bank_name, None)  # 매핑된 값이 없으면 None

                                if cor_no is None:
                                    continue 
                                
                                product["cor_no"] = cor_no  
                                new_product_list.append(product)

                            print("대출 상품 데이터 확인용\n" + new_product_list + "\n")

                            setLoanFinProd(new_product_list)

                    # 배치 로그 DB 저장
                    set_batch_log(BATCH_ID , BATCH_NM, res['fin_id'], task_name, now, task_time, status, res['result'], random_number)

                # 로그 파일 저장
                with open(log_file_path, "a", encoding="utf-8") as log_file:
                    log_file.write(log_message + "\n")

    except Exception as e:
        error_message = f"[{now}] 대출 상품 배치 실행 중 오류 발생: {e}"
        print(error_message)
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write("대출 상품 데이터 확인용\n" + new_product_list + "\n")
        with open(log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(error_message + "\n")

# 배치 실행 함수
def run_loan_product_batch_job():
    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(loan_product_batch_job())  # 비동기 실행

        # set_user_mapp()  # 사용자 이벤트 매핑 정보 등록
    except Exception as e:
        print(f"대출 상품정보 배치 작업 실행 중 오류 발생: {e}")

#매일 06:00에 실행
#schedule.every().day.at("06:00").do(run_loan_product_batch_job)
schedule.every(1).minutes.do(run_loan_product_batch_job)

print(f"대출 상품정보 배치 작업이 스케줄링되었습니다. (매일 06:00 실행)")

#무한 루프 실행 (배치 스케줄 유지)
while True:
    schedule.run_pending()
    time.sleep(60)  # 1초마다 체크

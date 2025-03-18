from datetime import datetime
import requests
import pprint

##############################
# 제목 : 실시간 지수 
# 방식 : API
# 수집 경로 : 네이버 증권(상업적 사용 여부 확인 필요)
# 특징 : 국내 / 해외 포맷이 다름 
##############################

async def get_index_list():
    urls = [
        "https://polling.finance.naver.com/api/realtime/domestic/index/KOSPI",      #코스피 
        "https://polling.finance.naver.com/api/realtime/domestic/index/KOSDAQ",     #코스닥
        "https://polling.finance.naver.com/api/realtime/worldstock/index/.IXIC",    #나스닥
        "https://polling.finance.naver.com/api/realtime/worldstock/index/.INX",     #S&P500
        "https://polling.finance.naver.com/api/realtime/worldstock/index/.SSEC",    #상해종합
        "https://polling.finance.naver.com/api/realtime/worldstock/index/.N225"     #니케이 225
    ]
    
    return_li = []

    for url in urls:
        try:
            # 동기적으로 API 요청
            response = requests.get(url)
            target_data = response.json()["datas"][0]
            
            if(url.split("/")[-1].count(".") > 0):
                stock_name = target_data["indexName"]
            else:
                stock_name = target_data["stockName"]

            close_price, compare_price, iso_date = (
                target_data["closePrice"],
                target_data["compareToPreviousClosePrice"],
                target_data["localTradedAt"]
            )

            dt = datetime.fromisoformat(iso_date)
            return_li.append({
                "name": stock_name,
                "price": close_price,
                "rate_upDown": compare_price,
                "standard_date": str(dt.date()),
                "standard_time": str(dt.time())
            })

        except KeyError as e:
            print(f"주요 지수 오류 발생 KeyError: {e}")
        except Exception as e:
            print(f"주요 지수 오류 발생: {e}")

    return return_li




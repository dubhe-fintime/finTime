from datetime import datetime
import requests
import pprint
import yfinance as yf

##############################
# 제목 : 실시간 지수 
# 방식 : API
# 수집 경로 : 야후 
# 특징 : 국내 / 해외 포맷이 다름 
##############################

def get_index_list_Yahoo():
    index_list = [
        ("KOSPI", yf.Ticker("^KS11").history(period="1d")),
        ("KOSDAQ", yf.Ticker("^KQ11").history(period="1d")),
        ("NASDAQ", yf.Ticker("^IXIC").history(period="1d")),
        ("S&P500", yf.Ticker("^GSPC").history(period="1d")),
        ("DOWJONES", yf.Ticker("^DJI").history(period="1d")),
        ("NIKKEI225", yf.Ticker("^N225").history(period="1d")),
        ("SSE", yf.Ticker("000001.SS").history(period="1d")),
        ("HANGSENG", yf.Ticker("^HSI").history(period="1d")),
        ("DAX", yf.Ticker("^GDAXI").history(period="1d")),
        ("FTSE100", yf.Ticker("^FTSE").history(period="1d"))
    ]

    return_li = []
    for name, data in index_list:
        start =  round(data['Open'].tolist()[0],2)
        end =  round(data['Close'].tolist()[0],2)
        up_down  = start - end
        change_rate = (up_down / start * 100) if start != 0 else 0

        return_li.append({
            "name":name,
            "start":start,
            "end":end
        })

    return return_li




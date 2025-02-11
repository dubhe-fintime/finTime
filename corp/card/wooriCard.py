import re
import requests
import ssl
from requests.adapters import HTTPAdapter

##############################
# 제목 : 우리카드
# 금융사코드 : 041
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

##############################
# Service URL = "https://pc.wooricard.com/dcpc/yh1/bnf/bnf02/prgevnt/getPrgEvntList.pwkjson"
# Method = POST
# header에 쿠키 필수!
# body = {
#     "bnf02PrgEvntVo": {
#         "evntCtgrNo": "",
#         "searchKwrd": "",
#         "sortOrd": "orderNew",
#         "pageIndex": "1",
#         "pageSize": "15",
#         "evntItgCfcd": ""
#     }
# }
##############################

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT@SECLEVEL=1")  # 보안 수준 낮춤
        context.check_hostname = False  # SSL 인증서 검증 비활성화
        kwargs["ssl_context"] = context
        super().init_poolmanager(*args, **kwargs)


async def get041Data():
    ######### 기초 설정 Start #############
    # return 값 넣을 리스트
    event_list = []
    # API URL
    url =  "https://pc.wooricard.com/dcpc/yh1/bnf/bnf02/prgevnt/getPrgEvntList.pwkjson"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    # 목록 URL 기본값
    list_domain =  "https://pc.wooricard.com/dcpc/yh1/bnf/bnf02/prgevnt/H1BNF202S00.do"
    ######### 기초 설정 END ##############

    try:

        headers = {
            "Cookie": "JSESSIONID=t6QPpV1W9bQf5FvDL7p3OjvaaLjSNyy0tnsv0QnqDCdWR18EvjseTFgr6bGh6nKJ.amV1c19kb21haW4vd2NwYzEx; TS01d6fea6=01bae404f5e7fb0f8de5c45f60ce75a346c6934a5bb44d05190e4b06f76ab5aff11bc0feea45c91efe283656e9f9969d0f38938a82; _xm_webid_1_=1638786099; TS01bba15d=01bae404f5e7fb0f8de5c45f60ce75a346c6934a5bb44d05190e4b06f76ab5aff11bc0feea45c91efe283656e9f9969d0f38938a82; PCID=12f439a1-af00-60f3-c51b-9823509b4210-1739173354155; lang=ko; bodyYn=Y; _ga=GA1.1.1694652932.1739173355; _gcl_au=1.1.1519562618.1739173355; _ga_LXPH18QLPW=GS1.1.1739173354.1.1.1739173615.60.0.0"
        }

        data = {"bnf02PrgEvntVo":{"evntCtgrNo":"","searchKwrd":"","sortOrd":"orderNew","pageIndex":"1","pageSize":"15","evntItgCfcd":""}}
        # 웹페이지 요청

        session = requests.Session()
        session.mount("https://", TLSAdapter())
        response = session.post(url, headers=headers,json=data,verify=False)
        
        response.raise_for_status()  

        #응답 데이터 가공
        target_data = response.json()["prgEvntList"]
        for element in target_data:

            event_list.append({
                "title": element['cardEvntNm'],
                "startDt": element['evntSdt'].replace('.','-'),
                "endDt": element['evntEdt'].replace('.','-'),
                "thumbNail": domain+element['fileCoursWeb'],
                "listURL": list_domain
            })

            #  확인용
            # print(f"제목 : {element['cardEvntNm']}")
            # print(f"시작 : {element['evntSdt'].replace('.','-')}")
            # print(f"종료 : {element['evntEdt'].replace('.','-')}")    
            # print(f"썸네일URL : {domain+element['fileCoursWeb']}")    
            # print(f"이벤트목록URL : {list_domain}")        

        print(f"우리카드 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list

    except requests.exceptions.RequestException as e:
        print(f"우리카드 요청 오류 발생: {e}")
        return [{"ERROR": str(e)}]
    except Exception as e:
        print(f"우리카드 크롤링 오류 발생: {e}")
        return [{"ERROR": str(e)}]







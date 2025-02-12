import requests
import asyncio
import re
##############################
# 제목 : IM뱅크(대구은행)
# 금융사코드 : 031
# 방식 : API
# 수집 데이터
# 제목 : O | 시작일 : O | 종료일 : O | 썸네일 : O 
# 이미지 : X | 내용 : X | 목록 URL : O | 상세 URL : X
##############################

##############################
# Service URL = "https://www.imbank.co.kr/bbs_ebz_sm_10010_bord_d003.jct"
# Method = POST
##############################
# 목록
    # headers = {
    #     "Content-Type": "application/x-www-form-urlencoded"
    # }

    # data = {
    #     "_JSON_":f"%7B%22EBZ_WEB_WORK_COMM%22%3A%7B%22INQ_SEQ%22%3A%221%22%2C%22INQ_NCSE%22%3A%225%22%2C%22EFN_DTL_CHNL_NO%22%3A%22INS%22%7D%2C%22BBS_ID%22%3A%22EVE003%22%7D"
    #     }

##############################

async def get031Data():

    ######### 기초 설정 Start #############
    event_list = []
    url = "https://www.imbank.co.kr/bbs_ebz_sm_10010_bord_d003.jct"
    # 메인 URL 
    domain = re.match(r"(https?://[^/]+)", url).group(1)
    list_domain = "https://www.imbank.co.kr/bbs_ebz_sm_main.act"
    ######### 기초 설정 END ##############
    try:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
                "_JSON_":f"%7B%22EBZ_WEB_WORK_COMM%22%3A%7B%22INQ_SEQ%22%3A%221%22%2C%22INQ_NCSE%22%3A%225%22%2C%22EFN_DTL_CHNL_NO%22%3A%22INS%22%7D%2C%22BBS_ID%22%3A%22EVE003%22%7D"
                }
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()

        target_data = response.json()["REC1"]
        for element in target_data:
            
            thumbnail = "/".join([
                    domain,
                    str(element['FILE_PATH_NM1']),
            ]) + str(element['IMG_FILE_NM1'])

            event_list.append({
                    "title": element["TIT_NM"],
                    "startDt": element['EVENT_STRT_DTTI'].replace(".","-"),
                    "endDt": element['EVENT_END_DTTI'].replace(".","-"),
                    "thumbNail": thumbnail,
                    "listURL": list_domain
                })
        print(f"IM뱅크 크롤링 완료 | 이벤트 개수 : {len(event_list)}")
        return event_list
    except Exception as e:
        print(f"IM뱅크 오류 발생: {e}")
        return [{"ERROR": str(e)}]
        

import re

## 날짜인지 확인하는 하는 정규식 
def validate_date(date_string):
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return bool(date_pattern.match(date_string))

#####################################
#####################################
##            쿼리 모음             ##
#####################################
#####################################
# 쿼리 모음
def selectQuery(qType, values):
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@S")
    # print("Query Id : "+qType)
    # if len(values) > 0:
    #     print(values)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@E")
    if qType == "Q1": # BACTH LOG 등록
        query = "INSERT INTO BATCH_LOG (BATCH_ID, BATCH_NM, TASK_ID, TASK_NM, ST_DATE, ED_DATE, STATUS, RESULT_DATA) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    elif qType == "Q2": # BACTH 데이터 등록
        query = "INSERT INTO BATCH_RST (COR_NO, EVT_TITLE, EVT_ID, EVT_ST_DATE, EVT_ED_DATE, EVT_THUMBNAIL, EVT_IMG, EVT_NOTI, EVT_LIST_LINK, EVT_DT_LINK) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    elif qType == "Q3": # BACTH 데이터 전체 삭제
        query = "DELETE FROM BATCH_RST"
    elif qType == "Q4": # FILE 업로드 등록
        query = "INSERT INTO FILE_MST (FILE_NM, ORG_FILE_NM, FILE_EXTENSION, FILE_PATH) VALUES (%s, %s, %s, %s)"
    elif qType == "Q5": # FILE 삭제
        query = "DELETE FROM FILE_MST WHERE FILE_NM = %s"
    elif qType == "Q6": # FILE 조회
        query = "SELECT FILE_NM, ORG_FILE_NM, FILE_EXTENSION, FILE_PATH FROM FILE_MST"
    elif qType == "Q7": # 고유 ID 조회
        query = "SELECT SEQUENCE FROM UNIQUE_IDS WHERE LETTER = %s ORDER BY ID DESC LIMIT 1"
    elif qType == "Q8": # 고유 ID 등록
        query = "INSERT INTO UNIQUE_IDS (LETTER, SEQUENCE, IDENTIFIER) VALUES (%s, %s, %s)"
    
    elif qType == "QTEMP": # 임시 배치 테이블 조회
        query = "SELECT * FROM BATCH_RST"

    elif qType == "Q9":  # 금융사 정보 관리 전체 조회
        query = """
            SELECT 
                CM.COR_NO,
                CM.COR_GP,
                COALESCE(CG.GP_NM, '') AS GP_NM,
                COALESCE(CM.COR_NM, '') AS COR_NM,
                COALESCE(CM.COR_NOTI, '') AS COR_NOTI,
                COALESCE(CM.IMG_URL, '') AS IMG_URL,
                COALESCE(CM.THUMBNAIL_URL, '') AS THUMBNAIL_URL,
                COALESCE(CM.USE_YN, '') AS USE_YN,
                COALESCE(DATE_FORMAT(CM.C_DATE, '%Y-%m-%d'), '') AS C_DATE,
                COALESCE(DATE_FORMAT(CM.U_DATE, '%Y-%m-%d'), '') AS U_DATE
            FROM 
                COR_MST AS CM
            JOIN 
                COR_GP AS CG 
            ON 
                CM.COR_GP = CG.GP_NO
        """

    




        

    

        
    # print("###################################")
    # print(query)
    # print("###################################")
    return query

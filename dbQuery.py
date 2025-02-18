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
    #     print(type(values))
    #     print(len(values))
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
        query = "SELECT * FROM EVT_MST"

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
            WHERE 1=1 
        """
        if (len(values) > 0 and values["cor_gp"]):
            query += f"AND CM.COR_GP = '{values['cor_gp']}' "
        if (len(values) > 0 and values["cor_nm"]):
            query += f"AND CM.COR_NM LIKE '%{values['cor_nm']}%' "
        if (len(values) > 0 and values["use_yn"]):
            query += f"AND CM.USE_YN = '{values['use_yn']}' "


    elif qType == "Q10": # 고유 ID 등록
        query = "UPDATE BATCH_RST BR JOIN ( SELECT EM.EVT_ID, EM.COR_NO, EM.EVT_TITLE FROM EVT_MST EM JOIN BATCH_RST BR_SUB ON EM.COR_NO = BR_SUB.COR_NO AND EM.EVT_TITLE = BR_SUB.EVT_TITLE GROUP BY EM.EVT_ID, EM.COR_NO, EM.EVT_TITLE) AS LatestEM ON BR.COR_NO = LatestEM.COR_NO AND BR.EVT_TITLE = LatestEM.EVT_TITLE SET BR.EVT_ID = LatestEM.EVT_ID"
    
    elif qType == "Q11": # 금융사 정보 등록 / 수정
        query = "INSERT INTO COR_MST "
        query += "( COR_NO, COR_NM, COR_GP, COR_NOTI, C_USER, IMG_URL, THUMBNAIL_URL ) "
        query += " VALUES  "
        query += " ( %s, %s, %s, %s, 'ADMIN', %s, %s ) "
        query += " ON DUPLICATE KEY UPDATE "
        query += " COR_NM = %s, COR_GP = %s, COR_NOTI = %s, U_DATE = SYSDATE(), "
        query += " U_USER = 'ADMIN', IMG_URL = %s, THUMBNAIL_URL = %s"

    elif qType == "Q12": # 금융사 사용여부 변경
        query =  "UPDATE COR_MST SET  "
        query += " USE_YN = %s WHERE COR_NO = %s "

    elif qType == "Q13": # 캘린더용 이벤트 조회
        query = """
            SELECT 
                EM.*,
                COALESCE(CM.cor_nm, '미등록기관') AS cor_nm
            FROM EVT_MST EM
            LEFT JOIN COR_MST CM 
                ON EM.COR_NO = CM.COR_NO
                AND CM.USE_YN = 'Y';
        """
    
    elif qType == "Q14": # USER, EVENT 매핑 테이블 등록
        query = "INSERT INTO USER_EVT_MAPP (US_ET_MAPPING_ID, USER_ID , EVT_ID) VALUES (%s, %s, %s)"

    elif qType == "Q15": # USER, EVENT 매핑 대상 조회
        query = """
            SELECT 
                U.USER_ID,
                E.EVT_ID
            FROM (
                SELECT USER_ID FROM CLIENT_USER WHERE USE_YN = 'Y'
            ) AS U
            JOIN EVT_MST AS E
                ON E.USE_YN = 'Y'
            ORDER BY USER_ID , EVT_ID    
            """

    elif qType == "A1": # 배치 데이터 조회
        query  = "SELECT "
        query += "    a.COR_NO cor_no, "
        query += "    COALESCE(c.cor_nm, '미등록기관') cor_nm, "
        query += "    a.EVT_TITLE evt_title, "
        query += "    COALESCE(a.EVT_ID, '') evt_id," #EVT_ID 값과 EVT_MST.USE_YN에 따른 상태 값 설정
        query += "    CASE "
        query += "        WHEN a.EVT_ID IS NULL OR a.EVT_ID = '' THEN 'NONE'"
        query += "        WHEN b.USE_YN = 'Y' THEN 'Y'"
        query += "        WHEN b.USE_YN = 'N' THEN 'N'"
        query += "        ELSE NULL"
        query += "    END AS evt_status, " # 상태 컬럼 추가
        query += "    DATE_FORMAT(a.EVT_ST_DATE, '%Y-%m-%d') evt_st_date, "
        query += "    DATE_FORMAT(a.EVT_ED_DATE, '%Y-%m-%d') evt_ed_date, "
        query += "    a.EVT_THUMBNAIL evt_thumbnail, "
        query += "    a.EVT_IMG evt_img, "
        query += "    a.EVT_NOTI evt_noti,"
        query += "    a.EVT_LIST_LINK evt_list_link, "
        query += "    a.EVT_DT_LINK evt_dt_link, "
        query += "    a.C_DATE c_date"
        query += " FROM BATCH_RST a"
        query += "    LEFT JOIN EVT_MST b ON a.EVT_ID = b.EVT_ID"
        query += "    LEFT JOIN COR_MST c ON a.COR_NO = c.COR_NO"
        query += " WHERE 1=1"
        
        if len(values[0])>0 :
            query += f" AND c.COR_NM LIKE ('{values[0]}')"
        if len(values[1])>0 :
            query += f" AND a.EVT_TITLE LIKE ('{values[1]}')"

        print(query)
    elif qType == "A2": # 배치데이터 이벤트 테이블 적용
        query =  "INSERT INTO EVT_MST "
        query += "	(	 "
        query += "		COR_NO, "
        query += "		EVT_TITLE, "
        query += "		EVT_ID, "
        query += "		EVT_ST_DATE, "
        query += "		EVT_ED_DATE, "
        query += "		EVT_THUMBNAIL, "
        query += "		EVT_IMG, "
        query += "		EVT_NOTI, "
        query += "		EVT_LIST_LINK, "
        query += "		EVT_DT_LINK, "
        query += "		C_DATE "
        query += "	) "
        query += "VALUES "
        query += "	( "
        query += "		%s, "
        query += "		%s, "
        query += "		%s, "
        query += "		%s, "
        query += "		%s, "
        query += "		%s, "
        query += "		%s, "
        query += "		%s, "
        query += "		%s, "
        query += "		%s,  "
        query += "		NOW()  "
        query += "	); "
    
    elif qType == "A3": # 배치데이터 테이블 이벤트 아이디 업데이트
        query =  "UPDATE BATCH_RST SET"
        query += " EVT_ID= %s"
        query += " WHERE COR_NO = %s AND EVT_TITLE = %s"

    elif qType == "A4": # 노출여부 업데이트
        query =  "UPDATE EVT_MST SET"
        query += " USE_YN= %s"
        query += " WHERE EVT_ID= %s"

    elif qType == "A5": # 이벤트 마스터 조회
        query =  "SELECT a.COR_NO cor_no, "
        query += "    COALESCE(b.cor_nm, '미등록기관') cor_nm, "
        query += "	  a.EVT_TITLE evt_title, "
        query += "    a.EVT_ID evt_id, "
        query += "    DATE_FORMAT(a.EVT_ST_DATE, '%Y-%m-%d') evt_st_date, "
        query += "    DATE_FORMAT(a.EVT_ED_DATE, '%Y-%m-%d') evt_ed_date, "
        query += "    a.EVT_THUMBNAIL evt_thumbnail, "
        query += "    a.EVT_IMG evt_img, "
        query += "    a.EVT_NOTI evt_noti, "
        query += "    a.EVT_LIST_LINK evt_list_link, "
        query += "    a.EVT_DT_LINK evt_dt_link, "
        query += "    a.USE_YN use_yn, "
        query += "    a.C_DATE c_date "
        query += "FROM EVT_MST a "
        query += "	LEFT JOIN COR_MST b ON a.COR_NO = b.COR_NO "
        
    # print("###################################")
    # print(query)
    # print("###################################")
    return query

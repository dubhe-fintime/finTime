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
        query = "INSERT INTO BATCH_LOG (BATCH_ID, BATCH_NM, TASK_ID, TASK_NM, ST_DATE, ED_DATE, STATUS, RESULT_DATA, SEQ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
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
                EM.COR_NO,
                COALESCE(CM.COR_NM, '미등록기관') AS COR_NM,
                EM.EVT_TITLE,
                EM.EVT_ST_DATE,
                EM.EVT_ED_DATE,
                EM.EVT_THUMBNAIL,
                EM.EVT_LiST_LINK,
                EM.EVT_DT_LINK,
                CM.PRI_COLOR,
                CASE 
                    WHEN FIND_IN_SET(EM.COR_NO, (
                        SELECT UEO.COR_NO 
                        FROM USER_EVT_OPT UEO 
                        WHERE UEO.USER_ID = '1'
                    )) > 0 THEN 'N'
                    ELSE 'Y'
                END AS GROUP_USE_YN,
                CASE 
                    WHEN FIND_IN_SET(EM.EVT_ID, (
                        SELECT UEO.EVT_ID 
                        FROM USER_EVT_OPT UEO 
                        WHERE UEO.USER_ID = '1'
                    )) > 0 THEN 'N'
                    ELSE 'Y'
                END AS EVT_USE_YN
            FROM EVT_MST EM
            LEFT JOIN COR_MST CM 
                ON EM.COR_NO = CM.COR_NO
                AND CM.USE_YN = 'Y'
                HAVING GROUP_USE_YN = 'Y' AND EVT_USE_YN = 'Y'
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

    elif qType == "Q16": # USER, EVENT 매핑 테이블 등록
        query = "DELETE FROM USER_EVT_MAPP "

    elif qType == "Q17": # 특정 UNIQUE_ID 삭제
        query = "DELETE FROM UNIQUE_IDS WHERE LETTER =%s "    

    elif qType == "Q18": # 배치 공휴일 등록 
        query = """
                INSERT INTO HOI_DAY 
                    ( HOI_DATE, HOI_YN, HOI_NAME ) 
                VALUES 
                    ( %s, %s, %s )
                ON DUPLICATE KEY UPDATE
                    HOI_DATE = %s, 
                    HOI_YN = %s, 
                    HOI_NAME = %s,
                    U_DATE = SYSDATE()
                """
    
    elif qType == "Q19": # 배치 실행 결과 통계 조회
        query = """
                SELECT 
                    BATCH_NM, 
                    TASK_NM, 
                    DATE_FORMAT(ST_DATE, '%Y.%m.%d %H:%i:%s') AS ST_DATE, 
                    DATE_FORMAT(ED_DATE, '%Y.%m.%d %H:%i:%s') AS ED_DATE, 
                    STATUS,
                    (SELECT COUNT(*) FROM BATCH_LOG WHERE SEQ = (
                        SELECT SEQ FROM BATCH_LOG ORDER BY ST_DATE DESC LIMIT 1
                    )) AS TOTAL_COUNT,
                    (SELECT COUNT(*) FROM BATCH_LOG WHERE SEQ = (
                        SELECT SEQ FROM BATCH_LOG ORDER BY ST_DATE DESC LIMIT 1
                    ) AND STATUS = 'SUCCESS') AS SUCCESS_COUNT,
                    (SELECT COUNT(*) FROM BATCH_LOG WHERE SEQ = (
                        SELECT SEQ FROM BATCH_LOG ORDER BY ST_DATE DESC LIMIT 1
                    ) AND STATUS = 'FAIL') AS FAIL_COUNT,
                    RESULT_DATA,
                    ROW_NUMBER() OVER (ORDER BY TASK_ID ASC) AS RN
                FROM BATCH_LOG 
                WHERE SEQ = (
                    SELECT SEQ FROM BATCH_LOG ORDER BY ST_DATE DESC LIMIT 1
                )
                ORDER BY TASK_ID ASC
                LIMIT 1000;

                """

    elif qType == "Q20": # 배치 공휴일 등록 
        query = """
            SELECT 
                HOI_DATE,
                HOI_NAME 
            FROM HOI_DAY
            WHERE HOI_YN = 'Y';
        """

    elif qType == "Q21": # 기관 코드 조회 
        placeholders = ', '.join(['%s'] * len(values))
        query = f"""
            SELECT 
                COR_NO,
                COR_NM,
                COR_GP 
            FROM COR_MST
            WHERE COR_NM IN (  {placeholders} ) 
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
            query += f" AND c.COR_NM LIKE '%{values[0]}%'"
        if len(values[1])>0 :
            query += f" AND a.EVT_TITLE LIKE '%{values[1]}%'"

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

        query += " WHERE 1=1"
        if len(values[0])>0 :
            query += f" AND b.COR_NM LIKE '%{values[0]}%'"
        if len(values[1])>0 :
            query += f" AND a.EVT_TITLE LIKE '%{values[1]}%'"
        if len(values[2])>0 :
            query += f" AND a.USE_YN = '{values[2]}'"


    elif qType == "C1": # 로그인 기능
        query = """
                SELECT  USER_ID,
                    NAME,
                    COALESCE(FIRST_LOGINT,"") 
                    FROM CLIENT_USER WHERE USER_ID = %s AND PASSWORD = %s
                """
    elif qType == "C2":  # 로그인 이력 업데이트
        query = "UPDATE CLIENT_USER SET RECENT_LOGIN = SYSDATE() "
        if len(values) == 2: 
            values.pop()
            query += ", FIRST_LOGINT = SYSDATE() "
        query += " WHERE USER_ID =  %s "

    elif qType == "C3":  # 설정 > 캘린더 설정
        query = """
            SELECT 
            EM.COR_NO,
            COALESCE(CM.cor_nm, '미등록기관') AS cor_nm,
            EM.EVT_TITLE,
            EVT_ID ,
            CM.COR_GP,
            CASE 
                    WHEN FIND_IN_SET(EM.COR_NO, (
                        SELECT UEO.COR_NO 
                        FROM USER_EVT_OPT UEO 
                        WHERE UEO.USER_ID = %s
                    )) > 0 THEN 'N'
                    ELSE 'Y'
                END AS GROUP_USE_YN,
                CASE 
                    WHEN FIND_IN_SET(EM.EVT_ID, (
                        SELECT UEO.EVT_ID 
                        FROM USER_EVT_OPT UEO 
                        WHERE UEO.USER_ID = %s
                    )) > 0 THEN 'N'
                    ELSE 'Y'
                END AS EVT_USE_YN
            FROM EVT_MST EM
            LEFT JOIN COR_MST CM 
                ON EM.COR_NO = CM.COR_NO
                AND CM.USE_YN = 'Y'
                ORDER BY EM.COR_NO ASC
        """

    elif qType == "C4":  # 설정 > 캘린더 설정 > 삭제 
        query = """
            DELETE FROM USER_EVT_OPT
            WHERE USER_ID = %s
        """

    elif qType == "C5":  # 설정 > 캘린더 설정 > 추가 
        query = """
            INSERT INTO USER_EVT_OPT 
                (USER_ID,COR_NO,EVT_ID,C_DATE)
            VALUES
                (%s, %s, %s, SYSDATE())
        """

    elif qType == "COMMON_CD":  # 공통 코드 조회
        query = """
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY CD_ID ASC) AS RN,
                    GP_NM, CD_ID, CD_NM FROM COMMON_CD cc
                JOIN COMMON_GP_CD cgc ON cgc.GP_ID = cc.GP_ID 
                    WHERE cc.GP_ID =%s;
                """
        






    # print("###################################")
    # print(query)
    # print("###################################")
    return query

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
                COALESCE(DATE_FORMAT(CM.U_DATE, '%Y-%m-%d'), '') AS U_DATE,
                COALESCE(CM.PRI_IMG, '') AS PRI_IMG
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
        query += "( COR_NO, COR_NM, COR_GP, COR_NOTI, C_USER, IMG_URL, THUMBNAIL_URL, PRI_IMG ) "
        query += " VALUES  "
        query += " ( %s, %s, %s, %s, 'ADMIN', %s, %s, %s ) "
        query += " ON DUPLICATE KEY UPDATE "
        query += " COR_NM = %s, COR_GP = %s, COR_NOTI = %s, U_DATE = SYSDATE(), "
        query += " U_USER = 'ADMIN', IMG_URL = %s, THUMBNAIL_URL = %s, PRI_IMG = %s"

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
                CM.COR_GP,
                CM.PRI_IMG,
                CASE 
                    WHEN EXISTS (
                        SELECT 1 
                        FROM USER_EVT_OPT UEO 
                        WHERE UEO.USER_ID = %s AND FIND_IN_SET(EM.COR_NO, UEO.COR_NO) > 0
                    ) THEN 'N'
                    ELSE 'Y'
                END AS GROUP_USE_YN,
                CASE 
                    WHEN EXISTS (
                        SELECT 1 
                        FROM USER_EVT_OPT UEO 
                        WHERE UEO.USER_ID = %s AND FIND_IN_SET(EM.EVT_ID, UEO.EVT_ID) > 0
                    ) THEN 'N'
                    ELSE 'Y'
                END AS EVT_USE_YN
            FROM EVT_MST EM
            LEFT JOIN COR_MST CM 
                ON EM.COR_NO = CM.COR_NO
                AND CM.USE_YN = 'Y'
            WHERE EM.USE_YN = 'Y' 
            AND (
                CASE 
                    WHEN EXISTS (
                        SELECT 1 
                        FROM USER_EVT_OPT UEO 
                        WHERE UEO.USER_ID = %s AND FIND_IN_SET(EM.COR_NO, UEO.COR_NO) > 0
                    ) THEN 'N'
                    ELSE 'Y'
                END = 'Y'
            )
            AND (
                CASE 
                    WHEN EXISTS (
                        SELECT 1 
                        FROM USER_EVT_OPT UEO 
                        WHERE UEO.USER_ID = %s AND FIND_IN_SET(EM.EVT_ID, UEO.EVT_ID) > 0
                    ) THEN 'N'
                    ELSE 'Y'
                END = 'Y'
            )
            ORDER BY EM.COR_NO ASC, EM.C_DATE ASC;
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
                WITH LatestSEQ AS (
                    SELECT BATCH_ID, SEQ 
                    FROM (
                        SELECT BATCH_ID, SEQ, ROW_NUMBER() OVER (PARTITION BY BATCH_ID ORDER BY ST_DATE DESC) AS RN
                        FROM BATCH_LOG 
                        WHERE BATCH_ID IN ('B000000002', 'B000000003', 'B000000004', 'B000000005', 'B000000006')
                    ) AS t
                    WHERE RN = 1

                    UNION ALL

                    -- B000000001의 최신 SEQ 찾기
                    SELECT BATCH_ID, SEQ 
                    FROM (
                        SELECT BATCH_ID, SEQ, ROW_NUMBER() OVER (PARTITION BY BATCH_ID ORDER BY ST_DATE DESC) AS RN
                        FROM BATCH_LOG 
                        WHERE BATCH_ID = 'B000000001'
                    ) AS t
                    WHERE RN = 1
                ),

                AggregatedCounts AS (
                    -- SEQ별 TASK_NM 단위로 TOTAL_COUNT, SUCCESS_COUNT, FAIL_COUNT 계산
                    SELECT 
                        SEQ,
                        TASK_NM,  -- TASK_NM 별로 그룹화
                        COUNT(*) AS TOTAL_COUNT,
                        SUM(CASE WHEN STATUS = 'SUCCESS' THEN 1 ELSE 0 END) AS SUCCESS_COUNT,
                        SUM(CASE WHEN STATUS = 'FAIL' THEN 1 ELSE 0 END) AS FAIL_COUNT
                    FROM BATCH_LOG
                    WHERE SEQ IN (SELECT SEQ FROM LatestSEQ)
                    GROUP BY SEQ, TASK_NM  -- TASK_NM 별로 집계
                )

                SELECT 
                    b.BATCH_ID,
                    b.BATCH_NM, 
                    b.TASK_NM,  -- 개별 TASK_NM 출력
                    DATE_FORMAT(b.ST_DATE, '%Y.%m.%d %H:%i:%s') AS ST_DATE, 
                    DATE_FORMAT(b.ED_DATE, '%Y.%m.%d %H:%i:%s') AS ED_DATE, 
                    b.STATUS,
                    a.TOTAL_COUNT,
                    a.SUCCESS_COUNT,
                    a.FAIL_COUNT,
                    b.RESULT_DATA,
                    ROW_NUMBER() OVER () AS RN
                FROM BATCH_LOG b
                JOIN LatestSEQ l ON b.SEQ = l.SEQ
                LEFT JOIN AggregatedCounts a ON b.SEQ = a.SEQ AND b.TASK_NM = a.TASK_NM  -- TASK_NM 기준으로 JOIN
                ORDER BY b.BATCH_ID, b.ED_DATE ASC
                LIMIT 1000

                """

    elif qType == "Q20": # 배치 공휴일 등록 
        query = """
            SELECT 
                HOI_DATE,
                HOI_NAME 
            FROM HOI_DAY
            WHERE HOI_YN = 'Y';
        """

    elif qType == "Q21": # 유튜브 컨텐츠 등록
        query = """
            INSERT INTO YOUTUBE_CONTENTS 
                    ( COR_NO, CONTENT_TITLE, CONTENT_URL, PRIORITY ) 
                VALUES 
                    ( %s, %s, %s, %s )
        """
    elif qType == "Q22": # 기관 코드 조회 
        placeholders = ', '.join(['%s'] * len(values))
        query = f"""
            SELECT 
                COR_NO,
                COR_NM,
                COR_GP 
            FROM COR_MST
            WHERE COR_NM IN (  {placeholders} )  """
        
    elif qType == "Q23": # 네이버 뉴스 배치 추가
        query = """
            REPLACE INTO NEWS_CONTENTS 
                (PRESS_NM, PRESS_IMG, TITLE, CONTENT, LINK, COR_NO, C_DATE) 
            VALUES 
                (%s,%s,%s,%s,%s,%s,SYSDATE());
        """

    elif qType == "Q24": # 유튜브 정보 등록
        query = """
            INSERT INTO YOUTUBE_CONTENTS 
                (COR_NO, CONTENT_TITLE, CONTENT_URL, THUMBNAIL_URL, PRIORITY) 
            VALUES(%s, %s, %s, %s, %s)
            """
    
    elif qType == "Q25": # 유튜브 정보 전체 삭제
        query = "DELETE FROM YOUTUBE_CONTENTS "

    elif qType == "Q26": # 네이버 뉴스 조회
        query = "SELECT TITLE,PRESS_NM,PRESS_IMG,CONTENT,LINK,COR_NO FROM NEWS_CONTENTS "

    elif qType == "Q27": # 네이버 뉴스 삭제
        query = "DELETE FROM NEWS_CONTENTS"

    elif qType == "Q28": # 유튜브 조회
        query = "SELECT COR_NO,CONTENT_TITLE,CONTENT_URL FROM YOUTUBE_CONTENTS "

    elif qType == "Q29": # 공모주 삭제
        query = "DELETE FROM PUBLIC_OFFERING_STOCK "
    
    elif qType == "Q30": # 공모주 정보 등록
        query = """
            INSERT INTO PUBLIC_OFFERING_STOCK 
                (STOCK_NM, SUB_ST_DATE, SUB_ED_DATE, CON_PUB_OFF_PRICE, HOPE_PUB_OFF_PRICE, SUB_COM_RATE, CHIEF_EDITOR) 
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s);
        """
    
    elif qType == "Q31": # 공모주 조회
        query = "SELECT STOCK_NM, SUB_ST_DATE, SUB_ED_DATE, CON_PUB_OFF_PRICE, HOPE_PUB_OFF_PRICE, SUB_COM_RATE, CHIEF_EDITOR, C_DATE FROM PUBLIC_OFFERING_STOCK "

    elif qType == "Q32": # 제주은행API > FILE_MST 테이블 기존것 삭제
        query = " DELETE FROM FILE_MST WHERE ORG_FILE_NM LIKE 'jeju_thumb%' "

    elif qType == "Q33": # 예적금 상품 조회
        query = """
            SELECT 
                FP.COR_NO,
                COALESCE(CM.COR_NM, '미등록기관') AS COR_NM,
                FP.PROD_NM,
                PT_CD.CD_NM AS PROD_TYPE,
                SM_CD.CD_NM AS SAVING_METHOD,
                IC_CD.CD_NM AS INTR_CALC,
                FP.PROD_DETAIL_LINK,
                FP.BASE_INTR,
                FP.MAX_INTR,
                FP.LAST_AVG_INTR,
                FP.C_DATE
            FROM FINANCIAL_PRODUCTS FP
            LEFT JOIN COR_MST CM 
                ON FP.COR_NO = CM.COR_NO
            LEFT JOIN COMMON_CD PT_CD 
                ON FP.PROD_TYPE = PT_CD.CD_ID
            LEFT JOIN COMMON_CD SM_CD 
                ON FP.SAVING_METHOD = SM_CD.CD_ID
            LEFT JOIN COMMON_CD IC_CD 
                ON FP.INTR_CALC = IC_CD.CD_ID;
            """

    elif qType == "Q34": # 예적금 상품 조회
        query = """
           SELECT 
                FLP.COR_NO,
                COALESCE(CM.COR_NM, '미등록기관') AS COR_NM,
                FLP.PROD_NM,
                RT_CD.CD_NM AS RESIDENCE_TYPE,
                IM_CD.CD_NM AS INTR_METHOD,
                RM_CD.CD_NM AS REPAY_METHOD,
                FLP.MIN_INTR,
                FLP.MAX_INTR,
                FLP.C_DATE
            FROM FINANCIAL_LOAN_PRODUCTS FLP
            LEFT JOIN COR_MST CM 
                ON FLP.COR_NO = CM.COR_NO
            LEFT JOIN COMMON_CD RT_CD 
                ON FLP.RESIDENCE_TYPE = RT_CD.CD_ID
            LEFT JOIN COMMON_CD IM_CD 
                ON FLP.INTR_METHOD = IM_CD.CD_ID
            LEFT JOIN COMMON_CD RM_CD 
                ON FLP.REPAY_METHOD = RM_CD.CD_ID;    
            """
        
    elif qType == "Q35": # 예적금 상품 평균 이율 조회
        query = """
            SELECT
                PT_CD.CD_NM AS PROD_TYPE, 
                AVG(FP.BASE_INTR) AS AVG_BASE_INTR, 
                AVG(FP.MAX_INTR) AS AVG_MAX_INTR
            FROM finTime.FINANCIAL_PRODUCTS FP
            LEFT JOIN COMMON_CD PT_CD 
                ON FP.PROD_TYPE = PT_CD.CD_ID
            GROUP BY PROD_TYPE;
            """
        
    elif qType == "Q36": # 대출 상품 평균 이율 조회
        query = """
            SELECT 
                IM_CD.CD_NM AS INTR_METHOD,
                AVG(FLP.MIN_INTR) AS AVG_MIN_INTR, 
                AVG(FLP.MAX_INTR) AS AVG_MAX_INTR
            FROM FINANCIAL_LOAN_PRODUCTS FLP
            LEFT JOIN COMMON_CD IM_CD 
                ON FLP.INTR_METHOD = IM_CD.CD_ID
            GROUP BY INTR_METHOD;
            """

    elif qType == "QA1": # 관리자 로그인 조회
        query = " SELECT USER_ID, USE_YN, NAME FROM ADMIN_USER WHERE USER_ID =%s AND PW =%s  "


    elif qType == "A1": # 배치 데이터 조회
        query  = "SELECT "
        query += "    a.COR_NO cor_no, "
        query += "    COALESCE(c.cor_nm, '미등록기관') cor_nm, "
        query += "    a.EVT_TITLE evt_title, "
        query += "    COALESCE(a.EVT_ID, '') evt_id," #EVT_ID 값과 EVT_MST.USE_YN에 따른 상태 값 설정
        query += "    CASE "
        query += "        WHEN b.USE_YN = 'Y' THEN 'Y'"
        query += "        WHEN b.USE_YN = 'N' THEN 'N'"
        query += "        ELSE 'NONE'"
        query += "    END AS evt_status, " # 상태 컬럼 추가
        query += "    IFNULL(DATE_FORMAT(a.EVT_ST_DATE, '%Y-%m-%d'),'') evt_st_date, "
        query += "    IFNULL(DATE_FORMAT(a.EVT_ED_DATE, '%Y-%m-%d'),'') evt_ed_date, "
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
        if len(values[2])>0 and values[2]=='NONE' :
            query += f" AND a.EVT_ID IS NULL OR a.EVT_ID =''"
        if len(values[2])>0 and values[2]!='NONE' and values[2]!='all' :
            query += f" AND b.USE_YN = '{values[2]}'"

        query += " ORDER BY COR_NM, EVT_ST_DATE DESC"

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
        query += "		SYSDATE()  "
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
        query += "    IFNULL(DATE_FORMAT(a.EVT_ST_DATE, '%Y-%m-%d'),'') evt_st_date, "
        query += "    IFNULL(DATE_FORMAT(a.EVT_ED_DATE, '%Y-%m-%d'),'') evt_ed_date, "
        query += "    a.EVT_THUMBNAIL evt_thumbnail, "
        query += "    a.EVT_IMG evt_img, "
        query += "    a.EVT_NOTI evt_noti, "
        query += "    a.EVT_LIST_LINK evt_list_link, "
        query += "    a.EVT_DT_LINK evt_dt_link, "
        query += "    a.USE_YN use_yn, "
        query += "    a.C_DATE c_date, "
        query += "    a.E_DATE e_date, "
        query += "    CASE  WHEN (a.EVT_ST_DATE IS NULL OR a.EVT_ED_DATE IS NULL OR r.EVT_ID IS NULL)"
        query += "    AND (a.EVT_ED_DATE IS NULL OR a.EVT_ED_DATE >= CURDATE()) "
        query += "    THEN 'CHK'  ELSE ''  END AS CHK_YN, "
        query += "    CASE WHEN a.EVT_ED_DATE < CURDATE() THEN 'END'"
        query += "    ELSE 'ING' END AS ING_YN "
        query += "FROM EVT_MST a "
        query += "	LEFT JOIN COR_MST b ON a.COR_NO = b.COR_NO "
        query += "  LEFT JOIN BATCH_RST r ON a.EVT_ID = r.EVT_ID "

        query += " WHERE 1=1"

        if len(values[0])>0 :
            query += f" AND b.COR_NM LIKE '%{values[0]}%'"
        if len(values[1])>0 :
            query += f" AND a.EVT_TITLE LIKE '%{values[1]}%'"
        if len(values[2])>0 :
            query += f" AND a.USE_YN = '{values[2]}'"
        if len(values[3])>0 :
            if values[3] == 'CHK':
                query += f" AND ( (a.EVT_ST_DATE IS NULL OR a.EVT_ED_DATE IS NULL OR r.EVT_ID IS NULL)"
                query += f" AND (a.EVT_ED_DATE IS NULL OR a.EVT_ED_DATE >= CURDATE()) ) "
            if values[3] == 'END' : 
                query += f" AND a.EVT_ED_DATE < CURDATE()"
            if values[3] == 'ING' : 
                query += f" AND a.EVT_ED_DATE >= CURDATE()"

        query += " GROUP BY a.EVT_ID "
        query += " ORDER BY cor_nm, evt_st_date desc"

    elif qType == "A6": #EVT_MST 컨텐츠 업데이트
        query = """
            UPDATE EVT_MST 
            SET 
                EVT_ST_DATE = %s,
                EVT_ED_DATE = %s,
                EVT_THUMBNAIL = %s,
                EVT_IMG = %s,
                EVT_NOTI = %s,
                EVT_LIST_LINK = %s,
                EVT_DT_LINK = %s,
                E_DATE = SYSDATE()
            WHERE
                EVT_ID = %s
        """
    
    elif qType == "A7" : #EVT_MST 컨텐츠 삭제
        query = """
            DELETE FROM EVT_MST
            WHERE 
                EVT_ID = %s
                """
    
    elif qType == "A8" : #그룹 조회
        query = """
                select GP_NO, GP_NM from COR_GP
                """

    elif qType == "C1": # 로그인 기능
        query = """
                SELECT  USER_ID,
                    NAME,
                    COALESCE(FIRST_LOGIN,"") 
                    FROM CLIENT_USER WHERE USER_ID = %s AND PASSWORD = %s
                """
    elif qType == "C2":  # 로그인 이력 업데이트
        query = "UPDATE CLIENT_USER SET RECENT_LOGIN = SYSDATE() "
        if len(values) == 2: 
            values.pop()
            query += ", FIRST_LOGIN = SYSDATE() "
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
    
    elif qType == "C6" : #SNS간편가입
        query = """
                INSERT INTO CLIENT_USER
                    ( USER_ID, PASSWORD, NAME, COMPANY, PHONE_NO, ADDRESS1, ADDRESS2, USE_YN, 
                    C_DATE, FIRST_LOGIN, RECENT_LOGIN, SNS_ID, SNS_TYPE)
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,SYSDATE(),SYSDATE(),SYSDATE(),%s,%s)
                """   
    elif qType == "C7" : #SNS 가입 확인
        query = """
                SELECT USER_ID, USE_YN FROM CLIENT_USER WHERE SNS_ID = %s  and SNS_TYPE = %s
                """
    elif qType == "C8" : # SNS 로그인 마지막로그인 시간 업데이트
        query = """
                UPDATE CLIENT_USER 
                SET RECENT_LOGIN = SYSDATE()
                WHERE
                SNS_ID = %s AND SNS_TYPE = %s
                """
        
    elif qType == "C9" : # SNS 로그인 연동해제
        query = """
                UPDATE CLIENT_USER 
                SET USE_YN = 'N'
                WHERE
                SNS_ID = %s AND SNS_TYPE = %s
                """

    elif qType == "C10" : # CLIENT_AUTH 최초 INSERT
        query = """
                INSERT INTO CLIENT_AUTH (
                    USER_ID, AUTH_TYPE, IDENTIFIER, ACCESS_TOKEN, ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN, REFRESH_TOKEN_EXPIRE,
                    FIRST_LOGIN, RECENT_LOGIN
                ) VALUES (
                    %s,    %s,    %s,    %s,    %s,    %s,    %s,    NOW(),    NOW()
                )
                """


    elif qType == "C11" : # CLIENT_AUTH 마지막로그인 update
        query = """
                UPDATE CLIENT_AUTH
                SET RECENT_LOGIN = SYSDATE()
                WHERE IDENTIFIER = %s AND AUTH_TYPE = %s
                """
    
    elif qType == "C12" : # SNS 로그인 USEYN 정보 수정
        query = """
                UPDATE CLIENT_AUTH
                SET USE_YN = %s,
                ACCESS_TOKEN = %s,
                ACCESS_TOKEN_EXPIRE = %s,
                REFRESH_TOKEN = %s,
                REFRESH_TOKEN_EXPIRE = %s
                WHERE IDENTIFIER = %s AND AUTH_TYPE = %s
                """
        
    elif qType == "C13" : # USER정보 가져오기
        query = """
                SELECT 
                    A.USER_ID, A.NAME, A.COMPANY, A.PHONE_NO, A.ADDRESS1, A.ADDRESS2, A.SNS_ID, A.SNS_TYPE, A.FIRST_LOGIN, A.RECENT_LOGIN,
                    B.ACCESS_TOKEN, B.ACCESS_TOKEN_EXPIRE, B.REFRESH_TOKEN, B.REFRESH_TOKEN_EXPIRE, B.FIRST_LOGIN SNS_FIRST_LOGIN, B.RECENT_LOGIN SNS_RECENT_LOGIN
                FROM
                    CLIENT_USER A
                        LEFT JOIN
                    CLIENT_AUTH B ON A.USER_ID = B.USER_ID
                    AND A.SNS_TYPE = B.AUTH_TYPE
                    AND A.SNS_ID = B.IDENTIFIER
                WHERE A.USE_YN = 'Y'
                AND A.USER_ID = %s
                """
    elif qType == "C14" : # 회원정보 USEYN 수정
        query = """
                UPDATE CLIENT_USER
                SET USE_YN = %s
                WHERE SNS_ID = %s AND SNS_TYPE = %s
                """ 
    elif qType == "COMMON_CD":  # 공통 코드 조회
        query = """
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY CD_ID ASC) AS RN,
                    GP_NM, CD_ID, CD_NM , EX_FIELD1, EX_FIELD2 FROM COMMON_CD cc
                JOIN COMMON_GP_CD cgc ON cgc.GP_ID = cc.GP_ID 
                    WHERE cc.GP_ID =%s;
                """
        
    elif qType == "F1" : 
        query = """
            INSERT INTO FINANCIAL_PRODUCTS 
                ( COR_NO, PROD_NM, PROD_TYPE, SAVING_METHOD, INTR_CALC, PROD_DETAIL_LINK, BASE_INTR, MAX_INTR, LAST_AVG_INTR, C_DATE )
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, SYSDATE())
            """
    
    elif qType == "F2" : 
        query = """
            DELETE FROM FINANCIAL_PRODUCTS
            """
        
    elif qType == "F3" : 
        query = """
            INSERT INTO FINANCIAL_LOAN_PRODUCTS 
                ( COR_NO, PROD_NM, RESIDENCE_TYPE, INTR_METHOD, REPAY_METHOD, MIN_INTR, MAX_INTR, C_DATE )
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, SYSDATE())
            """
        
    elif qType == "F4" : 
        query = """
            DELETE FROM FINANCIAL_LOAN_PRODUCTS
            """
        

    # print('####################')    
    # print(query)
    # print('####################')    
    return query

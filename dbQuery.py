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
    
    




        

    

        
    # print("###################################")
    # print(query)
    # print("###################################")
    return query

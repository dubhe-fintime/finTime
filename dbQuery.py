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
    if qType == "Q1": # 챗봇 Key mapping data
        query = "SELECT name FROM test_talbe"




        

    

        
    # print("###################################")
    # print(query)
    # print("###################################")
    return query

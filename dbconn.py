#####################################
#####################################
##            DB 연결              ##
#####################################
#####################################

import mysql.connector
import configparser

from dbQuery import selectQuery

import asyncio

import os
# 설정 파일 읽기
config = configparser.ConfigParser()

# DB Connetion 관리
def conn_mysql():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)

    db_host = config['DATABASE']['host']
    db_user = config['DATABASE']['user']
    db_password = config['DATABASE']['password']
    db_database = config['DATABASE']['database']

    cnx = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_database,
        use_pure=True
    )
    return cnx

# Select 쿼리 처리 (DB conn -> Query Search -> result -> DB conn close)
def execute_mysql_query_select(queryId, values):
    cnx = conn_mysql()
    cursor = cnx.cursor()
    try:
        cursor.execute(selectQuery(queryId, values), tuple(values))
        results = cursor.fetchall()
    finally:
        cursor.close()
        cnx.close()
    return results

# Insert 쿼리 처리 (DB conn -> Query Search -> result -> DB conn close)
def execute_mysql_query_insert(queryId, values):
    cnx = conn_mysql()
    cursor = cnx.cursor()
    try:
        query = selectQuery(queryId, values)
        # print(f"Executing query: {query} with values: {values}")
        cursor.execute(query, values)
        cnx.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        if cnx:  # 연결이 열려 있다면 롤백
            cnx.rollback()
        raise
    finally:
        if cursor:  # ✅ 커서가 None이 아닐 경우 닫기
            cursor.close()
        if cnx:  # ✅ 연결이 None이 아닐 경우 닫기
            cnx.close()

# Update 쿼리 처리 (DB conn -> Query Search -> result -> DB conn close)
def execute_mysql_query_update(queryId, values):
    cnx = None
    cursor = None
    try:
        cnx = conn_mysql()  # MySQL 연결을 받아옴
        cursor = cnx.cursor()  # 커서 생성

        # 쿼리 실행 (values를 튜플로 변환하여 전달)
        cursor.execute(selectQuery(queryId, values), tuple(values))
        cnx.commit()  # 커밋

    except Exception as e:
        print(f"Error occurred: {e}")
        if cnx:  # 연결이 열려 있다면 롤백
            cnx.rollback()
        raise
    
    finally:
        if cursor:  # 커서가 열려있다면 닫기
            cursor.close()
        if cnx:  # 연결이 열려있다면 닫기
            cnx.close()


# Delete 쿼리 처리 (DB conn -> Query Search -> result -> DB conn close)
def execute_mysql_query_delete(queryId, values):
    cnx = None
    cursor = None
    try:
        cnx = conn_mysql()  # MySQL 연결을 받아옴
        cursor = cnx.cursor()  # 커서 생성

        # 쿼리 실행 (values를 튜플로 변환하여 전달)
        cursor.execute(selectQuery(queryId, values), tuple(values))
        cnx.commit()  # 커밋

    except Exception as e:
        print(f"Error occurred: {e}")
        if cnx:  # 연결이 열려 있다면 롤백
            cnx.rollback()
        raise
    
    finally:
        if cursor:  # 커서가 열려있다면 닫기
            cursor.close()
        if cnx:  # 연결이 열려있다면 닫기
            cnx.close()


# 단순 쿼리 처리 (DB conn -> Query Search -> result -> DB conn close)
def execute_mysql_query_rest(queryId, values):
    cnx = conn_mysql()
    cursor = cnx.cursor()
    try:
        cursor.execute(selectQuery(queryId, values))
        results = cursor.fetchall()
    finally:
        cursor.close()
        cnx.close()
    return results

# Update 예외 쿼리 처리 (DB conn -> Query Search -> result -> DB conn close)
def execute_mysql_query_update2(queryId, values):
    cnx = conn_mysql()
    cursor = cnx.cursor()
    try:
        cursor.execute(selectQuery(queryId, values))
        cnx.commit()
    finally:
        cursor.close()
        cnx.close()
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
        print(tuple(values))
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
        cnx.rollback()
        raise
    finally:
        cursor.close()
        cnx.close()

# Update 쿼리 처리 (DB conn -> Query Search -> result -> DB conn close)
def execute_mysql_query_update(queryId, values):
    cnx = conn_mysql()
    cursor = cnx.cursor() 
    try:
        cursor.execute(selectQuery(queryId, values), tuple(values))
        cnx.commit()
    finally:
        cursor.close()
        cnx.close()

# Delete 쿼리 처리 (DB conn -> Query Search -> result -> DB conn close)
def execute_mysql_query_delete(queryId, values):
    cnx = conn_mysql()
    cursor = cnx.cursor()
    try:
        cursor.execute(selectQuery(queryId, values), tuple(values))
        cnx.commit()
    finally:
        cursor.close()
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

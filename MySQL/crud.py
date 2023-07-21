import pandas as pd
import mysql.connector as msql
from mysql.connector import Error

def create_table(table_name):
    try:
        conn = msql.connect(host='104.155.141.160', user='root',  
                            password='Qkrrldud2021!')#give ur username, password
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE {table_name}")
            print("Table is created")
    except Error as e:
        print("Error while connecting to MySQL", e)
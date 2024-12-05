# sudo apt upgrade
# sudo apt install -y python3-dev libmariadb3 libmariadb-dev
# pip install --updgrade pip
# pip install mariadb

import mariadb
import sys
import re as regex

import os
import logmodule as logger

connection = None
cursor = None

__logger_name = "DB"

def get_test(value):
    global cursor
    num_id = int(value)
    cursor.execute("select str0, str1 from test where id = ?", (num_id,))

    while True:
        query = cursor.fetchone()

        if query == None:
            break

        print("str0 == %s, str1 == %s" % (query[0], query[1]))

def init():
    global connection
    global cursor
    
    info = {}
    file = None
    
    try:
        path = os.path.abspath("./db_info.txt")
        file = open(path, "r")
        
        for i in range(5):
            line = file.readline()
            line = regex.sub(r"\s+", "", line)
            tokens = line.split(":")
            info[tokens[0]] = tokens[1]
    except Exception as ex:
        logger.print_log(f"DB Setting Error: {ex}", logger_name=__logger_name)
    finally:
        file.close()

    try:
        connection = mariadb.connect(
                user = info["user"],
                password = info["password"],
                host = info["host"],
                port = int(info["port"]),
                database = info["database"])
        cursor = connection.cursor()
    except mariadb.Error as ex:
        logger.print_log(f"Error connecting to MariaDB platform: {ex}", logger_name=__logger_name)
        sys.exit(1)

def update_always():
    pass

def update(value):
    global connection
    global cursor

    if connection == None:
        return

    try:
        get_test(value)
    except mariadb.Error as ex:
        logger.print_log(f"Invalid SQL syntax: {ex}", logger_name=__logger_name)

def final():
    global connection

    if connection == None:
        return
    connection.close()

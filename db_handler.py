# sudo apt upgrade
# sudo apt install -y python3-dev libmariadb3 libmariadb-dev
# pip install --updgrade pip
# pip install mariadb

import mariadb
import sys

connection = None
cursor = None

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

    try:
        connection = mariadb.connect(
                user = "root",
                password = "1234",
                host = "localhost",
                port = 3306,
                database = "test")
        cursor = connection.cursor()
    except mariadb.Error as ex:
        print(f"Error connecting to MariaDB platform: {ex}")
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
        print(f"Invalid SQL syntax: {ex}")

def final():
    global connection

    if connection == None:
        return
    connection.close()

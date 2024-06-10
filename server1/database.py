import mysql.connector

def set_conn():
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="db_onlinebookstore"
    )
    return conn

def inup(query, val):
    conn = set_conn()
    mycursor = conn.cursor()
    mycursor.execute(query, val)
    conn.commit()
    conn.close()

def row_count(query):
    conn = set_conn()
    mycursor = conn.cursor()
    mycursor.execute(query)
    mycursor.fetchall()
    rc = mycursor.rowcount
    conn.close()
    return rc

def get_data(query):
    conn = set_conn()
    mycursor = conn.cursor()
    mycursor.execute(query)
    data = mycursor.fetchall()
    conn.close()
    return data

def insert_data(table, data):
    col = ', '.join(data.keys())
    nval = "%s" + ", %s" * (len(data) - 1)
    query = f"INSERT INTO {table} ({col}) VALUES ({nval})"
    values = list(data.values())
    inup(query, values)

import sqlite3

DATABASE_PATH = 'identifier.sqlite'

def execute_query(query, parameters=None):
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            cursor = connection.cursor()
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            return result
    except Exception as e:
        raise e

def insert_data(table, data):
    query = f"INSERT INTO {table} VALUES ({', '.join(['?' for _ in range(len(data))])})"
    execute_query(query, data)

def update_data(table, set_values, condition):
    set_clause = ', '.join([f"{key} = ?" for key in set_values.keys()])
    query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
    execute_query(query, list(set_values.values()))

def delete_data(table, condition):
    query = f"DELETE FROM {table} WHERE {condition}"
    execute_query(query)

def select_data(table, columns="*", condition=None):
    if condition:
        query = f"SELECT {columns} FROM {table} WHERE {condition}"
    else:
        query = f"SELECT {columns} FROM {table}"
    return execute_query(query)

import psycopg2
from psycopg2 import sql

DATABASE_URL = "postgresql://admin:admin@5000/identifier.sqlite"

def execute_query(query, parameters=None):
    try:
        with psycopg2.connect(DATABASE_URL) as connection:
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
    placeholders = ', '.join(['%s' for _ in range(len(data))])
    query = sql.SQL(f"INSERT INTO {table} VALUES ({placeholders})")
    execute_query(query, data)

def update_data(table, set_values, condition):
    set_clause = sql.SQL(', '.join([sql.Identifier(key).as_sql(cursor=None)[0] + ' = %s' for key in set_values.keys()]))
    query = sql.SQL(f"UPDATE {table} SET {set_clause} WHERE {condition}")
    execute_query(query, list(set_values.values()))

def delete_data(table, condition):
    query = sql.SQL(f"DELETE FROM {table} WHERE {sql.SQL(condition)}")
    execute_query(query)

def select_data(table, columns="*", condition=None):
    if condition:
        query = sql.SQL(f"SELECT {sql.SQL(columns)} FROM {table} WHERE {sql.SQL(condition)}")
    else:
        query = sql.SQL(f"SELECT {sql.SQL(columns)} FROM {table}")
    return execute_query(query)

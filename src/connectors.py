### Import Libraries
import logging
import cx_Oracle
import psycopg2
import mysql.connector
import mariadb
import pyodbc


def get_connection_method( data_source_name:str,
                            hostname: str, 
                            port : int,
                            dbname: str,
                            user: str,
                            password: str):
    ''' Checks and matches the relevant connection and returns the connection function
        :param data_source_name - selected data source for connection 
    '''
    if data_source_name == 'os-postgres' or data_source_name == 'az-postgres':
        return connect_postgres(hostname, 
                                port,
                                dbname,
                                user,
                                password)

    elif data_source_name == 'az-maria' or data_source_name == 'os-maria':
        return connect_mariadb(hostname, 
                                port,
                                dbname,
                                user,
                                password)

    elif data_source_name == 'os-mysql' or  data_source_name == 'az-mysql':
        return connect_mysql(hostname, 
                                port,
                                dbname,
                                user,
                                password)

    elif data_source_name == 'os-oracle':
        return connect_oracle(hostname, 
                                port,
                                dbname,
                                user,
                                password)

    else:
        return connect_null_function(hostname, 
                                        port,
                                        dbname,
                                        user,
                                        password)


def connect_oracle( hostname: str, 
                    port : int,
                    dbname: str,
                    user: str,
                    password: str) -> bool:
    ''' Checks and tests the Oracle connection and returns the status of the connection
        :param hostname - hostname of thesystem
        :param port - port number of the system
        :param dbname - Database name of the system
        :param user - username of the system
        :param password - password for the DB
    '''
    conn = None
    try:
        dsn_tns = cx_Oracle.makedsn(hostname,
                            port,
                            service_name=dbname)
        conn = cx_Oracle.connect(user=user,
                         password=password,
                         dsn=dsn_tns)
        return conn 
    except (Exception, cx_Oracle.Error) as error:
        print(f"Error connecting to Oracle Platform: {error}")
    return False


def connect_postgres(hostname: str, 
                     port : int,
                     dbname: str,
                     user: str,
                     password: str) -> bool:
    ''' Checks and tests the postgres connection and returns the status of the connection
        :param hostname - hostname of thesystem
        :param port - port number of the system
        :param dbname - Database name of the system
        :param user - username of the system
        :param password - password for the DB
    '''
    conn = None
    try:
        conn = psycopg2.connect(host=hostname,
                                port = port,
                                database=dbname,
                                user=user,
                                password=password)
        return True 
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error connecting to Postgres Platform: {error}")
    return False


def connect_mariadb(hostname: str, 
                     port : int,
                     dbname: str,
                     user: str,
                     password: str) -> bool:
    ''' Checks and tests the mariadb connection and returns the status of the connection
        :param hostname - hostname of the system
        :param port - port number of the system
        :param dbname - Database name of the system
        :param user - username of the system
        :param password - password for the DB
    '''
    conn = None
    try:
        conn = mariadb.connect(host=hostname,
                                port=port,
                                user=user,
                                password=password)
        return True 
    except  mariadb.Error as error:
        print(f"Error connecting to MariaDB Platform: {error}")   
    return False
    

def connect_mysql(hostname: str, 
                     port : int,
                     dbname: str,
                     user: str,
                     password: str) -> bool:
    ''' Checks and tests the MySQL connection and returns the status of the connection
        :param hostname - hostname of the system
        :param port - port number of the system
        :param dbname - Database name of the system
        :param user - username of the system
        :param password - password for the DB
    '''
    conn = None
    try:
        conn = mysql.connector.connect(host=hostname,
                                        port=port,
                                        database=dbname,
                                        user=user,
                                        password=password)
        return True 
    except  mysql.connector.Error as error:
        print(f"Error connecting to MySQL Platform: {error}")   
    return False


def connect_sqlserver(hostname: str, 
                     port : int,
                     dbname: str,
                     user: str,
                     password: str) -> bool:
    ''' Checks and tests the MySQL connection and returns the status of the connection
        :param hostname - hostname of the system
        :param port - port number of the system
        :param dbname - Database name of the system
        :param user - username of the system
        :param password - password for the DB
    '''
    conn = None
    driver= '{ODBC Driver 17 for SQL Server}'
    try:
        conn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+hostname+';PORT=1433;DATABASE='+dbname+';UID='+user+';PWD='+ password)
        return True 
    except  pyodbc.Error as error:
        print(f"Error connecting to SQLServer Platform: {error}")   
    return False

def connect_null_function(hostname: str, 
                     port : int,
                     dbname: str,
                     user: str,
                     password: str)-> bool:
    print(f"The selected source is not configured")   
    return False

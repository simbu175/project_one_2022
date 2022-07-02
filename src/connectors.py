### Import Libraries
from urllib.parse import quote_plus

import cx_Oracle
import mariadb
import mysql.connector
import psycopg2
import pyodbc
import redshift_connector
from sqlalchemy import exc
from sqlalchemy.engine import create_engine


def get_connection_method(data_source_name: str,
                          hostname: str,
                          port: int,
                          dbname: str,
                          user: str,
                          password: str,
                          aws_access_key: str,
                          aws_secret_key: str,
                          s3_path: str,
                          aws_region: str):
    """ Checks and matches the relevant connection and returns the connection function
        :param hostname - Hostname of the system
        :param port - Db server Port
        :param dbname - Name of the database
        :param user - Userid of the database
        :param password - Password of the corresponding database
        :param aws_access_key - AWS access key from IAM
        :param aws_secret_key - AWS secret access key from IAM
        :param s3_path - Athena query results location
        :param aws_region - AWS region
        :param data_source_name - selected data source for connection
    """
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

    elif data_source_name == 'os-mysql' or data_source_name == 'az-mysql':
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

    elif data_source_name == 'aws-redshift':
        return connect_redshift(hostname,
                                dbname,
                                user,
                                password)

    elif data_source_name == 'aws-athena':
        return connect_athena(aws_access_key,
                              aws_secret_key,
                              dbname,
                              aws_region,
                              s3_path)

    else:
        return connect_null_function(hostname,
                                     port,
                                     dbname,
                                     user,
                                     password)


def connect_oracle(hostname: str,
                   port: int,
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
                     port: int,
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
                                port=port,
                                database=dbname,
                                user=user,
                                password=password)
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error connecting to Postgres Platform: {error}")
    return False


def connect_mariadb(hostname: str,
                    port: int,
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
                  port: int,
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
                      port: int,
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
    driver = '{ODBC Driver 17 for SQL Server}'
    try:
        conn = pyodbc.connect(
            'DRIVER=' + driver + ';SERVER=tcp:' + hostname + ';PORT=1433;DATABASE=' + dbname + ';UID=' + user + ';PWD=' + password)
        return True
    except  pyodbc.Error as error:
        print(f"Error connecting to SQLServer Platform: {error}")
    return False


def connect_redshift(hostname: str,
                     dbname: str,
                     user: str,
                     password: str) -> bool:
    """ Checks and tests the MySQL connection and returns the status of the connection
        :param hostname - hostname of the system
        :param dbname - Database name of the system
        :param user - username of the system
        :param password - password for the DB
    """
    conn = None
    try:
        conn = redshift_connector.connect(host=hostname,
                                          database=dbname,
                                          user=user,
                                          password=password)
        return True
    except redshift_connector.Error as error:
        print(f"Error connecting to RedShift cluster : {error}")
        return False


def connect_athena(access_key: str,
                   secret_key: str,
                   region: str,
                   path: str,
                   dbname: str) -> bool:
    """ Checks and tests the MySQL connection and returns the status of the connection
        :param access_key - Access key from IAM
        :param secret_key - Secret access key from IAM
        :param dbname - Database name of the system
        :param path - Athena query results bucket
        :param region - AWS region under consideration
    """
    conn = None
    try:
        connection_string = (
            f"awsathena+rest://{access_key}:{secret_key}@"
            f"athena.{region}.amazonaws.com:443/"
            f"{dbname}?s3_staging_dir={path}&work_group=primary"
        )
        # Create the SQLAlchemy connection
        engine = create_engine(
            connection_string.format(
                aws_access_key_id=quote_plus(access_key),
                aws_secret_access_key=quote_plus(secret_key),
                region_name=region,
                schema_name=dbname,
                s3_staging_dir=quote_plus(path),
            )
        )
        athena_connection = engine.connect()
        return True

    except exc.SQLAlchemyError as error:
        print(f"Error connecting to Amazon Athena : {error}")
        return False


def connect_null_function(hostname: str,
                          port: int,
                          dbname: str,
                          user: str,
                          password: str) -> bool:
    print(f"The selected source is not configured")
    return False

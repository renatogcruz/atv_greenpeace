from sqlalchemy import create_engine
import pymysql

from os import environ
from dotenv import load_dotenv

load_dotenv()


def conn():
    '''connecting to PRODUCTION database'''

    dbuser = environ['DBUSER']
    dbpass = environ['DBPASS']
    dbhost = environ['DBHOST']
    dbport = environ['DBPORT']
    dbname = environ['DBNAME']

    conn = create_engine('mysql+pymysql://' + dbuser + ':' + dbpass +
                         '@' + dbhost + ':' + str(dbport) + '/' + dbname, echo=False)

    return conn


def update_product(execution_data, execution_id, table_name):

    engine = conn()
    connection = engine.raw_connection()
    cursor = connection.cursor()

    values = []
    for key in execution_data.keys():
        values.append(f"{key} = '{execution_data[key]}'")

    values_statement = ', '.join(values)
    # print(values_statement)

    try:
        statement = f"UPDATE {table_name} SET {values_statement} WHERE id={int(execution_id)}".replace(
            "'None'", 'NULL')

        # print(statement)
        cursor.execute(statement)

        connection.commit()
        cursor.close()

        return dict(status='success', message=statement)
    except Exception as e:

        error = str(e).replace("'", "")
        print('--- Error update execution')
        print(error)
        print(statement)

        return dict(status='error', error=error)

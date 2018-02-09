import os
import sys


def main():
    import argparse

    parser = argparse.ArgumentParser(description='This tool loads a CSV file to any pgSQL DBMS table.')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--csv', type=str, help='The input CSV file to be loaded on DB.', required=True)
    requiredNamed.add_argument('--hst', type=str, help='The hostname for the pgSQL DBMS.', required=True)
    requiredNamed.add_argument('--dbn', type=str, help='The database name for which the data ingestion is desired.',
                               required=True)
    requiredNamed.add_argument('--uid', type=str, help='The username of the user peforming the ingestion.',
                               required=True)
    requiredNamed.add_argument('--pwd', type=str, help='The password of the user performing the ingestion.',
                               required=True)
    requiredNamed.add_argument('--tbl', type=str, help='The destination table name.', required=True)
    parser.add_argument('--sep', type=str, help='The CSV field separator. Semicolon by default.', default=';')
    args = parser.parse_args()

    csvfile = os.path.expanduser(args.csv)
    host = args.hst
    dbname = args.dbn
    uid = args.uid
    pwd = args.pwd
    dsn = "host = '{}' dbname = '{}' user = '{}' password = '{}'".format(host, dbname, uid, pwd)
    tbl = args.tbl
    separator = args.sep

    conn = connectDb(dsn)

    # Apro file CSV
    f = open(csvfile, 'r')

    if not existsTable(conn, tbl):  # La tabella non esiste, la devo creare prima
        createTable(f, conn, tbl)

    print("Tabella creata, ora inizio ingestion.")
    # Posso continuare con ingestion nella tabella appena creata
    f.seek(0)
    #loadCSV(conn, f, tbl, separator)
    print("ingestion completata")
    conn.close()
    f.close()


def existsTable(conn, tbl):
    cur = conn.cursor()
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (tbl,))
    return cur.fetchone()[0]


def readCSV(f):
    import csv

    reader = csv.reader(f, delimiter=';')

    longest, headers, type_list = [], [], []
    minlen = 10

    for row in reader:
        if len(headers) == 0:
            headers = row
            for _ in row:
                # Setting the min field length
                longest.append(minlen)
                type_list.append('')
        else:
            # After headers, I iterate on columns
            for i in range(len(row)):
                # NA is the csv null value
                if type_list[i] == 'varchar' or row[i] == 'NA':
                    pass
                else:
                    type_list[i] = dataType(row[i], type_list[i])
                if len(row[i]) > longest[i]:
                    longest[i] = len(row[i])

    return longest, headers, type_list


def dataType(val, current_type):
    import ast
    try:
        # Evaluates numbers to an appropriate type, and strings an error
        t = ast.literal_eval(val)
    except ValueError:
        return 'varchar'
    except SyntaxError:
        return 'varchar'
    if type(t) in [int, float]:
        if type(t) is float and current_type not in ['varchar']:
            return 'float'
        if (type(t) in [int]) and current_type not in ['float', 'varchar']:
            # Use smallest possible int type
            if (-32768 < t < 32767) and current_type not in ['integer', 'bigint']:
                return 'smallint'
            elif (-2147483648 < t < 2147483647) and current_type not in ['bigint']:
                return 'integer'
            else:
                return 'bigint'
    else:
        return 'varchar'


def createTable(file, conn, tbl):
    statement = 'create table ' + tbl + ' ('

    longest, headers, type_list = readCSV(file)

    for i in range(len(headers)):
        if type_list[i] == 'varchar':
            statement = (statement + '\n{} varchar({}),').format(headers[i].lower(), str(longest[i]))
        else:
            statement = (statement + '\n' + '{} {}' + ',').format(headers[i].lower(), type_list[i])

    statement = statement[:-1] + ');'

    if conn is None:
        sys.exit(1)

    cur = conn.cursor()

    cur.execute(statement)
    conn.commit()
    cur.close()


def connectDb(dsn):
    import psycopg2
    try:
        conn = psycopg2.connect(dsn)
    except:
        print("Connection failed.")
        return None

    return conn


def loadCSV(conn, file_object, table_name, separator):
    sql = """
        COPY %s FROM STDIN WITH CSV HEADER
        DELIMITER AS '""" + separator + """'
        """

    cursor = conn.cursor()
    cursor.copy_expert(sql=sql % table_name, file=file_object)
    conn.commit()
    cursor.close()


if __name__ == '__main__':
    main()

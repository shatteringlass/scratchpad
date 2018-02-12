def main():
    import argparse
    import os

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--cutoff', type=str, help='')

    parser.add_argument('--cleanup', metavar='ext', type=str, nargs='*', help='', default='')
    parser.add_argument('--sep', type=str, help='The CSV field separator. Semicolon by default.', default=';')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--wdir', type=str, help='Working directory path (used for downloads and conversions).',
                               required=True)
    requiredNamed.add_argument('--hst', type=str, help='The hostname for the pgSQL DBMS.', required=True)
    requiredNamed.add_argument('--dbn', type=str, help='The database name for which the data ingestion is desired.',
                               required=True)
    requiredNamed.add_argument('--uid', type=str, help='The username of the user peforming the ingestion.',
                               required=True)
    requiredNamed.add_argument('--pwd', type=str, help='The password of the user performing the ingestion.',
                               required=True)

    args = parser.parse_args()

    wdir = os.path.expanduser(args.wdir + '/')
    path = os.path.dirname(os.path.realpath(__file__))
    cutoff = args.cutoff
    hst = args.hst
    dbn = args.dbn
    uid = args.uid
    pwd = args.pwd
    sep = args.sep

    print("Fetching the available file list...")
    n = list(map(lambda x: x.strftime("%Y%m%d"), download_files(cutoff, wdir)))
    print("List fetched. Now going to download the most recent files...")

    for file in os.listdir(wdir):
        dlt = isDLT(file)
        ful = isFUL(file)
        first_dlt = dlt and first_dlt != dlt
        if file.endswith('.zip') and (dlt or ful):
            print(r"--> Unzipping and flattening file {}...".format(str(file)))
            unzip_files(file, os.path.dirname(file))

            no_ext = file[:-3]
            xml = "{}{}".format(no_ext, 'xml')
            xsl = path + '/FUL.xsl' if ful else path + '/DLT.xsl'
            csv = "{}{}".format(no_ext, 'csv')

            to_csv(xml, xsl, csv)

    m_ful = wdir + r'/merge_FULINS_' + n[0] + '.csv'
    m_dlt = wdir + r'/merge_DLTINS_' + n[1] + '.csv'

    print("Merging available FULINS files.")
    merge_mult_csv(wdir + r'/FULINS*.csv', m_ful)
    print("Merging available DLTINS files.")
    merge_mult_csv(wdir + r'/DLTINS*.csv', m_dlt)

    print("Ingesting FULINS data into pgSQL table.")
    ingest_db(hst, dbn, 'fulins', uid, pwd, m_ful, sep, True)
    print("Ingesting DLTINS data into pgSQL table.")
    ingest_db(hst, dbn, 'dltins', uid, pwd, m_dlt, sep, True)

    print("File ingested.")

    # insertHashes(hst, dbn, 'fulins', uid, pwd, m_ful)
    # insertHashes(hst, dbn, 'dltins', uid, pwd, m_ful)

    # Se l'utente lo ha richiesto, procedo a eliminare gli artefatti scaricati
    if len(args.cleanup) > 0:
        print("Now removing leftover files.")
        cleanup(wdir, args.cleanup)


def download_files(cutoff, dest_path):
    import firds2dl as f

    # Bypass the last run date if another ISO8601 timestamp is provided as argument
    if cutoff is not None:
        from datetime import datetime
        last_run = datetime.strptime(cutoff, f.ISOfmt)
    else:
        fname = 'lastrun'
        last_run = f.readDate(fname)  # Lancia errore se non esiste questo file

    list = f.getList(last_run, 0, 500)
    return f.downloadLinks(list, dest_path)


def merge_mult_csv(path, out):
    import shutil
    import glob
    allFiles = glob.glob(path)
    with open(out, 'wb') as outfile:
        for i, fname in enumerate(allFiles):
            with open(fname, 'rb') as infile:
                if i != 0:
                    infile.readline()  # Throw away header on all but first file
                # Block copy rest of file from input to output without parsing
                shutil.copyfileobj(infile, outfile)


def unzip_files(zip_path, dest_path):
    import zipfile
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(dest_path)


def to_csv(xml, xsl, csv):
    import xml2csv as x
    x.transform(xml, xsl, csv)


def ingest_db(host, dbname, tbl, uid, pwd, csvfile, separator, trunc):
    import csv2pg as c
    dsn = "host = '{}' dbname = '{}' user = '{}' password = '{}'".format(host, dbname, uid, pwd)

    conn = c.connectDb(dsn)
    f = open(csvfile, 'r')

    if not c.existsTable(conn, tbl):
        h = c.readCSV(f)
        c.createTable(*h, conn, tbl)

    print("Tabella creata, ora inizio ingestion.")
    f.seek(0)
    c.loadCSV(conn, f, tbl, separator, trunc)
    print("Ingestion completata.")

    conn.close()
    f.close()


def cleanup(dir, ext):
    import os
    # Remove files with specified extension
    for file in os.listdir(dir):
        for x in ext:
            if file.endswith('.' + str(x)):
                os.remove(file)


def isFUL(file):
    return string_contains(file, c='FULINS')


def isDLT(file):
    return string_contains(file, c='DLTINS')


def string_contains(s, c):
    return c in s


if __name__ == '__main__':
    main()

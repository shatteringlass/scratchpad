import argparse
import json
import os
import requests
import sys
from datetime import datetime

ISOfmt = "%Y-%m-%dT%H:%M:%SZ"


def main():
    parser = argparse.ArgumentParser(
        description='This tool queries ESMA FIRDS system to obtain available financial instrument data. If no argument is provided, the tool downloads to the current working directory any file made available on the platform no earlier than the last run date (provided that a lastrun file containing such timestamp is present alongside this tool).')
    parser.add_argument('--cutoff', type=str,
                        help='Earliest data publication date to be searched, in ISO8601 format and Zulu time - i.e. YYYY-MM-DDTHH:MM:SSZ')
    parser.add_argument('--dest', type=str, default='./', help='Destination folder for downloaded data.')
    args = parser.parse_args()

    # Bypass the last run date if another ISO8601 timestamp is provided as argument
    if args.cutoff is not None:
        lastRun = datetime.strptime(args.cutoff, ISOfmt)
    else:
        fname = 'lastrun'
        lastRun = readDate(fname)

    list = getList(lastRun, 0, 500)
    downloadLinks(list, args.dest)


def readDate(fname):
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            line = f.read()
            assert (len(line) > 0)
            return datetime.strptime(line, ISOfmt)
            f.close()
    else:
        print("No file to read last run date from. Please retry and specify a last run date in ISO 8601 format.")
        sys.exit(1)


def writeDate(fname):
    if os.path.isfile(fname):
        with open(fname, 'r+') as f:
            f.seek(0)
            f.write(endDate)
            f.truncate()
            f.close()
    else:
        print("No such file.")
        sys.exit(1)


def getList(lastRun, startRow, maxRows):
    endpoint = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/"
    nowISO = datetime.utcnow().replace(microsecond=0)
    endDate = nowISO.strftime(ISOfmt)

    startDate = lastRun.strftime(ISOfmt)
    query = "select?q=*&fq=publication_date:%5B{}+TO+{}%5D&wt=json&indent=true&start={}&rows={}".format(startDate,
                                                                                                        endDate,
                                                                                                        startRow,
                                                                                                        maxRows)

    destPage = endpoint + query
    response = json.loads(requests.get(destPage).content)
    response = response['response']

    leftRows = response['numFound'] - maxRows

    if leftRows <= 0:
        return response['docs']
    else:
        print("Pagination needed.")
        return response['docs'].update(getList(lastRun, maxRows + 1, leftRows))

def get_newest(list):
    return max([datetime.strptime(x['publication_date'], ISOfmt) for x in list])


def downloadLinks(list, destPath):
    FUL = [x for x in list if x['file_type'] == 'FULINS']

    if len(FUL) <= 0:
        print("No items found.")
        sys.exit(1)

    newestFUL = get_newest(FUL)
    FUL_OPT = [x for x in FUL if hasOptions(x) and datetime.strptime(x['publication_date'], ISOfmt) == newestFUL]
    FUL_FUT = [x for x in FUL if hasFutures(x) and datetime.strptime(x['publication_date'], ISOfmt) == newestFUL]
    FUL_FWD = [x for x in FUL if hasForwards(x) and datetime.strptime(x['publication_date'], ISOfmt) == newestFUL]
    FUL_SWP = [x for x in FUL if hasForwards(x) and datetime.strptime(x['publication_date'], ISOfmt) == newestFUL]

    DLT = [x for x in list if x['file_type'] == 'DLTINS' and isNewerThan(x, newestFUL)]
    newestDLT = get_newest(DLT)

    ls = [FUL_OPT, FUL_FUT, FUL_FWD, FUL_SWP, DLT]

    for list in ls:
        for file in list:
            link = file['download_link']
            downloadZip(link, destPath + getFilename(link))

    return newestFUL, newestDLT


def hasOptions(r):
    return r['file_name'].find("_O_") != -1


def hasSwaps(r):
    return r['file_name'].find("_S_") != -1


def hasFutures(r):
    return r['file_name'].find("_F_") != -1


def hasForwards(r):
    return r['file_name'].find("_J_") != -1


def isNewerThan(r, dt):
    return datetime.strptime(r['publication_date'], ISOfmt) > dt


def getFilename(link):
    return link[link.rfind("/") + 1:]


def downloadZip(link, dest):
    response = requests.get(link, stream=True)
    # Throw an error for bad status codes
    response.raise_for_status()

    # Write chunks to file
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)


if __name__ == '__main__':
    main()

import requests
from bs4 import BeautifulSoup
from xlrd import open_workbook
from pprint import pprint
from datetime import datetime
import os

def convert_date(l):
    print(l)
    t = datetime.strptime(l, '%b. %d, %Y').strftime('%Y-%m-%d')
    return t


def get_10k_report(link, ticker, comp_num):
    d = {
        'ticker_symbol': ticker,
        'index_key': comp_num
    }
    r = requests.get(link)
    fname = '{0}_10k.xls'.format(ticker)
    open(fname, 'wb').write(r.content)


    wb = open_workbook(fname)
    sheet = wb.sheets()[0]

    col_index = {}
    values = {
        'ticker_symbol': ticker,
        'index_key': comp_num
    }
    for row in range(sheet.nrows):
        label = sheet.cell(row, 0).value
        for col in range(sheet.ncols):
            if col > 0:
                cell = sheet.cell(row, col).value
                if cell:
                    if str(cell).strip().replace(" ","") != '':
                        values[label] = cell
                        if col > 1:
                            col_index[label] = col

    d = values

    if 'Entity Common Stock, Shares Outstanding' in col_index:
        d['shares_outstanding'] = {
            'date': convert_date(sheet.cell(1, col_index['Entity Common Stock, Shares Outstanding']).value),
            'value': d['Entity Common Stock, Shares Outstanding']
        }

    if 'Entity Public Float' in col_index:
        d['public_float'] = {
            'date': convert_date(sheet.cell(1, col_index['Entity Public Float']).value),
            'value': d['Entity Public Float']
        }

    d['doc_end_date'] = convert_date(sheet.cell(1, 1).value)

    # os.remove(fname)


    return d


def get_edgar_data(ticker):
    count = 0
    is_10k = None
    excel_link = None
    while not is_10k:
        u = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={0}&type=&dateb=&owner=include&start={1}&count=100'.format(ticker, str(count))
        print(u)
        r = requests.get(u)
        soup = BeautifulSoup(str(r.text))
        rows = soup.find_all('tr')
        comp_num = None
        for ro in rows:
            if not is_10k:
                td = ro.find_all('td')
                for d in td:
                    if str(d.text).strip() == '10-K':
                        is_10k = True

                if is_10k:
                    links = ro.find_all('a', {"id": "interactiveDataBtn"})
                    if len(links) > 0:
                        href = links[0]['href']
                        comp_num = href.split("&cik=")[1].split("&accession_number")[0]
                        access_number = str(href.split("&accession_number=")[1].split("&")[0]).replace("-","")
                        excel_link = 'https://www.sec.gov/Archives/edgar/data/{0}/{1}/Financial_Report.xlsx'.format(comp_num, access_number)

        count += 100


    if excel_link:
        print(excel_link)
        data = get_10k_report(excel_link, ticker, comp_num)
        return data

    else:
        return None
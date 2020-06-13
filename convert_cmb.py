import eml_parser
import io
import sys
import os
from common import *
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from beancount.core import data
from beancount.core.data import Amount, Balance, Decimal, Posting, Transaction
from beancount.parser import printer
from datetime import date
import dateparser


def get_currency(currency):
    trade_area_list = {
        'CN': 'CNY',
        'US': 'USD',
        'JP': 'JPY',
        'HK': 'HKD'
    }
    if currency == '':
        return 'CNY'
    if currency not in trade_area_list:
        print('Unknown trade area: ' + currency +
                ', please append it to ' + __file__)
        return currency
    return trade_area_list[currency]

def get_date(start_date, detail_date):
    month = detail_date[0:2]
    day = detail_date[2:4]
    ret = date(start_date.year, int(month), int(day))
    if month == '01' and ret < start_date:
        ret = ret.replace(ret.year + 1)
    return ret

def parse_cmb(filename):
    account = "Liabilities:CreditCard:CMB"
    transactions = []
    with open(filename, "rb") as f:
        file_bytes = f.read()
        parsed_eml = eml_parser.eml_parser.decode_email_b(file_bytes, include_raw_body=True)
        #  print(parsed_eml)
        content = parsed_eml["body"][0]["content"]
        soup = BeautifulSoup(content, "html.parser")
        print(soup)
        # balance according to bill amount
        date_range = soup.select("#fixBand38 div font")[0].text.strip()
        transaction_date = dateparser.parse(
            date_range.split('-')[1].split('(')[0])
        transaction_date = date(transaction_date.year,
                                transaction_date.month, transaction_date.day)
        start_date = dateparser.parse(date_range.split('-')[0])
        start_date = date(start_date.year,
                          start_date.month,
                          start_date.day)
        balance = '-' + \
            soup.select('#fixBand40 div font')[0].text.replace(
                '￥', '').replace(',', '').strip()

        entry = Balance(
            account=account,
            amount=Amount(Decimal(balance), 'CNY'),
            meta={},
            tolerance='',
            diff_amount=Amount(Decimal('0'), 'CNY'),
            date=transaction_date
        )
        transactions.append(entry)

        #  bands = soup.select('#fixBand29 #loopBand2>table>tbody>tr')
        bands = soup.select("#fixBand29 #loopBand2>table>tr")
        for band in bands:
            tds = band.select('td #fixBand15 table table td')
            if len(tds) == 0:
                continue
            trade_date = tds[1].text.strip()
            if trade_date == '':
                trade_date = tds[2].text.strip()
            time = get_date(start_date, trade_date)
            full_descriptions = tds[3].text.strip().split('-')
            payee = full_descriptions[0]
            description = '-'.join(full_descriptions[1:])
            trade_currency = get_currency(tds[6].text.strip())
            trade_price = tds[7].text.replace('\xa0', '').strip()
            real_currency = 'CNY'
            real_price = tds[4].text.replace(
                '￥', '').replace('\xa0', '').strip()
            print("Importing {} - {} at {}".format(payee, description, time))

            category = get_category(description, payee)
            if (payee == "自动还款" or payee == "掌上生活还款"):
                description = payee
                category = "Assets:DepositCard:CMB9843"
            flag = "*"
            amount = float(real_price.replace(',', ''))
            meta = {}
            entry = Transaction(meta, time, flag, payee,
                                description, data.EMPTY_SET, data.EMPTY_SET, [])

            if real_currency == trade_currency:
                data.create_simple_posting(
                    entry, category, trade_price, trade_currency)
            else:
                trade_amount = Amount(Decimal(trade_price), trade_currency)
                real_amount = Amount(Decimal(abs(round(float(
                    real_price), 2))) / Decimal(abs(round(float(trade_price), 2))), real_currency)
                posting = Posting(category, trade_amount,
                                    None, real_amount, None, None)
                entry.postings.append(posting)

            data.create_simple_posting(entry, account, None, None)
            transactions.append(entry)
        return transactions



        #  date = data[0]
        #  description = data[3]
        #  currency = "CNY"
        #  if data[4].strip():
            #  amount = -float(data[4].replace(',', ''))
        #  else:
            #  amount = float(data[5].replace(',', ''))

        #  print(get_notsure(date, "", description, amount, currency, account))


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    load_dotenv()
    cmb_path = os.getenv("CMBPATH")
    transactions = parse_cmb(cmb_path)
    with open("../temp.bean", "w") as f:
        printer.print_entries(transactions, file=f)

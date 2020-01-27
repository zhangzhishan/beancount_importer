import io
import sys
import os
from common import *
from dotenv import load_dotenv

def parse_boc(filename):
    account = "Liabilities:CreditCard:BOC"
    with open(filename, 'r', encoding="UTF-8") as f:
        for line in f.readlines()[0:]:
            line = line.strip()
            data = line.split('\t')
            date = data[0]
            description = data[3]
            currency = "CNY"
            if data[4].strip():
                amount = -float(data[4].replace(',', ''))
            else:
                amount = float(data[5].replace(',', ''))

            print(get_notsure(date, description, amount, currency, account))

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    load_dotenv()
    boc_path = os.getenv("BOCPATH")
    parse_boc(boc_path)
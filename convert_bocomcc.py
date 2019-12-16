import io
import sys
import os
from common import *
from dotenv import load_dotenv

def parse_bocm(filename):
    with open(filename, 'r', encoding="UTF-8") as f:
        for line in f.readlines()[1:]:
            line = line.strip()
            data = line.split('\t')
            date = data[0].replace('/', '-')
            description = data[2]
            currency = data[4].split(' ')[0]
            amount = float(data[4].split(' ')[1])
            print(get_notsure(date, description, amount, currency, "Liabilities:CreditCard:BCM"))

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    load_dotenv()
    bocm_path = os.getenv("BOCMPATH")
    parse_bocm(bocm_path)
#! /usr/bin/env python
# coding: UTF-8

import json
import argparse
import csv
import datetime
import os
import io
import sys
from os import path
import locale


EXPENSES_TMPLATE = """%s * %s
    %s                 -%s %s
    Expenses:%s                 +%s %s
"""

EXPENSES_REFUND_TMPLATE = """%s * %s
    %s                 +%s %s
    Expenses:%s                 -%s %s
"""

COMMON_TEMPLATE = """%s * %s
    %s                 +%s %s
    %s                 -%s %s
"""



def load_json(filename):
    fd = open(filename, 'r', encoding="UTF-8")
    data = fd.read()
    js = json.loads(data)
    fd.close()
    return js

def load_csv(filename, is_strip_head=False):
    fd = open(filename, 'r', encoding="UTF-8")
    csv_reader = csv.reader(fd, delimiter=',')
    records = []
    for row in csv_reader:
        records.append(tuple(row))
    return records[1:] if is_strip_head else records


def build_records(mapping, record):
    def description_and_tags(desc, tags):
        if tags:
            tags = tags.split(";")
            beancount_tag = ""
            for tag in tags:
                if tag.strip():
                    beancount_tag += "#" + mapping['tags'][tag.strip()] + " "
            return '"%s" %s' % (desc, beancount_tag)
        else:
            return '"%s"' % desc
    name, _, account, transfers_to, description, category, date, _, amount, currency, _, tags = record

    if name:
        # This record only contains the current balance in this account
        pass
    else:
        time = datetime.datetime.strptime(date, "%m/%d/%Y")
        time = time.strftime('%Y-%m-%d')
        amount = locale.atof(amount)
        if transfers_to:
            # This is a transfer between accounts record
            if amount > 0:
                # dedup the same transfer in different accounts
                return COMMON_TEMPLATE % (time, description_and_tags(description, tags), mapping['accounts'][account], 
                    amount, currency, mapping['accounts'][transfers_to], amount, currency)
        else:
            if amount > 0 and "Refund" not in description and "退货" not in description and "退款" not in description:
                # Income, refund is added to expenses
                if category:
                    return COMMON_TEMPLATE % (time, description_and_tags(description, tags), mapping['accounts'][account], 
                        amount, currency, mapping['incomes'][category], amount, currency)
                else:
                    # for new balance
                    return COMMON_TEMPLATE % (time, description_and_tags(description, tags), mapping['accounts'][account], 
                        amount, currency, "Income:Newbalance", amount, currency)
            else:
                if amount < 0:
                    amount = abs(amount)
                    if category:
                        return EXPENSES_TMPLATE % (time, description_and_tags(description, tags), mapping['accounts'][account], 
                            amount, currency, mapping['expenses'][category], amount, currency)
                    else:
                        # for new balance
                        return COMMON_TEMPLATE % (time, description_and_tags(description, tags), mapping['accounts'][account], 
                            amount, currency, "Expenses:Newbalance", amount, currency)
                else:
                    # refund
                    return EXPENSES_REFUND_TMPLATE % (time, description_and_tags(description, tags), mapping['accounts'][account], 
                            amount, currency, mapping['expenses'][category], amount, currency)


def print_records(mapping, records):
    for record in records:
        beancount_record = build_records(mapping, record)
        if beancount_record:
            print(build_records(mapping, record))


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    mapping = load_json(path.join(os.path.dirname(os.path.realpath(__file__)), 'map.json'))
    records = load_csv('../documents/moneywiz/201908report.csv', True)
    print_records(mapping, records)

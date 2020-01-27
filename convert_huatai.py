#! /usr/bin/env python
# coding: UTF-8

import json
import argparse
import csv
import datetime
import os
import io
import sys
from os.path import isfile, join, basename
import locale
import time


BUY_STOCK_TEMPLATE = """%s * "%s"
    Assets:Stock:Positions     +%s %s {%s CNY}
    Expenses:Stock:Brokerage   +%s CNY
    Expenses:Stock:Stamptax    +%s CNY
    Expenses:Stock:Transferfee +%s CNY
    Assets:Broker:China        -%s CNY

"""

SELL_STOCK_TEMPLATE = """%s * "%s"
    Assets:Stock:Positions     -%s %s {}
    Expenses:Stock:Brokerage   +%s CNY
    Expenses:Stock:Stamptax    +%s CNY
    Expenses:Stock:Transferfee +%s CNY
    Assets:Broker:China        +%s CNY
    Income:Trade:PnL

"""

DIVIDEND_STOCK_TEMPLATE = """%s * "%s"
    Assets:Broker:China        %s CNY
    Income:Trade:Dividend

"""


def load_json(filename):
    fd = open(filename, 'r', encoding="UTF-8")
    data = fd.read()
    js = json.loads(data)
    fd.close()
    return js

def load_csv(filename, is_strip_head=False):
    fd = open(filename, 'r', encoding="gb2312")
    csv_reader = csv.reader(fd, delimiter='\t')
    records = []
    for row in csv_reader:
        for i in range(len(row)):
            row[i] = row[i].strip("=\"")
        records.append(tuple(row))
    return records[1:] if is_strip_head else records


def build_records(record):
    # ('发生日期', '备注', '证券代码', '证券名称', '买卖标志', '成交数量', '成交价格', '成交金额', '佣金', '印花税', '过户费', '发生金额', '剩余金额', '申报序号', '股东代码', '席位代码', '委托编号', '成交编号', '证券数量', '其他费')
    date, trade, stock_code, stock_name, trade_operation, stock_share, stock_price, _, fee_1, fee_2, fee_3, total_money, *_ = record

    date = datetime.datetime.strptime(date, "%Y%m%d")
    date = date.strftime('%Y-%m-%d')
    # fee = locale.atof(fee_1) + locale.atof(fee_2) + locale.atof(fee_3)
    stock_share = abs(locale.atof(stock_share))
    total_money = locale.atof(total_money)
    only_pass_operation = ["新股入帐", "申购配号", "托管转出", "指定交易",
                           "交收资金冻结取消", "交收资金冻结", "市值申购中签",
                           "质押回购拆出", "拆出质押购回"]
    if trade_operation == "证券买入" or trade_operation == "新股申购确认缴款":
        return BUY_STOCK_TEMPLATE % (date, trade + " " + stock_name, stock_share, "S" + stock_code,
                                     stock_price, fee_1, fee_2, fee_3, abs(total_money))
    elif trade_operation == "证券卖出":
        return SELL_STOCK_TEMPLATE % (date, trade + " " + stock_name, stock_share, "S" + stock_code,
                                      fee_1, fee_2, fee_3, abs(total_money))
    elif trade_operation == "股息入帐":
        return DIVIDEND_STOCK_TEMPLATE % (date, trade + " " + stock_name, abs(total_money))
    elif trade_operation == "股息红利税补缴":
        return DIVIDEND_STOCK_TEMPLATE % (date, trade + " " + stock_name, (total_money))
    elif trade_operation in only_pass_operation:
        pass
    else:
        print(trade_operation)



def print_records(records):
    for record in records:
        beancount_record = build_records((record))
        if beancount_record:
            print(beancount_record)

def print_records_to_file(records, filename):
    with open(filename, "a", encoding="utf-8") as f:
        for record in records:
            beancount_record = build_records((record))
            if beancount_record:
                f.write(beancount_record)

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    folder = "../documents/huatai/"
    # out_filename = "../stock.bean"
    out_filename = "../stock" + str(time.time()) + ".bean"
    allfiles = [f for f in os.listdir(folder) if isfile(os.path.join(folder, f))]
    for filename in allfiles:
        # print(filename)
        # print(os.path.splitext(filename)[0])
        records = load_csv(os.path.join(folder, filename), True)
        # print_records(records)
        print_records_to_file(records, out_filename)

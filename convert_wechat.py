import io
import sys
import os
from common import *
from dotenv import load_dotenv

def parse_wechat(filename):
    account_map = {"工商银行(6613)": "Assets:DepositCard:ICBC26613", 
                   "零钱": "Assets:VirtualCard:Wechat:ZZS",
                   "招商银行(9843)": "Assets:DepositCard:CMB9843",
                   "民生银行(8531)": "Liabilities:CreditCard:CMBC8531"}
    ignore_account = {"中国银行(1163)"}
    with open(filename, 'r', encoding="UTF-8") as f:
        for line in f.readlines()[17:]:
            line = line.strip()
            data = line.split(',')
# 交易时间,交易类型,交易对方,商品,收/支,金额(元),支付方式,当前状态,交易单号,商户单号,备注
            date = data[0].split(' ')[0] # 付款时间
            status = data[7].strip() # 当前状态
            trade_type = data[1].strip() # 交易类型
            description = trade_type + ", " + data[3].strip("\"")
            trade_account = data[6].strip()
            counterpart = data[2].strip() # 交易对方
            currency = "CNY"
            amount_string = data[5].replace('¥', '')
            amount = float(amount_string)
            if trade_account in ignore_account:
                continue

            if status == '支付成功' or status == '已全额退款' or '已退款' in status or \
                trade_type == "扫二维码付款":
                if status == '已全额退款' or '已退款' in status:
                    amount = -amount
                print(get_notsure(date, counterpart, description, amount, currency, account_map[trade_account]))

                # account = get_account_by_guess(row['交易对方'], row['商品'], time)
                # if account == "Unknown":
                #     entry = replace_flag(entry, '!')
                # data.create_simple_posting(entry, account, amount_string, 'CNY')
                # data.create_simple_posting(entry, accounts[row['支付方式']], None, None)

            elif status == '已存入零钱':
                # 2020-01-01 09:40:58,微信红包,壁立千仞,"/",收入,¥0.16,/,已存入零钱,1000039501000001016020205183374	,1000039501202001016020205183374	,"/"
                amount = -amount
                if '微信红包' in trade_type:
                    print(get_notsure(date, counterpart, description, amount, currency, "Assets:VirtualCard:Wechat:ZZS"))
                    # data.create_simple_posting(entry, Account红包, None, 'CNY')
                else:
                    print(line)
                #     income = get_income_account_by_guess(row['交易对方'], row['商品'], time)
                #     if income == 'Income:Unknown':
                #         entry = replace_flag(entry, '!')
                #     data.create_simple_posting(entry, income, None, 'CNY')
                # data.create_simple_posting(entry, Account余额, amount_string, 'CNY')
            elif trade_type == "转账":
                print(get_notsure(date, counterpart, description, amount, currency, account_map[trade_account]))
            else:
                print(line)

            # print(get_notsure(date, description, amount, currency, account))

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    load_dotenv()
    wechat_path = os.getenv("WECHATPATH")
    parse_wechat(wechat_path)
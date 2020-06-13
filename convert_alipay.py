import io
import sys
import os
from common import *
from dotenv import load_dotenv

def parse_alipay(filename):
    account = "Liabilities:CreditCard:CITIC"
    account_alipay = "Assets:VirtualCard:Alipay:ZZS"
# 交易号 ,商家订单号 ,交易创建时间 ,付款时间 ,最近修改时间 ,交易来源地 ,类型 ,交易对方 ,商品名称 ,金额（元） ,收/支 ,交易状态 ,服务费（元） ,成功退款（元） ,备注,资金状态 ,

    with open(filename, 'r', encoding="gbk") as f:
        for line in f.readlines()[5:-8]:
            line = line.strip()
            data = line.split(',')

            date = data[2].split(' ')[0] # 付款时间
            counterpart = data[7].strip() # 交易对方
            description = data[8].strip() # 商品名称
            currency = "CNY"
            money_status = data[15].strip()
            amount = float(data[9])
            if money_status == "资金转移": # 资金状态
                if data[11] == "还款成功":
                    print("还款成功")
                    print(line)
                elif data[11] == "交易成功" and description == "余额宝-自动转入":
                    continue
                else:
                    print(line)
            elif money_status == "已支出":
                print(get_notsure(date, counterpart, description, amount, currency, account))
            elif money_status == "已收入":
                if "余额宝" in description:
                    print(get_yuebao(date, description, amount, currency, account_alipay))
                elif data[11].strip() == "退款成功": # 退款
                    print(get_notsure(date, counterpart, description, -1 * amount, currency, account))
                else: # 二手
                    print(sell_something(date, description, amount, currency, account_alipay))
                    print(line)
            elif data[11].strip() == "交易关闭": # 交易状态
                continue
            else:
                print(line)

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    load_dotenv()
    alipay_path = os.getenv("ALIPAYPATH")
    parse_alipay(alipay_path)
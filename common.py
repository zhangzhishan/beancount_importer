import json
import os
from dotenv import load_dotenv


NOTSURE_TEMPLATE = """%s * "%s" "%s"
    %s                 + %s %s
    %s
"""

NOTSURE_INCOME_TEMPLATE = """%s * "%s" "%s"
    %s                  %s %s
    %s
"""

SELL_TEMPLATE = """%s * "%s"
    Income:Selling                 - %s %s
    %s
"""

YUEBAO_TEMPLATE = """%s * "%s"
    Income:Interest:Ali                 - %s %s
    %s
"""

def load_json(filename):
    fd = open(filename, 'r', encoding="UTF-8")
    data = fd.read()
    js = json.loads(data)
    fd.close()
    return js

def sell_something(datetime, description, amount, currency, account):
    return SELL_TEMPLATE % (datetime, description,
                            amount, currency,
                            account)

def get_yuebao(datetime, description, amount, currency, account):
    return YUEBAO_TEMPLATE % (datetime, description,
                              amount, currency,
                              account)

def get_notsure(datetime, counterpart, description, amount, currency, account):
    category = get_category(description, counterpart)
    if amount < 0:
        return NOTSURE_INCOME_TEMPLATE % (datetime, counterpart, description,
                                          category, amount, currency,
                                          account)
    return NOTSURE_TEMPLATE % (datetime, counterpart, description,
                               category, amount, currency,
                               account)

def get_category(description, counterpart = ""):
    category = "Expenses:NotSure"
    load_dotenv()
    description_category_map_path = os.getenv("DESCRIPTIONMAPPATH")
    mapping = load_json(description_category_map_path)
    for key in mapping:
        if key in description or key in counterpart:
            category = mapping[key]
            break
    return category

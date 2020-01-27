import json
import os
from dotenv import load_dotenv


NOTSURE_TEMPLATE = """%s * "%s"
    %s                 + %s %s
    %s
"""

NOTSURE_INCOME_TEMPLATE = """%s * "%s"
    %s                  %s %s
    %s
"""

def load_json(filename):
    fd = open(filename, 'r', encoding="UTF-8")
    data = fd.read()
    js = json.loads(data)
    fd.close()
    return js

def get_notsure(datetime, description, amount, currency, account):
    category = "Expenses:NotSure"
    if amount < 0:
        return NOTSURE_INCOME_TEMPLATE % (datetime, description,
                                          category, amount, currency,
                                          account)
    load_dotenv()
    description_category_map_path = os.getenv("DESCRIPTIONMAPPATH")
    mapping = load_json(description_category_map_path)
    for key in mapping:
        if key in description:
            category = mapping[key]
            break
    return NOTSURE_TEMPLATE % (datetime, description,
                               category, amount, currency,
                               account)
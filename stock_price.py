from datetime import date
import json
import easyquotation


CURRENCY = "CNY"
TIME_DELAY = 1
# my_stock = ["002304", "600018", "600026", "600837", "601872", "000100", "000425", "601021", "511880"]

quotation = easyquotation.use("sina")
all_data = quotation.real(my_stock)
print(all_data)
for key, data in all_data.items():
    print(date.today().strftime("%Y-%m-%d") + " price " + 'S' + key + " " + str(data["now"]) + " " + CURRENCY + " ; " + data["name"])


# class CoinmarketcapError(ValueError):
#     "An error from the Coinmarketcap API."

# class Source(source.Source):
#     def _get_price_for_date(self, ticker, date=None):

#         if date == None:
#             date_string = "0"
#         else:
#             date_string = date.strftime("%Y%m%d")

#         url = "dd"

#         try:
#             content = requests.get(url).content
#             content = content.split(b"=")[1]
#             data = json.loads(content)
#             price = 0
#             date_int = int(date_string)
#             found_date = False

#             if date_string != "0":
#                 for item in data:
#                     if item[0] == date_string or int(item[0]) > date_int:
#                         date = item[0]
#                         price = item[1]
#                         found_date = True
#                         break

#             if not found_date:
#                 item = data[len(data) - 1]
#                 price = item[1]
#                 date = item[0]

#             parsed_date = parse_date_liberally(date)
#             date = datetime(parsed_date.year, parsed_date.month, parsed_date.day)

#             price = D(price)

#             return source.SourcePrice(price, date, CURRENCY)

#         except KeyError:
#             raise CoinmarketcapError("Invalid response from 10jqka: {}".format(repr(content)))
#         except AttributeError:
#             raise CoinmarketcapError("Invalid response from 10jqka: {}".format(repr(content)))

#     def get_latest_price(self, ticker):
#         return self._get_price_for_date(ticker, None)

#     def get_historical_price(self, ticker, time):
#         return self._get_price_for_date(ticker, time)
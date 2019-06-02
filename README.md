# beancount_importer

This is an importer for converting moneywiz3 exported csv file to beancount records.

## how to use it?
1. Rename `example.map.json` to `map.json`
2. Add the exported moneywiz3 file `report.csv` to current folder.
3. Fill the `expenses`, `incomes`, `accounts`, `tags` in `example.map.json`. The key is value in your moneywiz3, and the value is what your want in beancount record.
4. Run `python gen_account.py > account.bean` to open your account.
5. Run `python moneywiz_converter.py > temp.bean` to generate beancount records.
6. Check and combine with your original beancount document.


## Reference
https://github.com/lyricat/beancount-converter
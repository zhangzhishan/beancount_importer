import re


input_filename = "../2019.bean"
main_filename = "../2019new.bean"
splited_filename = "../cashout.bean"
keyword = "套现"
in_cash_out = False
with open(input_filename, "r", encoding="UTF-8") as input_file:
    with open(main_filename, "w", encoding="UTF-8") as output_file:
        with open(splited_filename, "w", encoding="UTF-8") as cash_out_file:
            for line in input_file:
                if keyword in line:
                    in_cash_out = True
                    cash_out_file.write(line)
                elif line.startswith("20"):
                    in_cash_out = False
                    output_file.write(line)
                else:
                    if not in_cash_out:
                        output_file.write(line)
                    else:
                        cash_out_file.write(line)
                
    #     pass
    # record = ""
    # nb_line = 0
    # nb_line_record = 0
    # for line in f.readlines():
    #     nb_line += 1
    #     nb_line_record += 1
    #     line = line.strip()
    #     if line.startswith("20"):
    #         # this is a new record
    #         encoded_record = base64.b64encode(record.encode("utf-8")) 
    #         if encoded_record in record_set:
    #             print("same result from line %d to %d: \n %s" % (nb_line - nb_line_record, nb_line - 1, record))
    #         else:
    #             record_set.add(encoded_record)
    #             record = line + "\n"
    #             nb_line_record = 0
    #     elif not line:
    #         pass
    #     else:
    #         record += line
    #         record += "\n"
            # print(line.strip())
    # print(record_set)
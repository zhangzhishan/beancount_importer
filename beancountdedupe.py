import base64

filename = "../2019.bean"
record_set = set();
with open(filename, encoding="UTF-8") as f:
    record = ""
    nb_line = 0
    nb_line_record = 0
    for line in f.readlines():
        nb_line += 1
        nb_line_record += 1
        line = line.strip()
        if line.startswith("20"):
            # this is a new record
            encoded_record = base64.b64encode(record.encode("utf-8")) 
            if encoded_record in record_set:
                print("same result from line %d to %d: \n %s" % (nb_line - nb_line_record, nb_line - 1, record))
            else:
                record_set.add(encoded_record)
                record = line + "\n"
                nb_line_record = 0
        elif not line:
            pass
        else:
            record += line
            record += "\n"
            # print(line.strip())
    # print(record_set)
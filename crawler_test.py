# -*- coding: utf-8 -*-
from util.xlsx.reader import XlsxReader
from util.xlsx.writer import write_xlsx
import re, json

if __name__ == "__main__":
    keys = [
        'lat', 'busi_area', 'payment', 'floor',
        'house_id', 'price', 'house_type', 'area',
        'lng', '月付', '季付', '半年付', '年付'        
    ]
    reader = XlsxReader("ziroom.xlsx")
    v = reader.get_sheet_data("ziroom")

    with write_xlsx("ziroom_clean.xlsx", "ziroom") as f:
        for s in v:
            for idx, sv in enumerate(s):
                if idx == 1 and sv is not None:
                    [s.append(x) for x in json.loads(sv.replace('\'','\"'))]
            s.pop(1)
            f.write_dict(dict(zip(keys, s)))
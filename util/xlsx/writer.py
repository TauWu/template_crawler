# -*- coding: utf-8 -*-

from openpyxl import Workbook
from .reader import XlsxReader
import os

class XlsxWriter(XlsxReader):

    def __init__(self, filename, sheetname):
        self.filename       = filename
        self.sheetname      = sheetname
        XlsxReader.__init__(self, filename)
        self._sheet         = self._wb.active
        self._title         = {t:chr(i+65) for i, t in enumerate(self.titles_dict[sheetname])}
        self._title_cur     = len(self._title.keys())
        self._cur           = len(self.get_sheet_content_dict(self.sheetname)) + 2

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._wb.save(self.filename)

    def write_dict(self, data):
        self.write_title(data)
        self.write_data(data)

    def write_title(self, data):
        for k in data.keys():
            if k not in self._title.keys():
                self._title[k] = chr(65+self._title_cur)
                self._title_cur += 1
        for k, v in zip(self._title.keys(), self._title.values()):
            self._sheet["%s%d"%(v, 1)] = k
    
    def write_data(self, data):
        for k, v in zip(data.keys(), data.values()):
            self._sheet["%s%d"%(self._title[k], self._cur)] = str(v)
        self._cur += 1
        

def write_xlsx(filename, sheetname):
    if not os.path.exists(filename):
        wb = Workbook()
        st = wb.active
        st.title = sheetname
        wb.save(filename)
        
    return XlsxWriter(filename, sheetname)

if __name__ == "__main__":
    with write_xlsx("./test.xlsx", "test") as x:
        x.write_dict(
            {
                "test1":'Test1',
                "test2":'Test2',
                "house_id":1230601
            }
        )
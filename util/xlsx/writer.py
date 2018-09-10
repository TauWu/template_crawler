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
        self._title         = dict()
        self._title_cur     = len(self._title.keys())
        self._cur           = len(self.get_sheet_content_dict(self.sheetname)) + 2

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._wb.save(self.filename)

    def write_dict(self, data, orderlist=None):
        self.write_title(data, orderlist)
        self.write_data(data, orderlist)

    def write_title(self, data, orderlist=None):
        title_list = list()
        if orderlist is not None:
            title_list = orderlist
        else:
            title_list = data.keys()

        for k in title_list:
            if k not in self._title.keys():
                self._title[k] = chr(65+self._title_cur)
                self._title_cur += 1

        for k, v in zip(self._title.keys(), self._title.values()):
            self._sheet["%s%d"%(v, 1)] = k

    
    def write_data(self, data, orderlist=None):
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
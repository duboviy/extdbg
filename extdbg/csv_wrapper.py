import sys
import csv


PY3 = sys.version > '3'


# Copyright for UnicodeReader and UnicodeWriter, Lennart Regebro
# http://python3porting.com/problems.html#csv-api-changes
class UnicodeReader:
    def __init__(self, filename, dialect=csv.excel, encoding="utf-8", **kw):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw

    def __enter__(self):
        if PY3:
            self.f = open(self.filename, 'rt', encoding=self.encoding, newline='')
        else:
            self.f = open(self.filename, 'rb')
        self.reader = csv.reader(self.f, dialect=self.dialect, **self.kw)
        return self
        
    def __exit__(self, type, value, traceback):
        self.f.close()

    def next(self):
        row = next(self.reader)
        if PY3:
            return row
        return [s.decode("utf-8") for s in row]
    
    __next__ = next

    def __iter__(self):
        return self


class UnicodeWriter:
    def __init__(self, filename, dialect=csv.excel, encoding="utf-8", **kw):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw
        
    def __enter__(self):
        if PY3:
            self.f = open(self.filename, 'wt', encoding=self.encoding, newline='')
        else:
            self.f = open(self.filename, 'wb')
        self.writer = csv.writer(self.f, dialect=self.dialect, **self.kw)
        return self
        
    def __exit__(self, type_, value, traceback_):
        self.f.close()

    def writerow(self, row):
        if not PY3:
            row = [s.encode(self.encoding) for s in row]
        self.writer.writerow(row)
        
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def transform_csv(src, dst, transformation, encoding='utf-8'):
    """
    Filter contents of file named `src` into file named `dst` row by row,
    using function `transformation` which receives row of csv in iterable
    and its number and returns iterable with rows of destination file.
    """
    with UnicodeReader(src, encoding=encoding, delimiter='\t') as reader, \
        UnicodeWriter(dst, encoding=encoding, delimiter='\t') as writer:
        for i, src_row in enumerate(reader):
            for dst_row in transformation(src_row, i):
                writer.writerow(dst_row)

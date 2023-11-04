# -*- coding: utf-8 -*-

import camelot
import io
from pypdf import PdfReader
import tempfile


class PDFParser:

    def __init__(self, bytes):
        self._tempfile = tempfile.NamedTemporaryFile(suffix='.pdf')
        self._tempfile.write(bytes)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self._tempfile.close()

    def parse_tables(self):
        self._tempfile.seek(0, 0)

        tables = camelot.read_pdf(self._tempfile.name, pages='all', strip_text='\n', copy_text=('v', 'h'))
        return [
            dict(
                rows=table.data,
                title='',
                unit='',
            )
            for table in tables
        ]

    def parse_text(self):
        self._tempfile.seek(0, 0)

        stream = io.StringIO()
        reader = PdfReader(self._tempfile.name)
        for page in reader.pages:
            stream.write(page.extract_text())
        return stream.getvalue()


if __name__ == '__main__':
    with open('data/集团利润表.pdf') as f:
        bytes = f.read()

    with PDFParser(bytes) as p:
        tables = p.parse_tables()
        print('tables', tables)

        text = p.parse_text()
        print('text', text)

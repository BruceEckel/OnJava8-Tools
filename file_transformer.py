import io
import sys
from pathlib import Path


class TransformFile:
    def __init__(self, infile, outfile):
        infile_path = Path(infile)
        if not infile_path.exists():
            print("ERROR: Can't find {}".format(infile))
            sys.exit(1)
        self.source = infile_path.open(encoding="utf8").read()
        self.outfile = Path(outfile)
        self.out = io.StringIO()
        # print('__init__({}, {})'.format(infile, outfile))

    def __enter__(self):
        # print('__enter__()')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print('__exit__()')
        with self.outfile.open('w', encoding="utf8") as outfile:
            outfile.write(self.out.getvalue())

    # Some syntax sugar:
    def get(self):
        "The source document"
        return self.source

    def put(self, str):
        "Write to the destination document"
        self.out.write(str)

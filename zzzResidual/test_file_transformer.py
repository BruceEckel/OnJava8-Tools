from file_transformer import TransformFile
from pathlib import Path
import shutil
import os

if not Path("test_in.txt").exists():
    shutil.copy("test_file_transformer.py", "test_in.txt")


def test1():
    with TransformFile("test_in.txt", "test1_out.txt") as tf:
        tf.out.write("=== Test1 Tranformed File ===\n\n")
        tf.put(tf.get())


if __name__ == '__main__':
    test1()
    os.system("cat test1_out.txt")
    os.remove("test1_out.txt")
    os.remove("test_in.txt")

# Name   : Shree Vashist
# Roll No: 2501730459
# Branch : CSE (AIML) - Section G
# Project: DAA Capstone - Huffman Coding File Compression

"""Simple tests. Run:  python test_huffman.py"""
import os
from huffman import compress_file, decompress_file

cases = {
    "normal text": b"hello world, this is huffman coding!",
    "single char": b"aaaaaaaaaa",
    "one byte": b"x",
    "newlines": b"line1\nline2\r\nline3\n",
    "all bytes": bytes(range(256)) * 3,
}

for name, data in cases.items():
    with open("t.txt", "wb") as f:
        f.write(data)
    compress_file("t.txt", "t.huff")
    decompress_file("t.huff", "t.out")
    ok = open("t.out", "rb").read() == data
    print("%-12s : %s" % (name, "PASS" if ok else "FAIL"))

for f in ("t.txt", "t.huff", "t.out"):
    os.remove(f)

# Name   : Shree Vashist
# Roll No: 2501730459
# Branch : CSE (AIML) - Section G
# Project: DAA Capstone - Huffman Coding File Compression

"""
analysis.py
Measures running time and file sizes for different input sizes so we can
check the time complexity of Huffman coding experimentally.
"""

import os
import random
import string
import time
from huffman import (calculate_frequencies, build_huffman_tree, generate_codes,
                     encode_data, compress_file)

random.seed(1)


def make_text(n):
    """Random English-like text of n characters (letters weighted unevenly)."""
    letters = "etaoinshrdlu" * 5 + string.ascii_lowercase + "    " * 6 + ".,\n"
    return "".join(random.choice(letters) for _ in range(n)).encode()


def run():
    sizes = [1000, 10000, 50000, 100000, 500000]
    print("\n%-10s %-12s %-12s %-10s %-12s" %
          ("Size(B)", "Compressed", "Saved %", "Time(ms)", "Time/n (us)"))
    print("-" * 60)

    for n in sizes:
        data = make_text(n)
        with open("_tmp.txt", "wb") as f:
            f.write(data)

        start = time.perf_counter()
        compress_file("_tmp.txt", "_tmp.huff")
        ms = (time.perf_counter() - start) * 1000

        comp = os.path.getsize("_tmp.huff")
        saved = (n - comp) / n * 100
        print("%-10d %-12d %-12.2f %-10.2f %-12.3f" % (n, comp, saved, ms, ms * 1000 / n))

    os.remove("_tmp.txt")
    os.remove("_tmp.huff")

    print("""
Observation:
 - Time per byte stays almost constant, so total time grows linearly with
   file size n  ->  O(n) for counting + encoding.
 - Tree building depends only on number of unique characters k, which is
   at most 256, so it takes O(k log k) (tiny compared to n).
 - Very small files save little (or even grow) because the frequency table
   stored in the header is extra overhead.
""")


if __name__ == "__main__":
    run()

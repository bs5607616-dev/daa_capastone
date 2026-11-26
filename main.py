# Name   : Shree Vashist
# Roll No: 2501730459
# Branch : CSE (AIML) - Section G
# Project: DAA Capstone - Huffman Coding File Compression

"""
main.py
Menu driven program for the Huffman Coding compression project.
Run:  python main.py
"""

import os
from huffman import (calculate_frequencies, build_huffman_tree, generate_codes,
                     compress_file, decompress_file, file_size,
                     average_code_length)


def show_char(b):
    """Make special characters readable when printing."""
    names = {10: "\\n", 13: "\\r", 9: "\\t", 32: "' ' (space)"}
    if b in names:
        return names[b]
    return chr(b) if 33 <= b < 127 else "0x%02X" % b


def show_frequencies_and_codes(path):
    with open(path, "rb") as f:
        data = f.read()
    if not data:
        print("File is empty.")
        return
    freq = calculate_frequencies(data)
    codes = generate_codes(build_huffman_tree(freq))

    print("\n%-14s %-10s %-10s %s" % ("Character", "Frequency", "Code", "Code length"))
    print("-" * 50)
    for sym in sorted(freq, key=lambda s: -freq[s]):
        print("%-14s %-10d %-10s %d" % (show_char(sym), freq[sym], codes[sym], len(codes[sym])))
    print("\nUnique characters :", len(freq))
    print("Average code length: %.3f bits (normal ASCII = 8 bits)" % average_code_length(freq, codes))


def do_compress():
    path = input("Enter input text file name: ").strip()
    if not os.path.isfile(path):
        print("File not found!")
        return
    if file_size(path) == 0:
        print("File is empty, nothing to compress.")
        return
    out = path + ".huff"
    compress_file(path, out)
    orig, comp = file_size(path), file_size(out)
    print("\nCompressed file saved as:", out)
    print("Original size   : %d bytes" % orig)
    print("Compressed size : %d bytes" % comp)
    print("Space saved     : %.2f %%" % ((orig - comp) / orig * 100))
    print("Compression ratio: %.3f" % (comp / orig))


def do_decompress():
    path = input("Enter compressed (.huff) file name: ").strip()
    if not os.path.isfile(path):
        print("File not found!")
        return
    out = path[:-5] + "_decoded.txt" if path.endswith(".huff") else path + "_decoded.txt"
    decompress_file(path, out)
    print("Decompressed file saved as:", out)


def do_verify():
    path = input("Enter original text file name: ").strip()
    if not os.path.isfile(path):
        print("File not found!")
        return
    tmp_c, tmp_d = path + ".tmp.huff", path + ".tmp.out"
    compress_file(path, tmp_c)
    decompress_file(tmp_c, tmp_d)
    with open(path, "rb") as a, open(tmp_d, "rb") as b:
        same = a.read() == b.read()
    os.remove(tmp_c)
    os.remove(tmp_d)
    print("Decoded file matches original: ", "YES (lossless)" if same else "NO (error!)")


def menu():
    while True:
        print("\n===== HUFFMAN CODING FILE COMPRESSION =====")
        print("1. Show character frequencies and Huffman codes")
        print("2. Compress a file")
        print("3. Decompress a file")
        print("4. Verify compress + decompress gives same file")
        print("5. Run performance analysis (time / space complexity)")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            p = input("Enter text file name: ").strip()
            if os.path.isfile(p):
                show_frequencies_and_codes(p)
            else:
                print("File not found!")
        elif choice == "2":
            do_compress()
        elif choice == "3":
            do_decompress()
        elif choice == "4":
            do_verify()
        elif choice == "5":
            import analysis
            analysis.run()
        elif choice == "6":
            print("Bye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    menu()

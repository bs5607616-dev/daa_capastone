# Name   : Shree Vashist
# Roll No: 2501730459
# Branch : CSE (AIML) - Section G
# Project: DAA Capstone - Huffman Coding File Compression

"""
huffman.py
Core logic for Huffman Coding file compression.

Steps:
 1. Count frequency of every character (byte)
 2. Build the Huffman Tree using a min-heap
 3. Generate binary codes by walking the tree
 4. Encode the data and write it to a compressed file
 5. Decode the compressed file back to the original
"""

import heapq
import os
import struct


class Node:
    """A node of the Huffman tree."""

    def __init__(self, symbol, freq):
        self.symbol = symbol      # byte value (0-255), None for internal nodes
        self.freq = freq
        self.left = None
        self.right = None

    # heapq needs to compare nodes. Ties are broken by symbol so the
    # tree is always built the same way (important for decoding).
    def __lt__(self, other):
        if self.freq == other.freq:
            a = self.symbol if self.symbol is not None else 256
            b = other.symbol if other.symbol is not None else 256
            return a < b
        return self.freq < other.freq


# ---------- Step 1: frequencies ----------
def calculate_frequencies(data):
    """Return a dict {byte: count}. Time O(n)."""
    freq = {}
    for b in data:
        freq[b] = freq.get(b, 0) + 1
    return freq


# ---------- Step 2: build tree ----------
def build_huffman_tree(freq):
    """Build the tree with a min-heap. Time O(k log k), k = unique symbols."""
    heap = [Node(sym, f) for sym, f in freq.items()]
    heapq.heapify(heap)

    if len(heap) == 0:
        return None

    while len(heap) > 1:
        left = heapq.heappop(heap)    # two smallest nodes
        right = heapq.heappop(heap)
        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)

    return heap[0]


# ---------- Step 3: generate codes ----------
def generate_codes(root):
    """Walk the tree: left edge = '0', right edge = '1'."""
    codes = {}
    if root is None:
        return codes

    # special case: only one unique symbol in the file
    if root.left is None and root.right is None:
        codes[root.symbol] = "0"
        return codes

    def walk(node, path):
        if node.left is None and node.right is None:
            codes[node.symbol] = path
            return
        walk(node.left, path + "0")
        walk(node.right, path + "1")

    walk(root, "")
    return codes


# ---------- Step 4: encoding ----------
def encode_data(data, codes):
    """Convert the data into one long string of 0s and 1s."""
    return "".join(codes[b] for b in data)


def bits_to_bytes(bit_string):
    """Pack the bit string into bytes. Returns (bytes, padding_added)."""
    padding = (8 - len(bit_string) % 8) % 8
    bit_string += "0" * padding
    out = bytearray()
    for i in range(0, len(bit_string), 8):
        out.append(int(bit_string[i:i + 8], 2))
    return bytes(out), padding


def compress_file(input_path, output_path):
    """
    Compressed file format:
      2 bytes  : number of unique symbols (k)
      k * 5    : [1 byte symbol][4 bytes frequency] for each symbol
      1 byte   : padding bits added at the end
      rest     : the encoded data
    The frequency table lets the decoder rebuild the same tree.
    """
    with open(input_path, "rb") as f:
        data = f.read()

    freq = calculate_frequencies(data)
    root = build_huffman_tree(freq)
    codes = generate_codes(root)
    bit_string = encode_data(data, codes)
    packed, padding = bits_to_bytes(bit_string)

    with open(output_path, "wb") as f:
        f.write(struct.pack(">H", len(freq)))
        for sym, count in freq.items():
            f.write(struct.pack(">BI", sym, count))
        f.write(struct.pack(">B", padding))
        f.write(packed)

    return codes, freq


# ---------- Step 5: decoding ----------
def decode_bits(bit_string, root, total_symbols):
    """Walk the tree bit by bit until we have decoded all symbols."""
    result = bytearray()
    if root is None:
        return bytes(result)

    # only one unique symbol: every symbol is that one
    if root.left is None and root.right is None:
        return bytes([root.symbol]) * total_symbols

    node = root
    for bit in bit_string:
        node = node.left if bit == "0" else node.right
        if node.left is None and node.right is None:
            result.append(node.symbol)
            node = root
    return bytes(result)


def decompress_file(input_path, output_path):
    with open(input_path, "rb") as f:
        k = struct.unpack(">H", f.read(2))[0]
        freq = {}
        for _ in range(k):
            sym, count = struct.unpack(">BI", f.read(5))
            freq[sym] = count
        padding = struct.unpack(">B", f.read(1))[0]
        packed = f.read()

    bit_string = "".join(format(b, "08b") for b in packed)
    if padding:
        bit_string = bit_string[:-padding]

    root = build_huffman_tree(freq)
    total = sum(freq.values())
    data = decode_bits(bit_string, root, total)

    with open(output_path, "wb") as f:
        f.write(data)


# ---------- helpers for the report ----------
def file_size(path):
    return os.path.getsize(path)


def average_code_length(freq, codes):
    total = sum(freq.values())
    if total == 0:
        return 0
    return sum(freq[s] * len(codes[s]) for s in freq) / total

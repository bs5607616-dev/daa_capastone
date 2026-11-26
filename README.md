# File Compression Using Huffman Coding

**Name:** Shree Vashist  
**Roll No:** 2501730459  
**Branch:** CSE (AIML) – Section G

**Subject:** Design and Analysis of Algorithms (DAA) – Capstone Project 3
**Language:** Python 3 (no external libraries)

## Problem Statement
Develop a file compression system using Huffman Coding that reduces the storage
space required for text files. The system calculates character frequencies,
constructs a Huffman Tree, generates binary codes, and performs encoding and
decoding. Analyse the time and space complexity and compare original and
compressed file sizes.

## Files
| File | Purpose |
|------|---------|
| `huffman.py` | Core algorithm: frequencies, tree, codes, encode, decode |
| `main.py` | Menu driven program |
| `analysis.py` | Experiment for time and size on different file sizes |
| `test_huffman.py` | Test cases (normal, single char, all bytes, etc.) |
| `sample.txt` | Sample input file |
| `huffman.html` | Website version: open it in any browser (no install needed) |

## How to Run
```
python main.py             # menu program
python analysis.py         # performance analysis only
python test_huffman.py     # run tests
```
For the website version, double-click `huffman.html` to open it in a browser.

## Algorithm
1. **Frequency count** – read the file and count each character.
2. **Build tree** – put every character in a min-heap (priority queue). Repeatedly
   remove the two nodes with lowest frequency, join them under a new parent whose
   frequency is the sum, and push it back. The last node left is the root.
3. **Generate codes** – walk the tree: left edge = `0`, right edge = `1`. The path
   to a leaf is that character's code. Frequent characters get short codes.
4. **Encode** – replace every character with its code and pack the bits into bytes.
5. **Decode** – the compressed file stores the frequency table, so the same tree is
   rebuilt. Read bits one by one, go left/right until a leaf is reached, output
   that character, return to the root.

Huffman codes are *prefix codes* (no code is the start of another), so decoding
is never ambiguous. The compression is lossless.

### Compressed file format
```
[2 bytes: unique symbols k] [k x (1 byte symbol + 4 bytes frequency)]
[1 byte: padding bits] [encoded data]
```

## Complexity Analysis
Let **n** = number of characters in the file, **k** = number of unique characters (k <= 256).

| Step | Time | Space |
|------|------|-------|
| Frequency count | O(n) | O(k) |
| Build tree (heap) | O(k log k) | O(k) |
| Generate codes | O(k) | O(k) |
| Encoding | O(n) | O(n) bits |
| Decoding | O(n) | O(n) |
| **Overall** | **O(n + k log k)** | **O(n + k)** |

Since k is at most 256 (a constant), the total time is effectively **O(n)**.

## Results
Sample file (`sample.txt`): 545 bytes -> 498 bytes (8.62 % saved). It is a very small file, so the stored frequency table takes a large share of the output.

Experiment on random English-like text (`analysis.py`):

| Original size (bytes) | Compressed (bytes) | Space saved | Time (ms) |
|----------------------:|-------------------:|------------:|----------:|
| 1,000   | 679     | 32.1 % | 0.40  |
| 10,000  | 5,467   | 45.3 % | 2.11  |
| 50,000  | 26,784  | 46.4 % | 9.95  |
| 100,000 | 53,301  | 46.7 % | 19.81 |
| 500,000 | 266,125 | 46.8 % | 97.82 |

(Times depend on the computer; yours will differ slightly.)

## Observations
- Normal English text compresses by about 45 %, since average code length is
  around 4.4 bits instead of 8 bits.
- Time grows linearly with file size, matching O(n).
- Small files save less because the frequency table in the header is overhead.
- A file with only one repeated character is handled as a special case (code `0`).
- Files with all characters equally frequent compress poorly, because Huffman
  gives them nearly equal code lengths.

## Limitations
- Stores the full frequency table (5 bytes per character); a canonical Huffman
  header would be smaller.
- Python string of bits is simple but uses more memory than a bit buffer.

## Conclusion
Huffman Coding is a greedy algorithm that produces an optimal prefix code. The
project shows it compresses text well in linear time, and the decoded output is
identical to the original file.

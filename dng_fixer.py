#!/usr/bin/python3

import re
import struct
import sys
import os
import argparse

SOI = struct.pack(">H", 0xFFD8)
SOF3 = struct.pack(">H", 0xFFC3)
EOI = struct.pack(">H", 0xFFD9)

strip_byte_counts_tag = 279

strip_byte_counts_hdr = struct.pack('<HHHH', strip_byte_counts_tag, 4, 1, 0)  #tag expects 4 Bytes long, 1 set of data, 0 offset

def main(args):
    with open(args.infile, "rb") as f:
        data = f.read()

    # SOI + SOF3 marks the start of the RAW stream
    try:
        match = re.finditer(SOI + SOF3 + b".+?" + EOI, data, re.S).__next__()
    except StopIteration:
        print("ERR: Could not find stream. Exit.")
        sys.exit(1)

    length = match.span()[1] - match.span()[0]
    print("Found RAW stream: at {}, len {}.".format(match.start(), length))

    idx_byte_counts = data[:1000].find(strip_byte_counts_hdr) + len(strip_byte_counts_hdr)  #find the value field, which comes after the tag preamble

    if idx_byte_counts < 0:
        print("Could not find StripByteCounts in header. Exit.")
        sys.exit(1)

    strip_byte_counts = struct.unpack("<L",data[idx_byte_counts:idx_byte_counts+4])[0]
    print("StripByteCounts: {}".format(strip_byte_counts))

    s = bytearray(data)
    s[idx_byte_counts:idx_byte_counts+4] = struct.pack("<L", length)

    with open(args.outfile, 'wb') as fd:
        fd.write(bytes(s))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='(Leica) DNG Fixer',
                    description='Fixes faulty DNGs that have a mismatch in StripByteCounts')
    
    parser.add_argument('-i', '--infile')
    parser.add_argument('-o', '--outfile')
    parser.add_argument('-f', '--force-overwrite', action='store_true')
    args = parser.parse_args()

    if not args.infile:
        print("ERR: input file missing. Exit.")
        sys.exit(1)
    if not args.outfile:
        print("ERR: output file missing. Exit.")
        sys.exit(1)
    if os.path.exists(args.outfile) and os.path.samefile(os.path.abspath(args.infile), os.path.abspath(args.outfile)) and not args.force_overwrite:
        print("ERR: input and output file are the same, but no -f given. Abort.")
        sys.exit(1)
    if os.path.exists(args.outfile) and not args.force_overwrite:
        print("ERR: output file exists, but no -f given. Abort.")
        sys.exit(1)
    main(args)

    
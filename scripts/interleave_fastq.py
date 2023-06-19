#!/usr/bin/env python3
import argparse

def main(forward: str, reverse: str, output: str):
    """ Interleave paired-end fastq files """
    with open(forward, "r") as f, open(reverse, "r") as r, open(output, "w") as outfile:
        for lineA in f:
            # forward reads
            outfile.write(lineA)
            lineA = next(f)
            outfile.write(lineA)
            lineA = next(f)
            outfile.write(lineA)
            lineA = next(f)
            outfile.write(lineA)
            # reverse reads
            lineB = next(r)
            outfile.write(lineB)
            lineB = next(r)
            outfile.write(lineB)
            lineB = next(r)
            outfile.write(lineB)
            lineB = next(r)
            outfile.write(lineB)
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script is used to interleave paired-end fastq files")
    parser.add_argument("-f", "--forward", type=str, dest="forward", help="Forward fastq file", required=True)
    parser.add_argument("-r", "--reverse", type=str, dest="reverse", help="Reverse fastq file", required=True)
    parser.add_argument("-o", "--outFile", type=str, dest="output", help="Outfile name after interleaved", default="interleaved_pe.fastq")
    args = parser.parse_args()
    main(args.forward, args.reverse, args.output)
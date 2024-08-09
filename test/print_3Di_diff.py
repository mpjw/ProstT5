#!/bin/python

from Bio import SeqIO
from pathlib import Path
import sys

#test_dir = Path("test")
#short_3Di_file = test_dir / "short_1000_3Di.fasta" #3Di_VSCdebug.fasta"
#long_3Di_file = test_dir / "long_3Di.fasta" #3Di_VSCdebug.fasta"

short_3Di_file = Path(sys.argv[1])
long_3Di_file = Path(sys.argv[2])
assert short_3Di_file.exists() and long_3Di_file.exists()

short_3Di_records = list(SeqIO.parse(short_3Di_file, "fasta"))
long_3Di_records = list(SeqIO.parse(long_3Di_file, "fasta"))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

for long_rec in long_3Di_records:
    #if str(long_rec.id) == "test_seq_one_AA_overlap":
    #        continue
    long_id = str(long_rec.id)
    long_seq = str(long_rec.seq)
    short_seqs = [(str(short_rec.seq), int(str(short_rec.id).replace(long_id, ''))) for short_rec in short_3Di_records if str(short_rec.id).startswith(long_id)]
    short_seq = ''.join([seq for seq, _ in sorted(short_seqs, key=lambda x: x[1])])

    print("\nlong_seq id: {}, L={}".format(long_id, len(long_seq)))

    if len(long_seq) != len(short_seq):
        print(bcolors.FAIL + "length difference: len(long_seq):{}, len(short_seq):{}".format(len(long_seq), len(short_seq)) + bcolors.FAIL)
    
    n_match = 0
    mismatch_string = ''
    for i in range(len(long_seq)):
        if short_seq[i] != long_seq[i]:
            mismatch_string += bcolors.FAIL + long_seq[i] + bcolors.ENDC
        else:
            mismatch_string += long_seq[i]
            n_match += 1
    
    print("seq id:{}".format(n_match/len(long_seq)))

    if n_match < len(long_seq):
        print(mismatch_string)


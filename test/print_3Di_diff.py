#!/bin/python

from Bio import SeqIO
from pathlib import Path
test_dir = Path("test")
short_3Di_file = test_dir / "short_1000_3Di.fasta" #3Di_VSCdebug.fasta"
long_3Di_file = test_dir / "long_3Di.fasta" #3Di_VSCdebug.fasta"

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
    if str(long_rec.id) == "test_seq_one_AA_overlap":
            continue
    long_id = str(long_rec.id)
    long_seq = str(long_rec.seq)
    short_seq = ''.join([str(short_rec.seq) for short_rec in short_3Di_records if str(short_rec.id).startswith(long_id)])

    assert len(long_seq) == len(short_seq)
    
    n_match = 0
    for i in range(len(long_seq)):
        if short_seq[i] != long_seq[i]:
            print(bcolors.FAIL + long_seq[i] + bcolors.ENDC, end='')
        else:
            print(long_seq[i], end='')
            n_match += 1
    
    print("\nSequence identity:{}\nid: {}".format(n_match/len(long_seq), long_id))


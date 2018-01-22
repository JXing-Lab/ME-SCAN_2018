#!/usr/bin/python

import subprocess as sp, argparse

parser=argparse.ArgumentParser()
parser.add_argument('--mei',nargs='*')
parser.add_argument('--r1',nargs='*')
parser.add_argument('--me_repeats',nargs='*')

args=parser.parse_args()
MEI=''.join(args.mei)
read1=''.join(args.r1)
ME_repeats=list(args.me_repeats)

fh = open(read1+"_"+MEI+"_blast.filter","r")
data = fh.readlines()
fh.close()

out = {}
for me in ME_repeats:
	out[me] = open(read1+"_"+me+"_blast.filter","w")

for row in range(0,len(data),1):
        temp=data[row].strip().split("\t")
        out[temp[1]].write(data[row])

for me in ME_repeats:
	out[me].close()	

print "%s_*blast.filter are generated"%read1

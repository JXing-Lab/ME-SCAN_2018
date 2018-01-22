#!/usr/bin/python

import subprocess as sp, argparse

parser=argparse.ArgumentParser()
parser.add_argument('--mei',nargs='*')
parser.add_argument('--r1',nargs='*')
parser.add_argument('--r2',nargs='*')
parser.add_argument('--me_repeats',nargs='*')
parser.add_argument('--path',nargs='*')

args=parser.parse_args()
MEI=''.join(args.mei)
read1=''.join(args.r1)
read2=''.join(args.r2)
ME_repeats=list(args.me_repeats)
file_path=''.join(args.path)

f_path=open(file_path,'r')

for row_path in f_path.readlines():
        columns_path = row_path.split('=')
	if columns_path[0] == "path_samtools":
                path_samtools = columns_path[1]
                path_samtools = path_samtools.rstrip('\n')

headers = sp.Popen("cat "+read2+"_BB.sam |grep '@SQ' > "+read2+"_temp_header",shell=True)
headers.wait()

for me in ME_repeats:
        p1 = sp.Popen("awk 'FNR==NR{a[$1]=$0;next}{if(b=a[$1]){print b}}' "+read2+"_BB.sam "+read1+"_"+me+"_blast.filter > "+read2+"_"+me+"_BB_no_header.sam",shell=True).wait()
        p2 = sp.Popen("cat "+read2+"_temp_header "+read2+"_"+me+"_BB_no_header.sam > "+read2+"_"+me+"_BB.sam",shell=True).wait()
	p3 = sp.Popen(path_samtools+"samtools view -bS "+read2+"_"+me+"_BB.sam > "+read2+"_"+me+"_BB.bam",shell=True).wait()
	p4 = sp.Popen(path_samtools+"samtools sort "+read2+"_"+me+"_BB.bam "+read2+"_"+me+"_BB_sorted",shell=True).wait()
	p5 = sp.Popen(path_samtools+"samtools index "+read2+"_"+me+"_BB_sorted.bam",shell=True).wait() 
	p6 = sp.Popen(path_samtools+"samtools idxstats "+read2+"_"+me+"_BB_sorted.bam",shell=True).wait()
	print "\n\n-------%s_%s_BB_sorted.bam is completed -------\n"%(read2,me) 
	
	p9 = sp.Popen("rm "+read2+"_%s_BB.sam"%me,shell=True)
	p10 = sp.Popen("rm "+read2+"_%s_BB.bam"%me,shell=True)

p7 = sp.Popen("rm "+read2+"_temp_header",shell=True)
p8 = sp.Popen("rm "+read2+"*BB_no_header.sam",shell=True)

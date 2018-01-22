#!/usr/bin/python

import subprocess as sp, argparse

parser=argparse.ArgumentParser()
parser.add_argument('--mei',nargs='*')
parser.add_argument('--option_tag',nargs='*')
parser.add_argument('--path',nargs='*')

args=parser.parse_args()
insertME=''.join(args.mei)
option_tag=''.join(args.option_tag)
path_current=''.join(args.path)


fh = open(path_current+"Results%s/fixed_insertion/fixed_insertion_candidates.bed"%option_tag,"r")
candidates = fh.readlines()
fh.close()

d_m = {}	#locusID as key, {ind:[#raw_read,#uniq_read]} as value
d_p = {}
for row in candidates:
	row=row.strip().split("\t")
	if row[5] == "+":
		d_p[row[3]]={}
	else:
		d_m[row[3]]={}

d_lib_r = {}	#ind as key, mapped_read as value
#to retrive the number of mapped read for the library used

is0 = sp.Popen(['ls',path_current],stdout = sp.PIPE)
is1 = sp.Popen(['grep','Sample'],stdin = is0.stdout, stdout = sp.PIPE)
i = sp.Popen(['awk','-F',r"_",r'{print $2}'],stdin = is1.stdout, stdout = sp.PIPE).communicate()[0].strip().split("\n")

#print i, len(i)
for s in i:
        qi = sp.Popen("ls "+path_current+"Sample_"+s+"/|grep -E '%s.*sorted.bam$'"%insertME,shell=True,stdout = sp.PIPE).communicate()[0].strip()
        bam_file = ""
        if len(qi) == 0:
                bam_file = sp.Popen("ls "+path_current+"Sample_"+s+"/|grep sorted.bam$",shell=True,stdout = sp.PIPE).communicate()[0].strip()
        else:
                bam_file = qi
#	print bam_file
	q1 = sp.Popen(['samtools','idxstats','%sSample_%s/%s'%(path_current,s,bam_file)],stdout = sp.PIPE)
	q2 = sp.Popen(['awk',r'{sum+=$3;} END {print sum;}'],stdin=q1.stdout,stdout=sp.PIPE)
	mapped_read = float(q2.communicate()[0].strip().split("\n")[0])
#	print "mapped read is %s"%mapped_read
	d_lib_r[s]=mapped_read
#print d_lib_r

for k in range(0,2,1):
	if k == 0 :
		orient = "minus"
		d = d_m
	else:
		orient = "plus"
		d = d_p
#	print orient
	fk = open("%soutput_bwa-blast%s/%s_all.insert_%s%stemp"%(path_current,option_tag,insertME,orient,option_tag),"r")
	data = fk.readlines()
	fk.close()

	for row in data:
		row=row.strip().split(" ")
		if row[5] in d.keys():
			if row[4] not in d[row[5]].keys():
				d[row[5]][row[4]] = [int(row[3]),1]
			else:
				d[row[5]][row[4]][0] += int(row[3])
				d[row[5]][row[4]][1] += 1

	out = open(path_current+"Results%s/fixed_insertion/Fixed_insertion_%s.%s%sBB.bed"%(option_tag,orient,insertME,option_tag),"w")		
	
	fz = open("%soutput_bwa-blast%s/%s_all%sBB.bed"%(path_current,option_tag,insertME,option_tag),"r")
	template = fz.readlines()
	fz.close()

	for row in template:
		row=row.strip().split("\t")
		if row[6] in d.keys():
			ind_list = []
			TPM_list = []
			UR_list = []
			flag = False
			for ind in d[row[6]].keys():
				if ind in i:
					flag = True
					ind_list.append(ind)
					temp_TPM = (d[row[6]][ind][0]*1000000.0)/d_lib_r[ind]
					TPM_list.append("%s"%float("%.6g"%temp_TPM))
					UR_list.append(str(d[row[6]][ind][1]))
			if flag:
				out.write(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+row[3]+"\t"+row[4]+"\t"+",".join(ind_list)+"\t"+row[6]+"\t"+",".join(ind_list)+"\t"+",".join(TPM_list)+"\t"+",".join(UR_list)+"\n")
out.close()
				

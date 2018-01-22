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

sensi_cutoff = input("Please enter the cutoff for sensitivity analysis (in term of percent): ")
fh = open(path_current+"Results%s/%s%sTPM_stats_%s_maxUR_10.txt"%(option_tag,insertME,option_tag,sensi_cutoff),"r")
ref = fh.readlines()[1:]
fh.close()
ind_TPM_UR = {}		#ind as key, (TPM,UR) as value
ind_loci = {}		#ind as key, {"Polymorphic":#,"Novel_polymorphic":#}
for row in ref:
	row=row.strip().split("\t")
	ind_TPM_UR[row[0]] = (float(row[2]),int(row[1]))
	ind_loci[row[0]] = {"Polymorphic":0,"Novel_polymorphic":0}
#print ind_loci

insert = ["Polymorphic","Novel_polymorphic"]
for fa in insert:
#	print fa	
	out_count = open(path_current+"output_bwa-blast%s/latest_data_TPM-10UR_filters_%s_insertion_ind_count_loci_%s%stxt"%(option_tag,fa,insertME,option_tag),"w")
	
	orient = ""
	for k in range(0,2,1):
		if k == 0:
			orient = "minus"
		else:
			orient = "plus"

		fk = open(path_current+"output_bwa-blast%s/%s_insertion_%s.%s%sBB.bed"%(option_tag,fa,orient,insertME,option_tag),"r")
		data = fk.readlines()
		fk.close()

		out = open(path_current+"output_bwa-blast%s/latest_data_TPM-10UR_filters_%s_insertion_%s_%s%sbed"%(option_tag,fa,orient,insertME,option_tag),"w")

		for row in data:
			row=row.strip().split("\t")
			ind_list = row[7].split(",")
			TPM_list = row[8].split(",")
			UR_list = row[9].split(",")
			temp_ind = []
			temp_TPM = []
			temp_UR = []
			for x in range(0,len(ind_list),1):
				if ind_list[x] in ind_TPM_UR.keys():
					if float(TPM_list[x]) > ind_TPM_UR[ind_list[x]][0] and int(UR_list[x]) > ind_TPM_UR[ind_list[x]][1]:
						temp_ind.append(ind_list[x])
						temp_TPM.append(TPM_list[x])
						temp_UR.append(UR_list[x])
						ind_loci[ind_list[x]][fa] += 1
			if len(temp_ind) > 0:
				out.write(row[0]+"\t"+row[1]+"\t"+row[2]+"\t"+row[3]+"\t"+row[4]+"\t"+row[5]+"\t"+row[6]+"\t"+",".join(temp_ind)+"\t"+",".join(temp_TPM)+"\t"+",".join(temp_UR)+"\n")
		out.close()

	for ind in ind_loci.keys():
		out_count.write(ind+"\t"+str(ind_loci[ind][fa])+"\n")
	out_count.close()

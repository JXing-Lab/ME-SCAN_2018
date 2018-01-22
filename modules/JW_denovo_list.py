#!/usr/bin/python

import subprocess as sp, argparse

parser=argparse.ArgumentParser()
parser.add_argument('--mei',nargs='*')
parser.add_argument('--option_tag',nargs='*')
parser.add_argument('--path',nargs='*')

args=parser.parse_args()
MEI=''.join(args.mei)
option_tag=''.join(args.option_tag)
path_current=''.join(args.path)

ln0 = sp.Popen(['ls',path_current],stdout = sp.PIPE)
lib_name = sp.Popen(['grep','library'],stdin = ln0.stdout, stdout = sp.PIPE).communicate()[0].strip()
#To get familyID and the relationship of each ind"
fk = open(path_current+lib_name,"r")
info = fk.readlines()
fk.close()
d_trio_info = {}        # family id as key, [(ind,relationship)] as value
child_list = {}		#ind (child) as key, (familyId,relationship) as value
for row in info:
        row=row.strip().split("\t")
	if row[3] == "1459" or row[3] == "1463":
		if row[4] == "father" or row[4] == "mother":
			child_list[row[1]] = (row[3],row[4])
	else:
		if row[4] == "child":
			child_list[row[1]] = (row[3],row[4])
        if row[3] not in d_trio_info.keys():
                d_trio_info[row[3]]=[(row[1],row[4])]
        else:
                d_trio_info[row[3]].append((row[1],row[4]))
#print d_trio_info

#to get the list of inds that are found both in the lib_file and in working directory
is0 = sp.Popen(['ls',path_current],stdout = sp.PIPE)
is1 = sp.Popen(['grep','Sample'],stdin = is0.stdout, stdout = sp.PIPE)
ind_sample = sp.Popen(['awk','-F',r"_",r'{print $2}'],stdin = is1.stdout, stdout = sp.PIPE).communicate()[0].strip().split("\n")
for fam in d_trio_info.keys():
        indID = 0
        while (indID < len(d_trio_info[fam])):
                if d_trio_info[fam][indID][0] in ind_sample:
                        pass
                else:
                        d_trio_info[fam].pop(indID)
                        indID -= 1
                indID += 1
        if len(d_trio_info[fam]) == 0:
                d_trio_info.pop(fam,None)
for childID in child_list.keys():
	if childID not in ind_sample:
		child_list.pop(childID,None)

sensi_cutoff = input("Please enter the cutoff for sensitivity analysis (in term of percent): ")
fl = open(path_current+"Results%s/%s%sTPM_stats_%s_maxUR_10.txt"%(option_tag,MEI,option_tag,sensi_cutoff),"r")
cutoff = fl.readlines()[1:]
fl.close()
TPM_UR = {}	#ind as key, (TPM,UR,sensitivity used as cutoff) as value
for row in cutoff:
	row=row.strip().split("\t")
	TPM_UR[row[0]] = (row[2],row[1],row[3])
#print TPM_UR

out = open(path_current+"output_bwa-blast%s/denovo_from_novel_polymorphic%sbed"%(option_tag,option_tag),"w")
for k in range(0,2,1):
	if k == 0:
		orient = "minus"
	else:
		orient = "plus"
	fh = open(path_current+"output_bwa-blast%s/latest_data_TPM-10UR_filters_Novel_polymorphic_insertion_%s_%s%sbed"%(option_tag,orient,MEI,option_tag),"r")
	data = fh.readlines()
	fh.close()

	for row in data:
		row=row.strip().split("\t")
		ind_list = row[5].split(",")
		if len(ind_list) == 1 and ind_list[0] in child_list:
			out.write("\t".join(row)+"\t"+ind_list[0]+"\t"+child_list[ind_list[0]][1]+"\t"+",".join(TPM_UR[ind_list[0]]))

			if child_list[ind_list[0]][0] == "1459":
				key = ""
				if child_list[ind_list[0]][1][0] == "f":
					key = "pa"
				elif child_list[ind_list[0]][1][0] == "m":
					key = "ma"
				for member in d_trio_info[child_list[ind_list[0]][0]]:
					if member[1][0:2] == key:
						out.write("\t"+member[0]+"\t"+member[1]+"\t"+",".join(TPM_UR[member[0]]))
				out.write("\n")
			else:
				for member in d_trio_info[child_list[ind_list[0]][0]]:
					if member[1] != child_list[ind_list[0]][1]:
						out.write("\t"+member[0]+"\t"+member[1]+"\t"+",".join(TPM_UR[member[0]]))
				out.write("\n")
out.close()

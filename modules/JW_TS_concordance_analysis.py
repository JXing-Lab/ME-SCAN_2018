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

def summing (output,key,all_list):
	if key not in output.keys():
		output[key] = all_list
	else:
		for counter in range(0,len(all_list),1):
			output[key][counter] += all_list[counter]

first_part = ["21","22","23"]
second_part = ["cell","iPSC","neurons","NSC"]

insert = ["Polymorphic","Novel_polymorphic"]
for fa in insert:
	print fa
        out = open(path_current+"Results%s/%s%s%s_concordance_analysis_across_cell_types.txt"%(option_tag,MEI,option_tag,fa),"w")
        out.write("individual\tcommon_among_all_cell_types\tcell_iPSC_neu\tiPSC_neu_NSC\tcell_neu_NSC\tcell_iPSC_NSC\tcell_iPSC\tcell_neu\tcell_NSC\tiPSC_neu\tiPSC_NSC\tneu_NSC\tuniq_cell\tuniq_iPSC\tuniq_neu\tuniq_NSC\ttotal_cell_insertion\ttotal_iPSC_insertion\ttotal_neu_insertion\ttotal_NSC_insertion\n")
	output = {}	#first_part as key, [all the length of different types of intersection] as value
	for k in range(0,2,1):
		if k == 0:
			type = "minus"
		else:
			type = "plus"
		print type

		fh = open(path_current+"output_bwa-blast%s/latest_data_TPM-10UR_filters_%s_insertion_%s_%s%sbed"%(option_tag,fa,type,MEI,option_tag),"r")
		data = fh.readlines()
		fh.close()

		d_aftTPM = {}	# ind as key, [insertion pos] as value
		for row in data:
			row=row.strip().split("\t")
			ind_list = row[7].split(",")
			for ind in ind_list:
				if ind not in d_aftTPM.keys():
					d_aftTPM[ind] = [row[0]+":"+row[1]]
				else:
					d_aftTPM[ind].append(row[0]+":"+row[1])

		for x in first_part:
			ID = [x+"-"+y for y in second_part]
			for types in ID:
				if types not in d_aftTPM.keys():
					d_aftTPM[types] = []
			cell = ID[0]
			common_4 = d_aftTPM[cell]
			cell_neu_NSC = d_aftTPM[cell]
			cell_iPSC_neu = d_aftTPM[cell]
			cell_iPSC_NSC = d_aftTPM[cell]
			cell_iPSC = d_aftTPM[cell]
			cell_neu = d_aftTPM[cell]
			cell_NSC = d_aftTPM[cell]
			for num in range(1,len(ID),1):
				common_4 = list(set(d_aftTPM[ID[num]])&set(common_4))
				if num > 1:
					cell_neu_NSC = list(set(d_aftTPM[ID[num]])&set(cell_neu_NSC))
				if num < 3:
					cell_iPSC_neu = list(set(d_aftTPM[ID[num]])&set(cell_iPSC_neu))
				if num == 1 or num == 3:
					cell_iPSC_NSC = list(set(d_aftTPM[ID[num]])&set(cell_iPSC_NSC))
				if num == 1:
					cell_iPSC = list(set(d_aftTPM[ID[num]])&set(cell_iPSC))
				if num == 2:
					cell_neu = list(set(d_aftTPM[ID[num]])&set(cell_neu))
				if num == 3:
					cell_NSC = list(set(d_aftTPM[ID[num]])&set(cell_NSC))
			only_cell_neu_NSC = list(set(cell_neu_NSC)-set(common_4))
			only_cell_iPSC_neu = list(set(cell_iPSC_neu)-set(common_4))
			only_cell_iPSC_NSC = list(set(cell_iPSC_NSC)-set(common_4))
			only_cell_iPSC = list(set(cell_iPSC)-set(common_4)-set(cell_iPSC_neu)-set(cell_iPSC_NSC))
			only_cell_neu = list(set(cell_neu)-set(common_4)-set(cell_neu_NSC)-set(cell_iPSC_neu))
			only_cell_NSC = list(set(cell_NSC)-set(common_4)-set(cell_neu_NSC)-set(cell_iPSC_NSC))


			iPSC = ID[1]
			iPSC_neu_NSC = d_aftTPM[iPSC]
			iPSC_neu = d_aftTPM[iPSC]
			iPSC_NSC = d_aftTPM[iPSC]
			for num in range(2,len(ID),1):
				iPSC_neu_NSC = list(set(d_aftTPM[ID[num]])&set(iPSC_neu_NSC))
				if num == 2:
					iPSC_neu = list(set(d_aftTPM[ID[num]])&set(iPSC_neu))
				if num == 3:
					iPSC_NSC = list(set(d_aftTPM[ID[num]])&set(iPSC_NSC))
			only_iPSC_neu_NSC = list(set(iPSC_neu_NSC)-set(common_4))
			only_iPSC_neu = list(set(iPSC_neu)-set(common_4)-set(cell_iPSC_neu)-set(iPSC_neu_NSC))
			only_iPSC_NSC = list(set(iPSC_NSC)-set(common_4)-set(cell_iPSC_NSC)-set(iPSC_neu_NSC))


			neu = ID[2]
			neu_NSC = list(set(d_aftTPM[neu])&set(d_aftTPM[ID[3]]))
			only_neu_NSC = list(set(neu_NSC)-set(common_4)-set(cell_neu_NSC)-set(iPSC_neu_NSC))
			uniq_cell = list(set(d_aftTPM[cell])-set(cell_iPSC)-set(cell_neu)-set(cell_NSC))
			uniq_iPSC = list(set(d_aftTPM[iPSC])-set(cell_iPSC)-set(iPSC_neu)-set(iPSC_NSC))
			uniq_neu = list(set(d_aftTPM[neu])-set(cell_neu)-set(iPSC_neu)-set(neu_NSC))
			uniq_NSC = list(set(d_aftTPM[ID[3]])-set(cell_NSC)-set(iPSC_NSC)-set(neu_NSC))

			print x, uniq_neu

			all_list = [len(common_4),len(only_cell_iPSC_neu),len(only_iPSC_neu_NSC),len(only_cell_neu_NSC),len(only_cell_iPSC_NSC),len(only_cell_iPSC),len(only_cell_neu),len(only_cell_NSC),len(only_iPSC_neu),len(only_iPSC_NSC),len(only_neu_NSC),len(uniq_cell),len(uniq_iPSC),len(uniq_neu),len(uniq_NSC),len(d_aftTPM[cell]),len(d_aftTPM[iPSC]),len(d_aftTPM[neu]),len(d_aftTPM[ID[3]])]
		
			summing(output,x,all_list)
	
	for sample in output.keys():
		output[sample] = map(str,output[sample])
		out.write(sample+"\t"+"\t".join(output[sample])+"\n")
out.close()

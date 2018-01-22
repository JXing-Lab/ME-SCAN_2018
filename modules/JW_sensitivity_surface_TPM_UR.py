#!/usr/bin/python

import subprocess as sp,argparse

parser=argparse.ArgumentParser()
parser.add_argument('--mei',nargs='*')
parser.add_argument('--option_tag',nargs='*')
parser.add_argument('--path',nargs='*')

args=parser.parse_args()
insertME=''.join(args.mei)
option_tag=''.join(args.option_tag)
path_current=''.join(args.path)

is0 = sp.Popen(['ls',path_current],stdout = sp.PIPE)
is1 = sp.Popen(['grep','Sample'],stdin = is0.stdout, stdout = sp.PIPE)
i = sp.Popen(['awk','-F',r"_",r'{print $2}'],stdin = is1.stdout, stdout = sp.PIPE).communicate()[0].strip().split("\n")
#print i, len(i)

filterTPM = [x for x in range(30)]
filterUR = [x for x in range(30)]
str_filterUR = map(str,filterUR)

out = open(path_current+"Results%s/sensitivity_stuff/overall_temp_sensitivity_analysis_with_variableTPM_and_UR.txt"%option_tag,"w")
out.write("TPM\UR\t"+"\t".join(str_filterUR)+"\n")
out_avg = open(path_current+"Results%s/sensitivity_stuff/average_temp_sensitivity_analysis_with_variableTPM_and_UR.txt"%option_tag,"w")
out_avg.write("TPM\UR\t"+"\t".join(str_filterUR)+"\n")

out_file = {}
for ind in i:
	out_file[ind] = open(path_current+"Results%s/sensitivity_stuff/%s_temp_sensitivity_analysis_with_variableTPM_and_UR.txt"%(option_tag,ind),"w")
	out_file[ind].write("TPM\UR\t"+"\t".join(str_filterUR)+"\n")

l1 = sp.Popen(['wc','-l','%sref_mescan_customized%s/Fixed_Reference.%s%sbed'%(path_current,option_tag,insertME,option_tag)],stdout=sp.PIPE)
total_insert = int(l1.communicate()[0].strip().split(" ")[0])
#print total_insert
for f_TPM in filterTPM:
	across_UR = []
	across_UR_avg = []
	across_UR_ind = {}
	for ind in i:
		across_UR_ind[ind] = []
	for f_UR in filterUR:
#		print f_TPM, f_UR
		overall_insert = 0
		d_aftTPM = {}		# ind as key, [insertion pos] as value
		for ind in i:
			d_aftTPM[ind] = []
#		print d_aftTPM
		
		for k in range(0,2,1):
			if k==0:
				type = "minus"
			else:
				type = "plus"
#			print type

			fh = open(path_current+"Results%s/fixed_insertion/Fixed_insertion_%s.%s%sBB.bed"%(option_tag,type,insertME,option_tag),"r")
			data = fh.readlines()
			fh.close()
			
			for row in data:
				row = row.strip().split("\t")
				ind_list = row[7].split(",")
				TPM_list = row[8].split(",")
				UR_list = row[9].split(",")
				flag = False
				for y in range(0,len(ind_list),1):
					if float(TPM_list[y]) > f_TPM and int(UR_list[y]) > f_UR:
						d_aftTPM[ind_list[y]].append(row[0]+":"+row[1])
						flag = True
				if flag:
					overall_insert+=1

		passed = 0
		for each in d_aftTPM.keys():
			across_UR_ind[each].append("%s"%str("%.1f"%(len(d_aftTPM[each])*100.0/total_insert)))
			passed += len(d_aftTPM[each])
#		print total_insert,overall_insert,passed
		across_UR.append("%s"%str("%.1f"%(overall_insert*100.0/total_insert)))
		across_UR_avg.append("%s"%str("%.1f"%(passed*100.0/(total_insert*len(i)))))

	for ind in i:
		out_file[ind].write(str(f_TPM)+"\t"+"\t".join(across_UR_ind[ind])+"\n")
#		out.write(str(f_TPM)+"\t"+str(f_UR)+"\t"+str(passed)+"\t"+str(total_insert)+"\t%.1f\n"%(passed*100.0/total_insert))
	out.write(str(f_TPM)+"\t"+"\t".join(across_UR)+"\n")
	out_avg.write(str(f_TPM)+"\t"+"\t".join(across_UR_avg)+"\n")
for ind in i:
	out_file[ind].close()
out.close()
out_avg.close()

s1 = sp.Popen(['ls',path_current+"Results%s/sensitivity_stuff/"%option_tag],stdout=sp.PIPE)
s2 = sp.Popen(['grep','temp_sensitivity'],stdin = s1.stdout, stdout = sp.PIPE)
input_files = s2.communicate()[0].strip().split("\n")
#print input_files,len(input_files)

new_files = {}
last_UR = filterUR[-1]
last_TPM = filterTPM[-1]
for fi in input_files:
#	print fi
	fa = open(path_current+"Results%s/sensitivity_stuff/"%(option_tag)+fi,"r")
	data = fa.readlines()[1:]
	fa.close()

	new_files[fi.split("_")[0]] = {}

	flag_last_TPM = False
	for row in range(0,len(data),1):
		col=data[row].strip().split("\t")
		new_files[fi.split("_")[0]][row] = []
		for x in range(1,len(col),1):
			if x == 1 and float(col[x]) < 80 and row-1 < last_TPM:
				last_TPM = row-1
				flag_last_TPM = True
				new_files[fi.split("_")[0]].pop(row)
				break
			if float(col[x]) < 80 and x-2 < last_UR:
				last_UR = x-2
				if last_UR < 10:
					last_UR = 10
			if float(col[x]) < 80 and x-1 > last_UR:
				break
			new_files[fi.split("_")[0]][row].append(col[x])
		if flag_last_TPM:
			break

#print last_TPM,last_UR

for ind in new_files.keys():
#	print ind
	out_new = open(path_current+"Results%s/sensitivity_stuff/"%(option_tag)+ind+"_80%_sensitivity_analysis_with_variableTPM_and_UR.txt","w")
	out_new.write("TPM\UR\t")
	for num in range(0,last_UR,1):
		out_new.write(str(num)+"\t")
	out_new.write("%i\n"%last_UR)

	for tpm in new_files[ind].keys():
		if tpm <= last_TPM:
			out_new.write("%i\t"%tpm)
			for ur in range(0,last_UR,1):
				out_new.write(new_files[ind][tpm][ur]+"\t")
			out_new.write(new_files[ind][tpm][last_UR]+"\n")
	out_new.close()
	r1 = sp.Popen(['rm',path_current+"Results%s/sensitivity_stuff/"%(option_tag)+ind+"_temp_sensitivity_analysis_with_variableTPM_and_UR.txt"],stdout=sp.PIPE)

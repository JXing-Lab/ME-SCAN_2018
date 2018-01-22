#!/usr/bin/python

import matplotlib.pyplot as plt, numpy as np, subprocess as sp, argparse, math

parser=argparse.ArgumentParser()
parser.add_argument('--mei',nargs='*')
parser.add_argument('--option_tag',nargs='*')
parser.add_argument('--path',nargs='*')

args=parser.parse_args()
MEI=''.join(args.mei)
option_tag=''.join(args.option_tag)
path_current=''.join(args.path)


folder = path_current+"Results%s/sensitivity_stuff/"%option_tag
p1 = sp.Popen(['ls','%s'%folder],stdout=sp.PIPE)
input_files = p1.communicate()[0].strip().split("\n")
#print input_files

max_UR = 10
sensi_cutoff = input("Please enter the cutoff for sensitivity analysis (in term of percent): ")
out = open(folder.split("sensitivity_stuff")[0]+MEI+option_tag+"TPM_stats_%s_maxUR_%i.txt"%(sensi_cutoff,max_UR),"w")
out.write("individual_ID\tUR\tTPM\t%_sensitivity\n")

TPM_UR = {}
small = 100.0
ind_list_check = []
for x in range(0,len(input_files),1):
	target_UR = 0
	flag_UR = False
	flag_TPM = False
#	print input_files[x]
	ind = input_files[x].split("_")[0]
	ind_list_check.append(ind)
	fh = open(folder+input_files[x],"r")
	data = fh.readlines()
	fh.close()

	UR_list = data[0].strip().split("\t")
	del UR_list[0]
	del data[0]
	TPM_UR[ind] = np.random.rand(len(data),len(UR_list))
	for row in range(0,len(data),1):
		data[row]=data[row].strip().split("\t")
		del data[row][0]
		for col in range(0,len(data[row]),1):
			TPM_UR[ind][row,col]=data[row][col]
			if float(data[row][col]) < small:
				small = float(data[row][col])
			if ind != "overall" and ind != "average":
				if not flag_UR and col < max_UR+1 and float(data[row][col]) < int(sensi_cutoff):
					flag_UR = True
					if col != max_UR and row > 0:
						target_UR = max_UR-1
					else:
						target_UR = col-1
		if ind != "overall" and ind != "average" and row == 9 and not flag_TPM and float(data[row][target_UR]) >= int(sensi_cutoff): 
			flag_TPM = True
			if not flag_UR:
				target_UR = 9
			out.write(ind+"\t%i\t%i\t%s\n"%(target_UR+1,row+1,data[row][target_UR]))

		if ind != "overall" and ind != "average" and not flag_TPM and flag_UR and float(data[row][target_UR]) < int(sensi_cutoff):
			flag_TPM = True
			out.write(ind+"\t%i\t%i\t%s\n"%(target_UR+1,row,data[row-1][target_UR]))
out.close()

c1 = sp.Popen(['cat',folder.split("sensitivity_stuff")[0]+MEI+option_tag+"TPM_stats_%s_maxUR_%i.txt"%(sensi_cutoff,max_UR)],stdout=sp.PIPE)
ind_have_cutoff = sp.Popen(['awk',r'NR>1{print $1}'],stdin=c1.stdout,stdout=sp.PIPE).communicate()[0].strip().split("\n")
ind_no_cutoff = list(set(ind_list_check)-set(ind_have_cutoff))
if len(ind_no_cutoff) > 2:
	print ind_no_cutoff
	print "Above individual(s) have no TPM_UR cutoff. Please look at the %s"%(folder.split("sensitivity_stuff")[0]+MEI+option_tag+"TPM_stats_%s_maxUR_%i.txt"%(sensi_cutoff,max_UR))


#print small

sorted_ID = sorted(TPM_UR.keys())
avg_ov = sorted_ID[-2:]
del sorted_ID[-2:]

flag_som = False
if len(sorted_ID) == 12:
	sorted_ID = ["21-cell","21-iPSC","21-NSC","21-neurons","22-cell","22-iPSC","22-NSC","22-neurons","23-cell","23-iPSC","23-NSC","23-neurons"]	#for 12 analysis somatic cells
	flag_som = True

two_heatmap = [sorted_ID,avg_ov]
for loop in range(0,len(two_heatmap),1):
	count = 0
	fig = plt.figure()
	for each in two_heatmap[loop]:
		count += 1
		if loop == 0:
			ax1 = fig.add_subplot(int(math.ceil(len(sorted_ID)/4.0)),4,count)
			size = ['%.1f',1.00]
		else:
			ax1 = fig.add_subplot(4,2,count)
			size = ['%.0f',1.02]
		heatmap = plt.pcolor(TPM_UR[each],vmin=int(small),vmax=100)
		for y in range(TPM_UR[each].shape[0]):
		    for x in range(TPM_UR[each].shape[1]):
		        plt.text(x + 0.5, y + 0.5, size[0] % TPM_UR[each][y,x],
		                 horizontalalignment='center',
		                 verticalalignment='center',
		                 )
		plt.colorbar(heatmap)
		plt.xlim(0,TPM_UR[each].shape[1])
		plt.ylim(0,TPM_UR[each].shape[0])
		ax1.set_title('%s'%each,fontsize=45,y=size[1])
		ax1.set_ylabel('TPM',fontsize = 30)
		ax1.set_xlabel('UR',fontsize = 30)
	
	if loop == 0:
		name = "individual"
		fig.set_size_inches(75, 105)	
		if flag_som:
			fig.set_size_inches(100, 45)	#for 12 analysis somatic cells
	else:
		name = "average_overall"
		fig.set_size_inches(30, 30)
	fig.savefig(folder.split("sensitivity_stuff")[0]+MEI+option_tag+'heatmap_sensitivity_%s_analysis.pdf'%(name))
	plt.close(fig)
	

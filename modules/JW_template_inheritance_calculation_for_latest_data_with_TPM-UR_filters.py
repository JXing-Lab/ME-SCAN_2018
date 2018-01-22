#!/usr/bin/python

import numpy as np, matplotlib.pyplot as plt, subprocess as sp, argparse

parser=argparse.ArgumentParser()
parser.add_argument('--mei',nargs='*')
parser.add_argument('--option_tag',nargs='*')
parser.add_argument('--path',nargs='*')

args=parser.parse_args()
MEI=''.join(args.mei)
option_tag=''.join(args.option_tag)
path_current=''.join(args.path)

def add_in_dict(output,each,relation,length,num):
	if (each,relation) not in output.keys():
		output[(each,relation)] = [num,length]
	else:
		output[(each,relation)][0] += num	#num is count of inheritance from each parent
		output[(each,relation)][1] += length	#length is the total number of insertion in that individual

def inheritance(parent_list,child_list,rel,each,output):
        for x in range(0,len(parent_list),1):
                inherit_from_parent = list(set(parent_list[x])&set(child_list))
                relation=""
                if x == 0:
                        relation = rel+"father"
                else:
                        relation = rel+"mother"
                add_in_dict(output,each,relation,len(parent_list[x]),len(inherit_from_parent))
        none = list(set(child_list)-set(parent_list[0])-set(parent_list[1]))
        add_in_dict(output,each,rel+"none",len(child_list),len(none))

def add_in_final (dict,key,value):
	if key not in dict.keys():
		dict[key] = value
	else:
		dict[key].extend(value)

ln0 = sp.Popen(['ls',path_current],stdout = sp.PIPE)
lib_name = sp.Popen(['grep','library'],stdin = ln0.stdout, stdout = sp.PIPE).communicate()[0].strip()
#To get familyID and the relationship of each ind"
fk = open(path_current+lib_name,"r")
info = fk.readlines()
fk.close()
d_trio_info = {}	# family id as key, [(ind,relationship)] as value
#count_ind = 0
for row in info:
	row=row.strip().split("\t")
	if row[3] not in d_trio_info.keys():
		d_trio_info[row[3]]=[(row[1],row[4])]
	else:
		d_trio_info[row[3]].append((row[1],row[4]))
#	count_ind += 1
#print d_trio_info

#to get the list of inds that are found both in the lib_file and in working directory
is0 = sp.Popen(['ls',path_current],stdout = sp.PIPE)
is1 = sp.Popen(['grep','Sample'],stdin = is0.stdout, stdout = sp.PIPE)
ind_sample = sp.Popen(['awk','-F',r"_",r'{print $2}'],stdin = is1.stdout, stdout = sp.PIPE).communicate()[0].strip().split("\n")
count_ind = 0
for fam in d_trio_info.keys():
	indID = 0
	while (indID < len(d_trio_info[fam])):
		if d_trio_info[fam][indID][0] in ind_sample:
			count_ind += 1
		else:
			d_trio_info[fam].pop(indID)
			indID -= 1
		indID += 1
	if len(d_trio_info[fam]) == 0:
		d_trio_info.pop(fam,None)

insert = ["Polymorphic","Novel_polymorphic"]
d_insert = {"Polymorphic":[0 for x in range(count_ind/3*2)],"Novel_polymorphic":[0 for x in range(count_ind/3*2)]}    #count of loci vs count of ind for unrelated ind
d_insert_all = {"Polymorphic":[0 for x in range(count_ind)],"Novel_polymorphic":[0 for x in range(count_ind)]}		#count of loci vs count of ind for all ind
total_insert = {"Polymorphic":0,"Novel_polymorphic":0}
total_insert_all = {"Polymorphic":0,"Novel_polymorphic":0}
for fa in insert:
#	print fa
        out_pos = open(path_current+"Results%s/%s%s%s_insertion_trio_inheritance.txt"%(option_tag,MEI,option_tag,fa),"w")
        out_pos.write("ped_id\tinsertion_found_in\t%_inherit_from_\ttotal_num_insertion\n")
	final_output = {}        #(familyID,relation) as key,[%_of_inheritance_rate,total_num_insertion_of_that_ind,...] as value
	output = {}     #(familyID,relation) as key, [number_of_inheritance,total_num_insertion_of_that_ind] as value

	out_denovo = open(path_current+"Results%s/%s%s%s_inheritance_calculation_error_rate.txt"%(option_tag,MEI,option_tag,fa),"w")  # only for child
	out_denovo.write("ped_id\tinsertion_found_in\t%_error_inheritance\ttotal_num_insertion\n")
	final_denovo_output = {}	#(familyID,child) as key,[%_of_inheritance_error_rate,total_num_insertion_of_child,...] as value
	denovo_output = {}	#(familyID,child) as key, [number_of_uniq_pos,number_of_child_insertion] as value
	for k in range(0,2,1):
		if k==0:
			type = "minus"
		else:
			type = "plus"
#		print type
		
		d_aftTPM = {}		# ind as key, [insertion pos] as value
		for row in info:
			row=row.strip().split("\t")
			d_aftTPM[row[1]] = []
	
		fh = open(path_current+"output_bwa-blast%s/latest_data_TPM-10UR_filters_%s_insertion_%s_%s%sbed"%(option_tag,fa,type,MEI,option_tag),"r")
		data = fh.readlines()
		fh.close()
		for row in data:
			row = row.strip().split("\t")
			ind_list = row[7].split(",")
			for y in range(0,len(ind_list),1):
				d_aftTPM[ind_list[y]].append(row[0]+":"+row[1])

		#generating inheritance error rate 
		child_list = []
		for familyID in d_trio_info.keys():
			if familyID == "1459" or familyID == "1463":
				for member in d_trio_info[familyID]:
					if member[1] == "father" or member[1] == "mother":
						child_list.append((member[0],member[1],familyID))
			else:
				for member in d_trio_info[familyID]:
					if member[1] == "child":
						child_list.append((member[0],member[1],familyID))

		for child in child_list:
			uniq_to_child = d_aftTPM[child[0]][:]
			for ind in d_aftTPM.keys():
				if child[0] == ind:
					continue
				else:
					overlap = list(set(d_aftTPM[child[0]])&set(d_aftTPM[ind]))
					uniq_to_child = list(set(uniq_to_child)-set(overlap))
			add_in_dict(denovo_output,child[2],child[1],len(d_aftTPM[child[0]]),len(uniq_to_child))

		#generating plot of histogram (allele frequency)
		child_temp = []
		for each in child_list:
			child_temp.append(each[0])
		parent_list = list(set(d_aftTPM.keys())-set(child_temp))
		#doing count of loci vs individual count for unrelated ind
		d_temp_count = {}
		for each_ind in parent_list:
		        for each_pos in d_aftTPM[each_ind]:
		                if each_pos not in d_temp_count.keys():
        		                d_temp_count[each_pos] = 1
        		        else:
                		        d_temp_count[each_pos]+=1
		total_insert[fa] += len(d_temp_count)
		for key in d_temp_count.keys():
		        d_insert[fa][d_temp_count[key]-1] += 1

		#doing count of loci vs individual count for all individuals
		d_temp_count_all = {}
		for each_ind in d_aftTPM.keys():
			for each_pos in d_aftTPM[each_ind]:
				if each_pos not in d_temp_count_all.keys():
					d_temp_count_all[each_pos] = 1
				else:
					d_temp_count_all[each_pos] += 1
		total_insert_all[fa] += len(d_temp_count_all)
		for key in d_temp_count_all.keys():
			d_insert_all[fa][d_temp_count_all[key]-1] += 1

		#generating trio inheritance
	        for each in d_trio_info.keys():
			if each == "1459" or each == "1463":
		                for ind in d_trio_info[each]:
					if ind[1] == "father":
					         child1_pos = d_aftTPM[ind[0]]
					elif ind[1] == "paternal grandfather":
					        dad1_pos = d_aftTPM[ind[0]]
					elif ind[1] == "paternal grandmother":
					        mom1_pos = d_aftTPM[ind[0]]
					elif ind[1] == "mother":
					         child2_pos = d_aftTPM[ind[0]]
					elif ind[1] == "maternal grandfather":
					        dad2_pos = d_aftTPM[ind[0]]
					elif ind[1] == "maternal grandmother":
					        mom2_pos = d_aftTPM[ind[0]]
			else:
		                for ind in d_trio_info[each]:
					if ind[1] == "child":
					         child_pos = d_aftTPM[ind[0]]
					elif ind[1] == "father":
					        dad_pos = d_aftTPM[ind[0]]
					elif ind[1] == "mother":
					        mom_pos = d_aftTPM[ind[0]]

			if each == "1459":
				inheritance([dad1_pos,mom1_pos],child1_pos,"paternal_",each,output)
				inheritance([dad2_pos,mom2_pos],child2_pos,"maternal_",each,output)
			elif each == '1463':
				inheritance([dad2_pos,mom2_pos],child2_pos,"maternal_",each,output)
			else:
				inheritance([dad_pos,mom_pos],child_pos,"",each,output)
			
	for each in output.keys():
	        if output[each][1] == 0:
	                add_in_final(final_output,each,["0.0",str(output[each][1])])
	        else:
	                add_in_final(final_output,each,[str("%.1f")%(output[each][0]*100.0/output[each][1]),str(output[each][1])])

        sorted_ID = sorted(final_output.keys())
        for each in sorted_ID:
                out_pos.write(each[0]+"\t"+each[1]+"\t"+"\t".join(final_output[each])+"\n")
        out_pos.close()


	for each in denovo_output.keys():
		if denovo_output[each][1] == 0:
			add_in_final(final_denovo_output,each,["0.0",str(denovo_output[each][1])])
		else:
			add_in_final(final_denovo_output,each,[str("%.1f")%(denovo_output[each][0]*100.0/denovo_output[each][1]),str(denovo_output[each][1])])

	sorted_denovo_ID = sorted(final_denovo_output.keys())
	for each in sorted_denovo_ID:
		out_denovo.write(each[0]+"\t"+each[1]+"\t"+"\t".join(final_denovo_output[each])+"\n")
	out_denovo.close()

#print total_insert
#print d_insert

#generating loci count plot for all parents
N = count_ind/3*2
ind = np.arange(N)  # the x locations for the groups
width = 0.45       # the width of the bars
fig, ax = plt.subplots()
poly = [(f*100.0/total_insert["Polymorphic"]) for f in d_insert["Polymorphic"]]
rects1 = ax.bar(ind, poly, width, color='r')
poly2 = [(f*100.0/total_insert["Novel_polymorphic"]) for f in d_insert["Novel_polymorphic"]]
rects2 = ax.bar(ind+width, poly2, width, color='y')

# add some text for labels, title and axes ticks
ax.set_ylabel('% of loci')
ax.set_xlabel('Number of individual')
ax.set_title('% of loci group by polymorphic and novel polymorphic')
ax.set_xticks(ind + width)
ax.set_xticklabels([x+1 for x in range(count_ind/3*2)])
plt.xlim(0,count_ind/3*2)

ax.legend((rects1[0], rects2[0]), ('Polymorphic', 'Novel_polymorphic'))
fig.set_size_inches(12.5, 10.5, forward=True)
fig.savefig(path_current+'Results%s/%s%sunrel_ind_count_loci_group_poly_and_novel_poly.pdf'%(option_tag,MEI,option_tag))
plt.close(fig)

#print total_insert_all
#print d_insert_all

#generating loci count plot for all individuals
N = count_ind
ind = np.arange(N)  # the x locations for the groups
width = 0.45       # the width of the bars
fig, ax = plt.subplots()
poly = [(f*100.0/total_insert_all["Polymorphic"]) for f in d_insert_all["Polymorphic"]]
rects1 = ax.bar(ind, poly, width, color='r')
poly2 = [(f*100.0/total_insert_all["Novel_polymorphic"]) for f in d_insert_all["Novel_polymorphic"]]
rects2 = ax.bar(ind+width, poly2, width, color='y')

# add some text for labels, title and axes ticks
ax.set_ylabel('% of loci')
ax.set_xlabel('Number of individual')
ax.set_title('% of loci group by polymorphic and novel polymorphic')
ax.set_xticks(ind + width)
ax.set_xticklabels([x+1 for x in range(count_ind)])
plt.xlim(0,count_ind)

ax.legend((rects1[0], rects2[0]), ('Polymorphic', 'Novel_polymorphic'))
fig.set_size_inches(12.5, 10.5, forward=True)
fig.savefig(path_current+'Results%s/%s%sall_ind_count_loci_group_poly_and_novel_poly.pdf'%(option_tag,MEI,option_tag))
plt.close(fig)

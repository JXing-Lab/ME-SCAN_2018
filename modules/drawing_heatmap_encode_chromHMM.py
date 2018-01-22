import argparse,os
import matplotlib.pyplot as plt
import numpy as np
from operator import add

parser=argparse.ArgumentParser()

parser.add_argument('--input_num',nargs='*')
parser.add_argument('--input_total',nargs='*')
parser.add_argument('--output',nargs='*')
args=parser.parse_args()
input_num=''.join(args.input_num)
input_total=''.join(args.input_total)
output=''.join(args.output)


f_num = open(input_num, 'r')
f_total = open(input_total, 'r')


data_num=[]
for row_num in f_num.readlines():
	columns_num = row_num.split()
	eachline_num = [int(cn) for cn in columns_num[1:]]
	data_num.append(eachline_num)



data_total=[]
for row_total in f_total.readlines():
	columns_total = row_total.split()
	eachline_total = [int(cn) for cn in columns_total[1:]]
	data_total.append(eachline_total)

#data=np.array(data_num)
data=np.array(data_num)/np.array(data_total)

column_labels = np.array(range(15))+np.array([1]*15)
row_labels = ('H1 ES','K562','GM15878','HepG2','HUVEC','HSMM','NHLF','NHEK','HMEC') # same order to reference paper

heatmap = plt.pcolor(data)

#for y in range(data.shape[0]):
#    for x in range(data.shape[1]):
#        plt.text(x + 0.5, y + 0.5, '%.4f' % data[y, x],
#                 horizontalalignment='center',
#                 verticalalignment='center',
#                 fontsize=5
#                 )

plt.colorbar(heatmap)

xtick=np.array(range(data.shape[1]))+np.array([0.5]*9)
ytick=np.array(range(data.shape[0]))+np.array([0.5]*15)

plt.xticks(xtick, row_labels, rotation='vertical')
plt.tick_params(axis='x', labeltop='off',labelbottom='on')

plt.yticks(ytick, column_labels)
plt.ylim([0,15])
plt.gca().invert_yaxis()
plt.savefig(output)

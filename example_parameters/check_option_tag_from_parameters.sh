#!/bin/sh
for parameters_file in $(ls *parameters)
    do
		cores=$(nproc)
		MEI=$(cat $parameters_file|awk -F "=" '$1=="MEI" {print $2}') 
		MEI_ref_RM=$(cat $parameters_file|awk -F "=" '$1=="MEI_ref_RM" {print $2}')
		MEI_known_stewart=$(cat $parameters_file|awk -F "=" '$1=="MEI_known_stewart" {print $2}')
		MEI_known_dbrip=$(cat $parameters_file|awk -F "=" '$1=="MEI_known_dbrip" {print $2}')
		window_size=$(cat $parameters_file|awk -F "=" '$1=="window_size" {print $2}')
		mapq_bwa=$(cat $parameters_file|awk -F "=" '$1=="mapq_bwa" {print $2}')
		blast_score_R1=$(cat $parameters_file|awk -F "=" '$1=="blast_score_R1" {print $2}')
		blast_score_ref=$(cat $parameters_file|awk -F "=" '$1=="blast_score_ref" {print $2}')
		primer_position=$(cat $parameters_file|awk -F "=" '$1=="primer_position" {print $2}')
		ME_fragment=$(cat $parameters_file|awk -F "=" '$1=="ME_fragment" {print $2}')
		repeatcover=$(cat $parameters_file|awk -F "=" '$1=="repeatcover" {print $2}')
		clustering_type=$(cat $parameters_file|awk -F "=" '$1=="clustering_type" {print $2}')


		option_tag="."$mapq_bwa"."$blast_score_R1"."$blast_score_ref"."$window_size".repeatcover_"$repeatcover"."$clustering_type"."
		echo -e "\e[0;0m"$parameters_file" -->  \e[0;31m"$option_tag
	done

echo -e "\e[0;0m"
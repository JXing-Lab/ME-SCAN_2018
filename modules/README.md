# This folder contains python codes to be called by main pipeline `ME-Scan.sh`

Here are the list of python codes used in each step:
1. step B1 - `BB_mapping.py`
2. step B1a - `JW_separate_into_ME.py`
3. step B1b - `JW_separate_BB_sorted_bam.py`
4. step B2 - `BB_mappedread2convert.py`
5. step B4 - `BB_all_insert_flexible.py`,`BB_all_insert.py`,`BB_insert_flexible.py`,`BB_insert.py`,
6. step D1 - `JW_producing_fixed_insertion_with_ind_info.py`
7. step D2 - `JW_heatmap.py`, `JW_sensitivity_surface_TPM_UR.pyJW_sensitivity_surface_TPM_UR.py`
8. step D3 - `JW_latest_data_with_TPM_UR_as_filter.py`
9. step D4 - `JW_template_inheritance_calculation_for_latest_data_with_TPM-UR_filters.pyJW_template_inheritance_calculation_for_latest_data_with_TPM-UR_filters.py`
10. step D5 - `JW_denovo_list.py`
11. step D6 - `JW_producing_all_insertion_with_ind_info.py`
12. step D7 - `drawing_pie_chart_intersection_gene.py`
13. step D8 - `drawing_heatmap_encode_chromHMM.py`
14. step E - `JW_bed2vcf.py`

The files `JW_TS_concordance_analysis.py`,`JW_TS_inheritance_calculation.py`, and `JW_TS_insertion_among_ind.py` are needed for 3 TS library (Refer to modification part under family_info/README.md)

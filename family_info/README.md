# family information files used for pMEI inheritance analysis

* The files "library_12_trios.txt" (for 12 trios library) and "library_3_TS_trio.txt" (for 3 TS library) will be used by module `JW_template_inheritance_calculation_for_latest_data_with_TPM-UR_filters.py` in step D4 of the pipeline `MEScaner.sh`.

* For 12 trios library, we generated 3 separate sequencing libraries for Alu, LINE, and SVA respectively, thus we used standard pipeline for data analysis. 

* For 3 TS library, it is composed of 12 samples with Blood, iPSC, NSC and Neuron for each of the 3 individuals. We generated one sequencing library containing Alu, LINE and SVA elements. To analyze the pooled library, several modifications in the pipeline were made:

1. Run steps 1a and 1b in addition to step 1. Because the library is pooled, we need to include `JW_separate_into_ME.py` and `JW_separate_BB_sorted_bam.py` in the pipeline.
2. Replace `modules/JW_template_inheritance_calculation_for_latest_data_with_TPM-UR_filters.py` with `modules/JW_TS_inheritance_calculation.py` for step D4.
3. Instead of step E for converting bed to vcf format, run `modules/JW_TS_insertion_among_ind.py` to generate list of insertions in one individual:

`python modules/JW_TS_insertion_among_ind.py --input_file /lab01/Projects/MEScan/MEScan_Paper/analysis/analysis_3_TS_samples/output_bwa-blast.30.65.65.500.repeatcover_off.flexible./latest_data_TPM-10UR_filters_Novel_polymorphic_insertion_minus_SVA.30.65.65.500.repeatcover_off.flexible.bed /lab01/Projects/MEScan/MEScan_Paper/analysis/analysis_3_TS_samples/output_bwa-blast.30.65.65.500.repeatcover_off.flexible./latest_data_TPM-10UR_filters_Novel_polymorphic_insertion_plus_SVA.30.65.65.500.repeatcover_off.flexible.bed`

4. To generate concordance analysis across cell types, run `modules/JW_TS_concordance_analysis.py`: 

`python modules/JW_TS_concordance_analysis.py --mei SVA --option_tag .30.65.65.500.repeatcover_off.flexible. --path /lab01/Projects/MEScan/MEScan_Paper/analysis/analysis_3_TS_samples/`

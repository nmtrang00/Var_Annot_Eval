#!/bin/python
import pandas as pd
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='To get most severe consequence for each variant from SIFT4G')
parser.add_argument("-i", "--input", help="Dir to the SIFT4G annotation file (eg. toy_SIFTannotations.xls)", type=str)
parser.add_argument("-r", "--reference", help="Dir to the ID table created from the original VCF", type=str)
parser.add_argument("-o", "--output", help="Dir to the output tab", type=str)
args = parser.parse_args()

inref=pd.read_csv(args.reference, sep="\t", header=0)
final_dict=dict()
for i in range(inref.shape[0]):
    final_dict[inref["var"][i]]=0

indf=pd.read_csv(args.input, sep='\t', header=0)
#CHROM   POS     REF_ALLELE      ALT_ALLELE      TRANSCRIPT_ID   GENE_ID GENE_NAME       REGION  VARIANT_TYPE    REF_AMINO       ALT_AMINO       AMINO_POS       SIFT_SCORE      SIFT_MEDIAN     NUM_SEQS        dbSNP   SIFT_PREDICTION
for i in range(indf.shape[0]):
    # Check format of the id
    if not "chr" in str(indf["CHROM"][i]):
        var_id="chr"+str(indf["CHROM"][i])+':'+str(indf["POS"][i])+"-"+indf["REF_ALLELE"][i]+'-'+indf['ALT_ALLELE'][i]
    else:
        var_id=str(indf["CHROM"][i])+':'+str(indf["POS"][i])+"-"+indf["REF_ALLELE"][i]+'-'+indf['ALT_ALLELE'][i]
    # Check if there exists a record of that variant
    ## NO => Add record
    if len(final_dict[var_id])==1:
        final_dict[var_id].extend(indf["TRANSCRIPT_ID"][i], indf["VARIANT_TYPE"][i], indf["SIFT_SCORE"][i], indf["SIFT_MEDIAN"][i], indf["SIFT_PREDICTION"][i]])
    ## YES => Check if there are "Low confidence" warnings in records
    ### Only in new record => Keep old record
    elif "*WARNING! Low confidence" in indf["SIFT_PREDICTION"][i] and not "*WARNING! Low confidence" in final_dict[var_id][4]:
        continue
    ### Only in old record => Update record
    elif not "*WARNING! Low confidence" in indf["SIFT_PREDICTION"][i] and "*WARNING! Low confidence" in final_dict[var_id][4]:
        final_dict[var_id].extend(indf["TRANSCRIPT_ID"][i], indf["VARIANT_TYPE"][i], indf["SIFT_SCORE"][i], indf["SIFT_MEDIAN"][i], indf["SIFT_PREDICTION"][i]])
    ### Either in both or not in both => Check type of prediction: "D" is more severe than "T"
    else:
        #### D-T => Keep old record
        if "DELETERIOUS" in final_dict[var_id][4] and "TOLERATED" in indf["SIFT_PREDICTION"][i]:
            continue
        #### T-T and score closer to 1 => Update record
        elif  "TOLERATED" in indf["SIFT_PREDICTION"][i] and indf["SIFT_SCORE"][i] > final_dict[var_id][2]:
            final_dict[var_id].extend([indf["TRANSCRIPT_ID"][i], indf["VARIANT_TYPE"][i], indf["SIFT_SCORE"][i], indf["SIFT_MEDIAN"][i], indf["SIFT_PREDICTION"][i]])
        #### *-D and score closer to 0 => Update record
        elif "DELETERIOUS" in indf["SIFT_PREDICTION"][i] and indf["SIFT_SCORE"][i] < final_dict[var_id][2]:
            #Score for deleterious always smaller than score for tolerated => work for case both are D and case current is D, former is T
            final_dict[var_id].extend([indf["TRANSCRIPT_ID"][i], indf[indf["VARIANT_TYPE"][i], indf["SIFT_SCORE"][i], indf["SIFT_MEDIAN"][i], indf["SIFT_PREDICTION"][i]]])

final_df=pd.DataFrame.from_dict(final_dict,orient="index")
final_df.columns=["SIFT_transcript_id", "SIFT_variant_type", "SIFT_score", "SIFT_median", "SIFT_prediction"]
final_df.to_csv(args.output,sep='\t')
~                                                                                                                                 
                 

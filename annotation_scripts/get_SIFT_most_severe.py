#!/bin/python
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='To get most severe consequence for each variant from SIFT4G')
parser.add_argument("-i", "--input", help="Dir to the SIFT4G annoation file (eg. toy_SIFTannotations.xls)", type=str)
parser.add_argument("-o", "--output", help="Dir to the output tab", type=str)
args = parser.parse_args()

indf=pd.read_csv(args.input, sep='\t', header=0)
#CHROM   POS     REF_ALLELE      ALT_ALLELE      TRANSCRIPT_ID   GENE_ID GENE_NAME       REGION  VARIANT_TYPE    REF_AMINO       ALT_AMINO       AMINO_POS       SIFT_SCORE      SIFT_MEDIAN     NUM_SEQS        dbSNP   SIFT_PREDICTION
final_dict=dict()
for i in range(indf.shape[0]):
  
    if not type(indf["SIFT_PREDICTION"][i]) == str:
        continue
    var_id="chr"+str(indf["CHROM"][i])+':'+str(indf["POS"][i])+"-"+indf["REF_ALLELE"][i]+'-'+indf['ALT_ALLELE'][i]
    if not var_id in final_dict.keys():
        final_dict[var_id]=[indf["TRANSCRIPT_ID"][i], indf["VARIANT_TYPE"][i], indf["SIFT_SCORE"][i], indf["SIFT_MEDIAN"][i], indf["SIFT_PREDICTION"][i]]
    elif "*WARNING! Low confidence" in indf["SIFT_PREDICTION"][i]:
        continue
    elif "DELETERIOUS" in final_dict[var_id][4] and "TOLERATED" in indf["SIFT_PREDICTION"][i]:
        continue
    else:
        if indf["SIFT_PREDICTION"][i] == "TOLERATED" and indf["SIFT_SCORE"][i] > final_dict[var_id][2]:
            final_dict[var_id]=[indf["TRANSCRIPT_ID"][i], indf["VARIANT_TYPE"][i], indf["SIFT_SCORE"][i], indf["SIFT_MEDIAN"][i], indf["SIFT_PREDICTION"][i]]
        elif indf["SIFT_PREDICTION"][i] == "DELETERIOUS" and indf["SIFT_SCORE"][i] < final_dict[var_id][2]:
            final_dict[var_id]=[indf["TRANSCRIPT_ID"][i], indf[indf["VARIANT_TYPE"][i], indf["SIFT_SCORE"][i], indf["SIFT_MEDIAN"][i], indf["SIFT_PREDICTION"][i]]]
final_df=pd.DataFrame.from_dict(final_dict,orient="index")
final_df.columns=["SIFT_transcript_id", "SIFT_variant_type", "SIFT_score", "SIFT_median", "SIFT_prediction"]
final_df.to_csv(args.output,sep='\t')
~                                                                                                                                 
                 

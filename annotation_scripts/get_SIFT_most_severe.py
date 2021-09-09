#!/bin/python
from typing import final
import pandas as pd
from cyvcf2 import VCF
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='To get most severe consequence for each variant from SIFT4G')
parser.add_argument("-i", "--input", help="Dir to the SIFT4G annotation file (eg. toy_SIFTannotations.xls)", type=str)
parser.add_argument("-r", "--reference", help="Dir to the input VCF", type=str)
parser.add_argument("-o", "--output", help="Dir to the output tab", type=str)
args = parser.parse_args()

invcf=VCF(args.reference)
final_dict=dict()
for variant in invcf:
    if "chr" in str(variant.CHROM):
        chr=str(variant.CHROM)
    else:
        chr="chr"+str(variant.CHROM)
    try:
        var_id=chr+':'+str(variant.POS)+"-"+variant.REF+'-'+variant.ALT[0]
        final_dict[var_id]=[variant.ID]
    except:
        var_id=chr+':'+str(variant.POS)+"-"+variant.REF+'-.'
        final_dict[var_id]=[variant.ID]

#CHROM|0   POS|1     REF_ALLELE|2      ALT_ALLELE|3      TRANSCRIPT_ID|4   GENE_ID|5 GENE_NAME|6       REGION|7  VARIANT_TYPE|8    REF_AMINO|9       ALT_AMINO|10       AMINO_POS|11       SIFT_SCORE|12      SIFT_MEDIAN|13     NUM_SEQS|14        dbSNP|15   SIFT_PREDICTION|16
with  open(args.input) as infile:
    line=infile.readline()
    count=0
    while line:
        print(count)
        sift=line.strip().split("\t")
        # Check format of the id
        if not "chr" in sift[0]:
            var_id="chr"+sift[0]+':'+sift[1]+"-"+sift[2]+'-'+sift[3]
        else:
            var_id=sift[0]+':'+sift[1]+"-"+sift[2]+'-'+sift[3]
        # Check if the variant is in the desired list
        if not var_id in final_dict.keys():
            line=infile.readline()
            count+=1
            continue
        # Check if there exists a record of that variant
        ## NO => Add record
        if len(final_dict[var_id])==1:
            final_dict[var_id].extend([sift[4], sift[8], sift[12], sift[13], sift[16]])
        ## YES => Check if there are "Low confidence" warnings in records
        ### Only in new record => Keep old record
        elif "*WARNING! Low confidence" in sift[16] and not "*WARNING! Low confidence" in final_dict[var_id][4]:
            line=infile.readline()
            count+=1
            continue
        ### Only in old record => Update record
        elif not "*WARNING! Low confidence" in sift[16] and "*WARNING! Low confidence" in final_dict[var_id][4]:
            final_dict[var_id][1]=sift[4]
            final_dict[var_id][2]=sift[8]
            final_dict[var_id][3]=sift[12]
            final_dict[var_id][4]=sift[13]
            final_dict[var_id][5]=sift[16]
            #final_dict[var_id].extend([sift[4], sift[8], sift[12], sift[13], sift[16]])
        ### Either in both or not in both => Check type of prediction: "D" is more severe than "T"
        else:
            #### D-T => Keep old record
            if "DELETERIOUS" in final_dict[var_id][4] and "TOLERATED" in sift[16]:
                line=infile.readline()
                count+=1
                continue
            #### T-T and score closer to 1 => Update record
            elif  "TOLERATED" in sift[16] and sift[12] > final_dict[var_id][2]:
                final_dict[var_id][1]=sift[4]
                final_dict[var_id][2]=sift[8]
                final_dict[var_id][3]=sift[12]
                final_dict[var_id][4]=sift[13]
                final_dict[var_id][5]=sift[16]
            #### *-D and score closer to 0 => Update record
            elif "DELETERIOUS" in sift[16] and sift[12] < final_dict[var_id][2]:
                #Score for deleterious always smaller than score for tolerated => work for case both are D and case current is D, former is T
                final_dict[var_id][1]=sift[4]
                final_dict[var_id][2]=sift[8]
                final_dict[var_id][3]=sift[12]
                final_dict[var_id][4]=sift[13]
                final_dict[var_id][5]=sift[16]
        line=infile.readline()
        count+=1
final_df=pd.DataFrame.from_dict(final_dict,orient="index")
final_df.columns=["id","SIFT_transcript_id", "SIFT_variant_type", "SIFT_score", "SIFT_median", "SIFT_prediction"]
final_df.to_csv(args.output,sep='\t')                                                                                                      

#!/bin/python

import pandas as pd
import argparse
import numpy as np

# Parse arguments
parser = argparse.ArgumentParser(description='To conbine CADD scores for SNPs (SNVs) and indels')
parser.add_argument("-s", "--snp", help="Dir to CADD scores for SNPs", type=str)
parser.add_argument("-i", "--indel", help="Dir to the input tab delimited file", type=str)
parser.add_argument("-o", "--output", help="Dir to the output file", type=str)
args = parser.parse_args()

cadd_indel=pd.read_csv(args.indel, sep="\t", header=0, names=["var", "CADD", "CADD_phred"])
indel_dict=dict()
for i in range(cadd_indel.shape[0]):
    if np.isnan(cadd_indel["CADD"][i]):
        continue
    else:
        indel_dict[cadd_indel["var"][i]]=[cadd_indel["CADD"][i], cadd_indel["CADD_phred"][i]]

cadd_snv=pd.read_csv(args.snp, sep="\t", header=0, names=["var", "CADD",  "CADD_phred"])
final_dict=dict()
for i in range(cadd_snv.shape[0]):
    if np.isnan(cadd_indel["CADD"][i]) and cadd_snv["var"][i] in indel_dict.keys():
        final_dict[cadd_snv["var"][i]]=indel_dict[cadd_snv["var"][i]]
    else:
        final_dict[cadd_snv["var"][i]]=[cadd_snv["CADD"][i], cadd_snv["CADD_phred"][i]]
final_df=pd.DataFrame.from_dict(final_dict, orient="index")
final_df.columns=["CADD", "CADD_phred"]
final_df.to_csv(args.output, sep="\t", index=False)

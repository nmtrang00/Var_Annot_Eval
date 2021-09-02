#!/bin/python

import pandas as pd
from cyvcf2 import VCF
import argparse

parser = argparse.ArgumentParser(description='To create variant and bed file from VCF')
parser.add_argument("-i", "--input", help="Dir to the input vcf.gz", type=str)
parser.add_argument("-o", "--output", help="Dir to the output bed", type=str)
args = parser.parse_args()

invcf=VCF(args.input)
cols=["chr", "start", "end"]
final_dict=dict()
for col in cols:
    final_dict[col]=[]
for variant in invcf:
    chr=str(variant.CHROM)
    final_dict["chr"].append(chr)
    final_dict["start"].append(variant.start)
    final_dict["end"].append(variant.end)
final_df=pd.DataFrame.from_dict(final_dict)
final_df.to_csv(args.output, sep='\t', header=False, index=False)

    

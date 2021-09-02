#!/bin/python

import pandas as pd
from cyvcf2 import VCF
import argparse

parser = argparse.ArgumentParser(description='To create variant and id table from VCF')
parser.add_argument("-i", "--input", help="Dir to the input vcf.gz", type=str)
parser.add_argument("-o", "--output", help="Dir to the output tab", type=str)
args = parser.parse_args()

invcf=VCF(args.input)
var=[]
id=[]
for variant in invcf:
    if "chr" in str(variant.CHROM):
        chr=str(variant.CHROM)
    else:
        chr="chr"+str(variant.CHROM)
    try:
        var_id=chr+':'+str(variant.POS)+"-"+variant.REF+'-'+variant.ALT[0]
        var.append(var_id)
    except:
        var_id=chr+':'+str(variant.POS)+"-"+variant.REF+'-.'
        var.append(var_id)
    id.append(variant.ID)
df=pd.DataFrame()
df["var"]=var
df["id"]=id
df.to_csv(args.output,sep='\t',index=False)
        

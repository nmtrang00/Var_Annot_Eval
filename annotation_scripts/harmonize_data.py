#!/bin/python
import pandas as pd
import argparse
from cyvcf2 import VCF
import numpy as np
# Parse arguments
parser = argparse.ArgumentParser(description='To convert the queried data from UCSC database to a standard format')
parser.add_argument("-t", "--type", help="Type of data", type=str)
parser.add_argument("-r", "--reference_vcf", help="Dir to the reference vcf.gz", type=str)
parser.add_argument("-i", "--input", help="Dir to the input tab delimited file", type=str)
parser.add_argument("-o", "--output", help="Dir to the output file", type=str)
args = parser.parse_args()
'''
a: ada score
con: conservation score
ca: cadd
m: m-cap
mkl: fathmm-mkl
xf: fathmm-xf
pri: primateAI
'''
inref=VCF(args.reference_vcf)
final_dict=dict()
count_var=0
for variant in inref:
    if "chr" in str(variant.CHROM):
        chr=str(variant.CHROM)
    else:
        chr="chr"+str(variant.CHROM)
    try:
        if args.type in ["con"]:
            var_id=chr+':'+str(variant.start)+'-'+str(variant.end)
        elif args.type in ["ca","m", "xf", "a", "pri"]:
            var_id=chr+':'+str(variant.POS)+"-"+variant.REF+'-'+variant.ALT[0]
        elif args.type in [ "mkl"]:
            var_id=chr+':'+str(variant.start)+'-'+str(variant.end)+"-"+variant.REF+'-'+variant.ALT[0]
        if var_id in final_dict.keys():
            continue
        if args.type in ["xf", "con", "a", "pri"]:
            final_dict[var_id]=[np.nan]
        elif args.type in ["ca","m"]:
            final_dict[var_id]=[np.nan, np.nan]
        elif args.type in ["mkl"]:
            final_dict[var_id]=[np.nan, np.nan, np.nan, np.nan]

    except:
        continue

if args.type in ["xf", "a", "pri"]:
    h=["chr","pos", "ref","alt","score"]
elif args.type in ["m"]:
    h=["chr","pos", "ref","alt","mcapv1.4", "mcap_sensitivityv1.4"]
elif args.type in ["ca"]:
    h=["chr","pos", "ref","alt","CADD", "CADD_phred"]
elif args.type in ["mkl"]:
    h=["chr","start","end","ref","alt","NC.score","NC.groups","C.score","C.groups"]
elif args.type in ["con"]:
    h=["chr", "start", "end", "len", "score"]

indf=pd.read_csv(args.input, sep='\t', names=h)
for i in range(indf.shape[0]):
    try:
        if args.type in ["con"]:
            var=str(indf["chr"][i])+':'+str(indf["start"][i])+"-"+str(indf["end"][i])
        elif args.type in ["ca", "xf", "a", "pri"]:
            var="chr"+str(indf["chr"][i])+':'+str(indf["pos"][i])+"-"+indf["ref"][i]+'-'+indf["alt"][i]
        elif args.type in ["m", "mkl"]:
            var="chr"+str(indf["chr"][i])+':'+str(indf["start"][i])+"-"+str(indf["end"][i])+"-"+str(indf["ref"][i])+'-'+str(indf["alt"][i])
        if var in final_dict.keys():
            if args.type in ["ca"]:
                final_dict[var][0]=indf["CADD"][i]
                final_dict[var][1]=indf["CADD_phred"][i]
            elif args.type in ["mkl"]:
                final_dict[var][0]=indf["NC.score"][i]
                final_dict[var][1]=indf["NC.groups"][i]
                final_dict[var][2]=indf["C.score"][i]
                final_dict[var][3]=indf["C.groups"][i]
            elif args.type in ["m"]:
                final_dict[var][0]=indf["mcapv1.4"][i]
                final_dict[var][1]=indf["mcap_sensitivityv1.4"][i]
        else:
                if args.type in ["con"] and len(indf["score"][i].split(','))>1:
                    continue
                final_dict[var][0]=indf["score"][i]
        else:
            continue
    except:
        continue
final_df=pd.DataFrame.from_dict(final_dict, orient="index")
if args.type in ["xf", "con", "a"]:
    final_df.columns=["score"]
elif args.type in ["ca"]:
    final_df.columns=["CADD", "CADD_phred"]
elif args.type in ["mkl"]:
    final_df.columns=["NC.score","NC.groups","C.score","C.groups"]
elif args.type in ["m"]:
    final_df.columns=["mcapv1.4", "mcap_sensitivityv1.4"]
if args.type in ["ca"]:
    final_df.to_csv(args.output, sep='\t', index=True)
else:
    final_df.to_csv(args.output, sep='\t')

#!/bin/bash

typ=$1
invcf=$2
inbed=$3
ref=$4
out=$5

tabix -R $inbed $ref > $out
python3 harmonize_data.py -t $1 -r $invcf -i $out -o ${out}_f.tab

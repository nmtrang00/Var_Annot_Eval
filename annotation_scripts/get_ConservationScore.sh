#!/bin/bash

invcf=$1
inbed=$2
inbW=$3
out=$4

bwtool extract bed $inbed $inbW $out
python3 harmonize_data.py -t con -r $invcf -i $out -o ${out}_f.tab
          

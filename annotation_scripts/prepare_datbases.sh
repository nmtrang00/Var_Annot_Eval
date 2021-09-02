#!/bin/bash

resources=$1

#M-CAP
tabix -C  -p vcf $resources/mcap_v1_4.txt.gz

#Fathmm-mkl
tabix -C -p bed $resources/fathmm-MKL_Current_zerobased.tab.gz

#Ada score from dbscSNV
zcat $resources/dbscSNV1.1.zip |  cut -f1,2,3,4,17 | sed -e '1s/chr/#chr/' > $resources/dbscSNV1.1.AdaOnly.tsv
bgzip dbscSNV1.1.AdaOnly.tsv
tabix -C -p vcf $resources/dbscSNV1.1.AdaOnly.tsv.gz

#primateAI
zcat $resources/PrimateAI_scores_v0.2.tsv.gz | sed '/^$/d' | sed '1,/chr/s/chr/#chr/' | sed 's/^chr//g' | head -n1000  > $resources/PrimateAI_scores_v0.2.scoreOnly.tsv
sort -k1,1V -k2,2n $resources/PrimateAI_scores_v0.2.scoreOnly.tsv > $resources/PrimateAI_scores_v0.2.scoreOnly.sorted.tsv
bgzip $resources/PrimateAI_scores_v0.2.scoreOnly.sorted.tsv
tabix -C -p vcf $resources/PrimateAI_scores_v0.2.scoreOnly.sorted.tsv.gz

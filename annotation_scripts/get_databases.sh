#!/bin/bash

#Create folders
storage_folder=$1

#GERP++
wget --directory-prefix=$storage_folder https://hgdownload.soe.ucsc.edu/gbdb/hg19/bbi/All_hg19_RS.bw

#PhyloP46way
wget --directory-prefix=$storage_folder https://hgdownload.cse.ucsc.edu/goldenpath/hg19/phyloP46way/vertebrate.phyloP46way.bw 

#PhastCons46way
wget --directory-prefix=$storage_folder https://hgdownload.cse.ucsc.edu/goldenpath/hg19/phastCons46way/vertebrate.phastCons46way.bw

#CADD
wget --directory-prefix=$storage_folder https://krishna.gs.washington.edu/download/CADD/v1.6/GRCh37/whole_genome_SNVs.tsv.gz
wget --directory-prefix=$storage_folder https://krishna.gs.washington.edu/download/CADD/v1.6/GRCh37/whole_genome_SNVs.tsv.gz.tbi
wget --directory-prefix=$storage_folder https://krishna.gs.washington.edu/download/CADD/v1.6/GRCh37/InDels.tsv.gz
wget --directory-prefix=$storage_folder https://krishna.gs.washington.edu/download/CADD/v1.6/GRCh37/InDels.tsv.gz.tbi

#M-CAP
wget --directory-prefix=$storage_folder http://bejerano.stanford.edu/mcap/downloads/dat/mcap_v1_4.txt.gz

#FATHMM-MKL
wget --directory-prefix=$storage_folder http://fathmm.biocompute.org.uk/database/fathmm-MKL_Current_zerobased.tab.gz

#FATHMM-XF
wget --directory-prefix=$storage_folder	https://fathmm.biocompute.org.uk/fathmm-xf/fathmm_xf_coding.vcf.gz
wget --directory-prefix=$storage_folder https://fathmm.biocompute.org.uk/fathmm-xf/fathmm_xf_coding.vcf.gz.tbi
wget --directory-prefix=$storage_folder https://fathmm.biocompute.org.uk/fathmm-xf/fathmm_xf_noncoding.vcf.gz
wget --directory-prefix=$storage_folder https://fathmm.biocompute.org.uk/fathmm-xf/fathmm_xf_noncoding.vcf.gz.tbi

#Ada score from dbscSNV
wget --directory-prefix=$storage_folder ftp://dbnsfp:dbnsfp@dbnsfp.softgenetics.com/dbscSNV1.1.zip

#!/bin/bash

invcf=$1
resources=$2
outdir=$3
keeping_tmp_files=$4
mkdir $outdir/tmp

#1. Check input data
case $invcf in
	*"vcf")
		echo -n "Formatting input data... "
		filename_0="$(basename -- $invcf)"
		filename=${filename_0:0:(${#filename_0}-4)}
		#echo $filename
		bgzip -c $invcf > $outdir/tmp/${filename}.vcf.gz
		tabix $outdir/tmp/${filename}.vcf.gz
		echo "Done"
		vcf=$outdir/tmp/${filename}.vcf.gz
		;;
	*"vcf.gz")
		filename_0="$(basename -- $invcf)"
		filename=${filename_0:0:(${#filename_0}-7)}
		#echo $filename
		vcf=$invcf
    		;;
	*)
		echo "ERROR: The input has wrong format. An input file is a VCF (eg. toy.vcf, toy.vcf.gz)"
		exit 1
		;;
esac
case $keeping_tmp_files in
        0,1)
                ;;
        *)
         	echo "ERROR: Invalid value. Enter 0 to remove tmp annotation files, enter 1 to keep tmp annotation files"
		exit 2
	 	;;
esac
#2. Create id table
echo -n "Creating id table... "
python3 annotation_scripts/create_ID_table.py -i $vcf -o $outdir/tmp/${filename}.ID.tab
echo "Done"

#3. Create bed file for query
echo -n "Creating BED file for query... "
python3 annotation_scripts/create_bed_from_vcf.py -i $vcf -o $outdir/tmp/${filename}.bed
echo "Done"

#4. GERP++
echo -n "Extracting GERP++ scores... "
./annotation_scripts/get_ConservationScore.sh $vcf $outdir/tmp/${filename}.bed $resources/All_hg19_RS.bw $outdir/tmp/${filename}_gerp
echo "Done"

#5. PhyloP46way
echo -n "Extracting PhyloP46way scores... "
./annotation_scripts/get_ConservationScore.sh $vcf $outdir/tmp/${filename}.bed $resources/vertebrate.phyloP46way.bw $outdir/tmp/${filename}_phyloP46
echo "Done"

#6. PhastCon46ways
echo -n "Extracting PhastCons46way scores... "
./annotation_scripts/get_ConservationScore.sh $vcf $outdir/tmp/${filename}.bed $resources/vertebrate.phastCons46way.bw $outdir/tmp/${filename}_phastCon46
echo "Done"

#7. CADD
echo -n "Extracting CADD scores..."
./annotation_scripts/get_IndexedData.sh "ca" $vcf $outdir/tmp/${filename}.bed $resources/whole_genome_SNVs.tsv.gz $outdir/tmp/${filename}_CADD_snv
./annotation_scripts/get_IndexedData.sh "ca" $vcf $outdir/tmp/${filename}.bed $resources/InDels.tsv.gz $outdir/tmp/${filename}_CADD_indel
python3 annotation_scripts/combine_CADD_snv_indel.py -s $outdir/tmp/${filename}_CADD_snv_f.tab -i $outdir/tmp/${filename}_CADD_indel_f.tab -o $outdir/tmp/${filename}_CADD_f.tab
echo "Done"

#8. M-CAP
echo -n "Extracting M-CAP scores..."
./annotation_scripts/get_IndexedData.sh "m" $vcf $outdir/tmp/${filename}.bed $resources/mcap_v1_4.txt.gz $outdir/tmp/${filename}_mcap
echo "Done"

#9. Fathmm-mkl
echo -n "Extracting fathmm-mkl scores..."
./annotation_scripts/get_IndexedData.sh "mkl" $vcf $outdir/tmp/${filename}.bed $resources/fathmm-MKL_Current_zerobased.tab.gz $outdir/tmp/${filename}_mkl
echo "Done"

#10. Fathmm-xf
echo -n "Extracting fathmm-xf scores..."
./annotation_scripts/get_IndexedData.sh "xf" $vcf $outdir/tmp/${filename}.bed $resources/fathmm_xf_coding.vcf.gz $outdir/tmp/${filename}_xfCoding
./annotation_scripts/get_IndexedData.sh "xf" $vcf $outdir/tmp/${filename}.bed $resources/fathmm_xf_noncoding.vcf.gz $outdir/tmp/${filename}_xfNonCoding
echo "Done"

#11. Ada_score
echo -n "Extracting Ada_score from dbscSNV..."
./annotation_scripts/get_IndexedData.sh "a" $vcf $outdir/tmp/${filename}.bed $resources/dbscSNV1.1.AdaOnly.tsv.gz $outdir/tmp/${filename}_ada
echo "Done"

#12. PrimateAI
echo -n "Extracting PrimateAI..."
./annotation_scripts/get_IndexedData.sh "pri" $vcf $outdir/tmp/${filename}.bed $resources/PrimateAI_scores_v0.2.scoreOnly.sorted.tsv.gz $outdir/tmp/${filename}_primateAI
echo "Done"

#13. Merge data
echo -n "Merging annotations... "
./annotation_scripts/combine_data.sh $outdir/${filename}.annotated.tab \
	$outdir/tmp/${filename}.ID.tab \
	$outdir/tmp/${filename}_gerp_f.tab \
	$outdir/tmp/${filename}_phyloP46_f.tab \
	$outdir/tmp/${filename}_phastCon46_f.tab \
	$outdir/tmp/${filename}_CADD_f.tab \
	$outdir/tmp/${filename}_mcap_f.tab \
	$outdir/tmp/${filename}_mkl_f.tab \
	$outdir/tmp/${filename}_xfCoding_f.tab \
	$outdir/tmp/${filename}_xfNonCoding_f.tab \
	$outdir/tmp/${filename}_ada_f.tab \
	$outdir/tmp/${filename}_primateAI_f.tab
echo "Done"

#14. Cleaning tmp files
case $keeping_tmp_files in
	0)
		echo -n  "Cleaning tmp files... "
		rm -r $outdir/tmp/
		echo "Done"
		;;
	1)
		;;
esac
echo "Annotation is done."

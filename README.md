This is a variant annotation and evaluation pipeline as described in [A comprehensive and bias-free evaluation of genomic variant clinical interpretation tools](https://doi.org/10.1109/KSE53942.2021.9648755). Some scoring tools (SIFT4G, Polyphen-2, MutationTaster2021, SpliceAI) only offer command-line or web-based programs. You can follow the instruction below to download and annotate variants with those tools separately, then use provided scripts to format and combine with the annotation from precomputed databases.

# Installation
To optimize the analysis, we use Dython as a submodule and make some alternations to the package. The pipeline and optimized packages can be downloaded as followed.
```
git clone  --recurse-submodules https://github.com/nmtrang00/Var_Annot_Eval
```
If you forget to use ```--recurse-submodules```, please proceed with two lines of codes below.
```
git submodule init
git submodule update
```
The links to github or website of tools not offering precomputed data.
SIFT4G: https://sift.bii.a-star.edu.sg/ 
Polyphen-2: http://genetics.bwh.harvard.edu/pph2/bgi.shtml 
MutationTaster2021: https://www.genecascade.org/MutationTaster2021/info/ 
SpliceAI: https://github.com/Illumina/SpliceAI.git 
Required python packages in requirements.txt can be installed with pip or conda. To prevent any undesired, it is recommended to setup a conda env as followed.
```
conda create -n bwtool python=3.6
conda activate bwtool
conda install -c bioconda htslib==1.3.2
conda install -c pwwang bwtool
conda install -c bioconda openssl=1.0
conda install -c bioconda cyvcf2==0.10.0
conda install -c bioconda pandas==1.1.5
conda install -c anaconda seaborn==0.11.1
conda install -c conda-forge matplotlib==3.4.1
conda install -c conda-forge ppscore==1.2.0
pip install git+https://github.com/mainguyenanhvu/dython.git
```

# Variants Annotation
## Annotation with command line programs
After annotating variants with command-line or web-based programs, do as follow to turn the output the format that can be combined with other precomputed scores.\
### SIFT
Include -t option when running SIFT to get annotations for all possible transcripts, else SIFT automatically chooses the annotation for the 1st transcript. Get the most severe consequences of each variant from SIFT4G:
```
python3 annotation_scripts/get_SIFT_most_severe.py -i [SIFTannotations.xls] -r [inVCF] -o [output]
```
Required parameters:\
- ```-i```: Dir to SIFT output ended with "_SIFTannotations.xls"\
- ```-r```: Dir to inVCF\
- ```-o```: Dir to output TAB with 6 columns: "var", ""SIFT_transcript_id", "SIFT_variant_type","SIFT_score", "SIFT_median", "SIFT_prediction"

## Annotation with precomputed scores
### Precomputed databases
Download databases needed for the annotation.
```
./annotation_scripts/get_databases.sh [resources]
```
Required parameters:\
- ```resources```: Directory to databases storage folder.\
In order to download PrimateAI datbases, you need to have an Illumina account. Please do as instructed in the following link [PrimateAI](https://basespace.illumina.com/s/yYGFdGih1rXL) and download file name "PrimateAI_scores_v0.2.tsv.gz" to the same folder storaging other databases.
Preprocess databases for optimal query:
```
./annotation_scripts/prepare_datbases.sh [resources]
```
Required parameters:\
- ```resources```: Directory to databases storage folder.
### Variants annotation
Run the following script
```
./annotation_scripts/run_annotation.sh [inVCF] [resources] [output] [keeping_tmp_files]
```
Required parameters:\
- ```invcf```: Directory to input VCF with variants of interest.\
- ```resources```: Directory to databases storage folder.\
- ```output```: Directory to annotated TAB.\
- ```keeping_tmp_files```: 0 to remove all tmp scoring files, 1 to keep all of them.

# Data Evaluation
To generate ppscore and association score, use the following command:
```
python annotation_evaluation.py -i [inCSV] -o [outputFolder]
```
- ```-i```: Directory to input tab-formated file.
- ```-o```: Directory to a output folder
# Contact



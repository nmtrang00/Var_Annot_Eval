This is a variant annotation and evaluation pipeline as described in [[Paper name]]. Some scoring tools (SIFT4G, Polyphen-2, MutationTaster2021, SpliceAI) only offer command-line or web-based programs. You can follow the instruction below to download and annotate variants with those tools separately, then use provided scripts to format and combine with the annotation from precomputed databases.

# INSTALLATION
The pipeline and submodules (Dython) can be dowloaded as followed.
```
git clone https://github.com/nmtrang00/KSE2021_Variant-Annotation.git
```
If you only want to download the pipepline, please do as followed.
```
git clone https://github.com/nmtrang00/KSE2021_Variant-Annotation.git
```
The links to github or website of tools not offering precomputed data.
SIFT4G: https://sift.bii.a-star.edu.sg/ \
Polyphen-2: http://genetics.bwh.harvard.edu/pph2/bgi.shtml \
MutationTaster2021: https://www.genecascade.org/MutationTaster2021/info/ \
SpliceAI: https://github.com/Illumina/SpliceAI.git \
Required python packages in requirements.txt can be installed with pip or conda. To prevent any undesired, it is recommended to setup a conda env as followed.
```
conda create -n bwtool
conda activate bwtool
conda install -c bioconda htslib==1.3.2
conda install -c pwwang bwtool
conda install -c bioconda openssl=1.0
conda install -c bioconda cyvcf2==
conda install -c bioconda pandas==
conda install -c anaconda seaborn==
conda install -c conda-forge matplotlib==
conda install -c conda-forge ppscore==
```
For Dython, we perform some alternation to optimize the analysis, please download from the follow repository: https://github.com/mainguyenanhvu/dython.git

# VARIANTS ANNOTATION
## Annotaion with command line programs
In development
## Annotation with precomputed scores
### Precomputed databases
Download databases needed for the annotation.
```
./annotation_scripts/get_databases.sh /dir/to/storage/folder
```
In order to download PrimateAI datbases, you need to have an Illumina account. Please do as instructed in the following link [PrimateAI](https://basespace.illumina.com/s/yYGFdGih1rXL) and download file name "PrimateAI_scores_v0.2.tsv.gz" to the same folder storaging other databases.
Preprocess databases for optimal query:
```
./annotation_scripts/prepare_datbases.sh /dir/to/storage/folder
```

### Variants annotation
Run the following script
```
./annotation_scripts/run_annotation.sh [inVCF] [resources] [output] [keeping_tmp_files]
```
Required parameters:
-```invcf```: Directory to input VCF with variants of interest.
-```resources```: Directory to databases storage folder.
-```output```: Directory to annotated TAB.
-```keeping_tmp_files```: 0 to remove all tmp scoring files, 1 to keep all of them.

# DATA EVALUATION

# CONTACT



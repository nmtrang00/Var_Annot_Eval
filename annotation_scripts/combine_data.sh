#!/bin/bash

output=$1
id_table=$2
gerp=$3
phyloP=$4
phastCon=$5
cadd=$6
mcap=$7
mkl=$8
xfC=$9
xfNC=${10}
ada=${11}
primate=${12}

paste -d "\t"  $id_table $gerp $phyloP $phastCon $cadd $mcap $mkl $xf $ada $primate > $output 

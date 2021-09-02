#!/usr/bin/env Rscript
 
require(raster)
require(httr)
require(jsonlite)
require(vcfR)
require(stringr)
ext="https://genecascade.org/MT2021/MT_API102.cgi?variants="
target=read.vcfR(args[1])
df=target@fix[,c(1,2,4,5)]
id=apply(df,1,function(i) paste(i[1],":",i[2],i[3],"%3E",i[4],sep=""))

 


fetch.MT=function(id){
  result.o=list()
  i=length(result.o)
  while (length(result.o)<length(id)) {
    tryCatch(
      {
        r=read.csv(text=content(GET(paste(ext,id[i+1],sep = "")),"text"),sep="\t")[,c(2:5,10)]
        r.hgvs=apply(r[,1:4],1,function(i) paste(i[1],":",i[2],":",i[3],":",i[4],sep = ""))
        r=data.frame(r.hgvs,r[,5])
        if (!"ERROR..Data.error" %in% names(i)) {
          result.o=append(result.o,list(r))
          
          write.table(r, file=args[2], sep="\t", append=TRUE , row.names=FALSE, col.names=FALSE)
        }
        cat(i,"\n")   
        i=length(result.o)
      }
    )
  }
}

 

fetch.MT()

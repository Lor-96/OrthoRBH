# RBH_software
## Introduction

This software can perform a Reciprocal Best Hit (RBH) using the BLAST output as input file and return the predicted orthologs
for the 2 chosen species.

As input file is possible to use also the output of the Exalign Software (i.e., exalign_example.tsv.tab),
if this type of file is used, both the recommended percentage argument (```-perc```)
and the recommended bitscore argument (```-bit```) are 0, because the Exalign gives already a score for the match of the 2 input files.

The GTF file can be used also in gzipped extension (```sp1.gtf.gz```).

The tool can return also the discrepancies found during the assegnation of the gene names while reading the protein/transcripts.

In order to efficiently predict orthologs, for the analysis of the proteins is recommended to use in this tool as input the BLASTP output 
done bewteen two species comparing one isoform per gene.

For the transcripts analysis is recommended to use the Exalign Software or make a BLASTN between all the transcripts for both species and use them
as input for the tool.

For this software you need ALL the arguments as input, and mainly need:
- BLAST output (-outfmt 7) of the first species against the second 
- BLAST output (-outfmt 7) of the second species against the first
- GTF file of the first species
- GTF file of the second species
- Threshold for identity percentage 
- Threshold for bitscore percentage


### Usage

```
usage: main.py [-h] -b1 --blast1 -b2 --blast2 -gtf1 --gtf1 -gtf2 --gtf2 -perc --percentage -bit --bitscore

optional arguments:
  -h, --help          show this help message and exit
  -b1 --blast1        Blast result for Species 1 vs Species 2
  -b2 --blast2        Blast result for Species 2 vs Species 1
  -gtf1 --gtf1        GTF file for Species 1
  -gtf2 --gtf2        GTF file for Species 2
  -perc --percentage  Threshold for the percentage of identity
  -bit --bitscore     Threshold for the Bitscore
```

 #### Example Command Windows
```
python main.py -b1 '.\inputblast1.txt' -b2 '.\inputblast2.txt' -gtf1 '.\sp1.gtf' -gtf2 '.\sp2.gtf' -perc 40 -bit 0.2
```

#### Example Command Linux
```
python main.py -b1 inputblast1.txt -b2 inputblast2.txt -gtf1 sp1.gtf  -gtf2 sp2.gtf  -perc 40 -bit 0.2
```


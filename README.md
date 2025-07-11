## OrthoRBH

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

## Introduction

This software can perform a Reciprocal Best Hit (RBH) using the BLAST output as input file and return the predicted orthologs
for the 2 chosen species.

As input file is possible to use also the output of the Exalign Software (i.e., exalign_example.tsv.tab),
if this type of file is used, both the recommended percentage argument (```-perc```)
and the recommended bitscore argument (```-bit```) are 0, because the Exalign workflow already assigns a score for the match of the 2 input files.

The GTF file can be used also in gzipped extension (```sp1.gtf.gz```).

The tool can return also the discrepancies found during the assegnation of the gene names while reading the protein/transcripts.

In order to efficiently predict orthologs, for the analysis of the proteins is recommended to use as input the BLASTP output done bewteen two species comparing one isoform per gene.

For the transcripts analysis is recommended to use the Exalign software or make a BLASTN between all the transcripts for both species and use them
as input for the tool.

Here two files of input (```inputblast1.txt```, ```inputblast2.txt```) have been reported as example from a BLASTP analysis between Homo Sapiens and Mus Musculus, these files contain only the first 1000 proteins
aligned with BLASTP, the GTF files have to be downloaded from the [RefSeq index of genomes](https://ftp.ncbi.nlm.nih.gov/genomes/refseq/), choosing the
species you want, for files reported as example you need to use *Homo Sapiens* as species1 and *Mus Musculus* as species2.

For this software you need ALL the arguments as input, and mainly need:
- BLAST output (-outfmt 7) of the first species against the second 
- BLAST output (-outfmt 7) of the second species against the first
- GTF file of the first species
- GTF file of the second species
- Threshold for identity percentage 
- Threshold for bitscore percentage

There are also optional argument that are:
- EVALUE is a value that is by default set to 0.001 and it is necessary to filter the Exalign matches together with the SCORE, it is recommended to not change it if you are not sure of the result that you want obtain.
- SCORE  is a value that is by default set to 0 and is necessary to filt together with the SCORE the Exalign table hits, it is recommended to not change it if youn are not sure of the result that you want obtain.
- Transcripts is a boolean value set it as "True" if the BLAST output that you usa as input contain transcripts instead of proteins.


### Usage

```
usage: main.py [-h] -b1 --blast1 -b2 --blast2 -gtf1 --gtf1 -gtf2 --gtf2 -perc --percentage -bit --bitscore [-ev --pvalue] [-sc --score]
               [-tr --transcript]

optional arguments:
  -h, --help          show this help message and exit
  -b1 --blast1        Blast result for Species 1 vs Species 2
  -b2 --blast2        Blast result for Species 2 vs Species 1
  -gtf1 --gtf1        GTF file for Species 1
  -gtf2 --gtf2        GTF file for Species 2
  -perc --percentage  Threshold for the percentage of identity
  -bit --bitscore     Threshold for the Bitscore
  -ev --pvalue        Exalign Threshold for the pvalue
  -sc --score         Exalign threshold for the score
  -tr --transcript    Set it as "True" if in the BLAST there are transcripts instead of proteins
```

 #### Example Command Windows
```
python main.py -b1 .\inputblast1.txt -b2 .\inputblast2.txt -gtf1 .\sp1.gtf -gtf2 .\sp2.gtf -perc 40 -bit 0.2
```

#### Example Command Linux
```
python main.py -b1 inputblast1.txt -b2 inputblast2.txt -gtf1 sp1.gtf  -gtf2 sp2.gtf  -perc 40 -bit 0.2
```


# Positional Covariance Statistical Learning (PCSL)
> PCSL is a statistical learning method that parametrizes the Elastic Network Model from positional covariance of structural ensemble.

## Contents

README: Instructions for installation.

Dataset:
- str_collection_log: Log file during the collection of homologous structures
- ref: The reference sequence in fasta format
- homo: Raw homologous sequences in fasta format
- pdb_store: Please unzip the compressed file to get the raw homologous structures
- homo_ensemble: Please unzip the compressed file to get the aligned snapshots from homology

PCSL_Output:
- MD_chat_MD_res: Inter-residue spring constants from MD $\hat{\text{c}}$ with positional fluctuation restraints from MD ensemble
- homo_chat_homo_res: Inter-residue spring constants from homologous $\hat{\text{c}}$ with positional fluctuation restraints from homologous ensemble
- MD_chat_homo_res: Inter-residue spring constants from MD $\hat{\text{c}}$ with positional fluctuation restraints from homologous ensemble
- MD_chat_Xray_res: Inter-residue spring constants from MD $\hat{\text{c}}$ with positional fluctuation restraints from Xray

PCSL:
- homologs_collection.py: Utilities to collect raw homologous structures
- PCSL.py: Codes for reading outputs of PCSL


## Installation:

Installation of required packages for processing ensemble from all-atom MD and homology:

conda install python=3.6 prody=2.2.0 mdanalysis==2.0.0

## Prerequisites:

Tools for processing ensemble from all-atom MD and homology:

* CD_HIT v4.8.1 (https://sites.google.com/view/cd-hit?pli=1)
* MUSCLE v5.1 (https://www.drive5.com/muscle/)
* THESEUS v3.3.0 (https://theobald.brandeis.edu/theseus/)

## Release History

* version 1
    * First Release (academic publication)


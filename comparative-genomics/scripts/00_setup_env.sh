#!/bin/bash
# 00_setup_env.sh — one-time toolchain setup via conda/mamba on the HPC.
# If your cluster uses modules instead, load equivalents and skip this.
set -euo pipefail
ENV=${1:-primate-selection}
mamba create -y -n "$ENV" -c bioconda -c conda-forge \
    ncbi-datasets-cli miniprot gffread seqkit samtools \
    mafft hyphy "python>=3.10" biopython dendropy || \
conda create -y -n "$ENV" -c bioconda -c conda-forge \
    ncbi-datasets-cli miniprot gffread seqkit samtools \
    mafft hyphy "python>=3.10" biopython dendropy
echo "conda activate $ENV   # then run 01_ -> 02_ -> 03_"

#!/bin/bash
###############################################################################
# 01_fetch_and_extract.sh
# Download target primate genomes from NCBI and extract per-gene CDS.
#   - annotated assemblies  -> pull CDS directly from the annotation
#   - unannotated assemblies-> miniprot(reference_proteins.faa -> genome) -> CDS
#
# Inputs (in this bundle):
#   refs/reference_proteins.faa   query proteins (80 genes x up to 3 ref species)
#   $ACC_CSV                      accession list (species,chosen_accession,...)
# Output:
#   cds/<gene>/<species>.cds.fna  one CDS per gene per species (nucleotide)
#   logs/extract.log
#
# Tools required on PATH: datasets (NCBI), miniprot, gffread, seqkit, samtools
# Usage:  bash 01_fetch_and_extract.sh accessions_gibbon_flagship.csv
###############################################################################
set -euo pipefail
ACC_CSV="${1:-accessions_gibbon_flagship.csv}"
THREADS="${THREADS:-8}"
REF=refs/reference_proteins.faa
mkdir -p genomes cds logs annot
LOG=logs/extract.log; : > "$LOG"

# gene list (from reference fasta headers: >GENE|species)
GENES=$(grep '^>' "$REF" | sed 's/^>//; s/|.*//' | sort -u)

# species-safe filename
safe(){ echo "$1" | tr ' ' '_' ; }

tail -n +2 "$ACC_CSV" | while IFS=, read -r species acc level annotated dichro family path; do
  sp=$(safe "$species"); echo "=== $sp ($acc, annotated=$annotated) ===" | tee -a "$LOG"
  # ---- download ----
  if [ ! -f "genomes/${acc}.zip" ]; then
    datasets download genome accession "$acc" \
       --include genome,protein,cds,gff3 --filename "genomes/${acc}.zip" 2>>"$LOG" || {
       echo "  DOWNLOAD FAILED $acc" | tee -a "$LOG"; continue; }
  fi
  rm -rf "genomes/${acc}_x"; mkdir -p "genomes/${acc}_x"
  unzip -oq "genomes/${acc}.zip" -d "genomes/${acc}_x" 2>>"$LOG" || true
  DATADIR="genomes/${acc}_x/ncbi_dataset/data/${acc}"

  if [ "$annotated" = "True" ] && ls "$DATADIR"/cds_from_genomic.fna >/dev/null 2>&1; then
    # ---- direct: grab CDS whose gene= matches our panel ----
    CDSFILE="$DATADIR/cds_from_genomic.fna"
    for g in $GENES; do
      # match [gene=G] token, take the longest transcript
      seqkit grep -nrp "\[gene=${g}\]" "$CDSFILE" 2>/dev/null \
        | seqkit sort -l -r 2>/dev/null | seqkit head -n 1 2>/dev/null \
        > "cds/${g}.__tmp.fna" || true
      if [ -s "cds/${g}.__tmp.fna" ]; then
        mkdir -p "cds/${g}"
        awk -v s=">$sp" 'NR==1{print s} NR>1{print}' "cds/${g}.__tmp.fna" > "cds/${g}/${sp}.cds.fna"
      fi
      rm -f "cds/${g}.__tmp.fna"
    done
  else
    # ---- miniprot: align reference proteins to the genome, emit GFF, extract CDS ----
    GENOME=$(ls "$DATADIR"/*.fna 2>/dev/null | head -1)
    [ -z "$GENOME" ] && { echo "  NO GENOME FASTA $acc" | tee -a "$LOG"; continue; }
    miniprot -t "$THREADS" --gff "$GENOME" "$REF" > "annot/${sp}.miniprot.gff" 2>>"$LOG" || {
       echo "  MINIPROT FAILED $sp" | tee -a "$LOG"; continue; }
    # best hit per gene: parse mRNA lines, keep top-scoring per gene label
    python3 extract_miniprot_cds.py \
        --gff "annot/${sp}.miniprot.gff" --genome "$GENOME" \
        --species "$sp" --genes "$REF" --outdir cds 2>>"$LOG" || \
        echo "  EXTRACT FAILED $sp" | tee -a "$LOG"
  fi
done
echo "DONE. CDS in cds/<gene>/<species>.cds.fna" | tee -a "$LOG"

#!/bin/bash
# fetch_ref_proteins.sh GENES.txt  ->  refs/reference_proteins_new.faa  (headers ">GENE|human")
# Run on a LOGIN node (needs internet). NCBI datasets, human (taxon 9606), longest isoform per gene.
set -uo pipefail
export PATH=/scratch/tlasisi_root/tlasisi0/tlasisi/envs/align/bin:$PATH
GENES_FILE="${1:?usage: fetch_ref_proteins.sh genes.txt}"
W=/scratch/tlasisi_root/tlasisi0/tlasisi/pgn_run117
cd "$W"; mkdir -p refs tmp_prot
OUT="${OUT:-refs/reference_proteins_new.faa}"; : > "$OUT"
MISSING=""
while read -r g; do
  g=$(echo "$g" | tr -d '[:space:]'); [ -z "$g" ] && continue
  rm -rf "tmp_prot/$g"; mkdir -p "tmp_prot/$g"
  if datasets download gene symbol "$g" --taxon 9606 --include protein --filename "tmp_prot/$g/p.zip" >/dev/null 2>&1; then
    unzip -oq "tmp_prot/$g/p.zip" -d "tmp_prot/$g/x" 2>/dev/null || true
    FAA=$(ls "tmp_prot/$g/x/ncbi_dataset/data/protein.faa" 2>/dev/null | head -1)
    if [ -s "$FAA" ]; then
      seqkit sort -l -r "$FAA" 2>/dev/null | seqkit head -n 1 2>/dev/null \
        | awk -v g="$g" 'NR==1{print ">"g"|human"} NR>1{print}' >> "$OUT"
      echo "  $g OK ($(seqkit sort -l -r "$FAA" 2>/dev/null | seqkit head -n 1 2>/dev/null | seqkit stats -T 2>/dev/null | awk 'NR==2{print $5" aa"}'))"
    else MISSING="$MISSING $g"; echo "  $g -- NO PROTEIN in download"; fi
  else MISSING="$MISSING $g"; echo "  $g -- DOWNLOAD FAILED"; fi
  rm -rf "tmp_prot/$g"
done < "$GENES_FILE"
echo "wrote $(grep -c '^>' "$OUT") proteins -> $OUT"
[ -n "$MISSING" ] && echo "MISSING (need manual ref):$MISSING" || echo "all genes resolved"

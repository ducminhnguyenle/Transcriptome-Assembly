# TRANSCRIPTOME ASSEMBLY PRACTICE

---

- [TRANSCRIPTOME ASSEMBLY PRACTICE](#transcriptome-assembly-practice)
  - [Tools](#tools)
  - [Conda/Miniconda installation](#condaminiconda-installation)
  - [Mapping-based assembly method](#mapping-based-assembly-method)
  - [De novo assembly](#de-novo-assembly)

This tutorial demonstrates how to perform a simple transcriptome assembly based on 2 methods:

- Mapping-based assembly  
- De-novo assembly

## Tools

In this practical transcriptome assembly, these tools are utilized for simple and easy implementation.

| Tools     | Usage | Github |
| :---: | :----: | :---: |
| **Hisat2**    | Building an index</br>Alignment | <https://github.com/DaehwanKimLab/hisat2> |
| **Samtools** | Manipulating bam file | <https://github.com/samtools/samtools> |
| **Cufflinks** | Assemble transcript</br>Estimate abundances | <https://github.com/cole-trapnell-lab/cufflinks> |
| **Velvet** | Short read de novo assembler</br>using de Bruijn graphs | <https://github.com/dzerbino/velvet> |
| **Oases** | De novo transcriptome assembler</br>for short reads | <https://github.com/dzerbino/oases/> |

## Conda/Miniconda installation

Every tools and their dependencies that are required in this tutorial will be installed through [Conda/Miniconda](https://docs.conda.io/en/latest/).

Please use this [environment.yml](./environment.yml) file which includes all the tools needed for this practice.

Using this conda command line to generate necessary [Conda/Miniconda](https://docs.conda.io/en/latest/) evnvironment:

```bash
conda env create -f environment.yml
```

If everything is installed correctly, one can check if `rna_assembly` conda environment exists.

```bash
conda env list
```

Please activate `rna_assembly` environment before any further steps.

```bash
conda activate rna_assembly
```

## Mapping-based assembly method

1. Building an index using HISAT2

    ```bash
    hisat2-build ref.fa ref
    ```

2. Mapping paired-end reads with reference genome

    ```bash
    hisat2 \
        -x ref \
        -1 sample_R1.fastq.gz \
        -2 sample_R2.fastq.gz \
        -S sample.sam
    ```

3. Converting to bam format and sorting by coordinates

    ```bash
    samtools view -Sb sample.sam > sample.bam
    samtools sort sample.bam -o sample.sorted.bam
    ```

4. Reconstruct full-length transcript sequences based on RNA-seq read mapping using Cufflinks

    ```bash
    cufflinks \
        -p 8 \
        --library-type fr-firststrand \
        -G "/path/to/*.gtf" \
        -o "/path/to/outdir/" "sample.sorted.bam"
    ```

Output of Cufflinks is given in BED or GTF format which contains the transcript coordinates in a reference sequence.

## De novo assembly

1. Interleave paired-end reads (forward + reverse)

    ```python
    python3 interleave_fastq.py -f "/path/to/sample_R1.fastq" -r "/path/to/sample_R2.fastq" -o "/path/to/outFile"
    ```

    OR

    ```bash
    paste <(cat "/path/to/sample_R1.fastq") <(cat "/path/to/sample_R2.fastq") | paste - - - - | awk 'BEGIN{FS="\t"; OFS="\n"}; {print $1,$3,$5,$7,$2,$4,$6,$8}' > "sample_interleaved.fastq"
    ```

2. Define k-mer length and the output dir (e.g., k-mer=25, outdir="vdir")

    ```bash
    velveth vdir 25 -fastq -shortPaired sample_interleaved.fastq
    ```

3. Graph traversal and contig extraction, insert size is 200 ( One can specify insert size based on your interest and data)

    ```bash
    velvetg vdir -ins_length 200 -read_trkg yes
    ```

4. Oases is applied to the resulting de Bruijn graph

    ```bash
    oases vdir -ins_length 200 -min_trans_lgth 200
    ```

5. Running several assemblies with different k-mer lengths and merge th assemblies

    ```bash
    oases_pipeline.py \
        -m 25 -M 31 \
        -o output_denovo/pairedEnd \
        -d ' -fastq -shortPaired sample_interleaved.fastq ' \
        -p ' -ins_length 200 -min_trans_lgth 200 '
    ```

Output directory vdir contains the transcript sequences which are stored in FASTA file `transcript.fa`. The name of each FASTA entry describes the locus and isoforms. Another file produced by Oases is `contig-ordering.txt`.

An example of a FASTA entry name is `Locus_10_Transcript_1/3_Confidence_0.571_Length_3815.`

- It indicates that there are three transcripts from locus 10, and this is the first of them.
- The confidence value is a number between 0 and 1 (the higher the better), and length is the transcript length in base pairs.

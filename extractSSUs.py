#!/usr/bin/env python

import os
import subprocess
import io

directory = os.path.basename(os.getcwd())

gff_filename = directory + '_Rfam.gff'
fasta_filename = directory + '_contigs.fasta'

response = subprocess.run("grep SSU " + gff_filename + "|" + 
                        "awk '{if($6 >= 1000) print}'", 
                        stdout = subprocess.PIPE, 
                        shell = True, env = dict(os.environ), encoding='utf-8')
output = io.StringIO(response.stdout)

for line in output:
    line = line.split()
    if line[6] == '+':
        subprocess.run(f'samtools faidx {fasta_filename} \
                        {line[0]}:{line[3]}-{line[4]} | seqtk seq -l 0',
                        shell = True, env = dict(os.environ), encoding='utf-8')
    elif line[6] == '-':
        subprocess.run(f'samtools faidx {fasta_filename} \
                        {line[0]}:{line[3]}-{line[4]} | seqtk seq -r',
                        shell = True, env = dict(os.environ), encoding='utf-8')
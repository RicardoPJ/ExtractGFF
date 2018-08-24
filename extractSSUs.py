#!/usr/bin/env python

import argparse
import os
import subprocess
import io

try:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("directory", type = str, help = "directory where the files are")
    arg_parser.add_argument("pattern", type = str, help = "pattern to look for")
    arg_parser.add_argument("score", type = int, help = "score threshold")
    arguments = arg_parser.parse_args()

    directory = os.path.basename(os.path.realpath(arguments.directory))
    pattern = arguments.pattern
    score = arguments.score

    print(directory, pattern, score)

    directory = os.path.basename(os.getcwd())

    os.chdir(directory)

    gff_filename = directory + '_Rfam.gff'
    fasta_filename = directory + '_contigs.fasta'

    response = subprocess.run(f"grep {pattern} " + gff_filename + "|" +
                              f"awk '{{if($6 >= {score}) print}}'",
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

    os.chdir("..")
except KeyboardInterrupt:
    pass

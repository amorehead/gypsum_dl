#!/usr/bin/env python

# Copyright 2018 Jacob D. Durrant
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Gypsum is a conversion script to transform smiles strings and 2D SDFs into 3D
models.
"""

import argparse
import copy
from gypsum.Start import prepare_molecules
from gypsum.Test.Tester import run_test
from gypsum import Utils

PARSER = argparse.ArgumentParser()


PARSER.add_argument('--json', '-j', metavar='param.json',
                    help='Name of a json file containing all parameters. \
                    Overrides all other arguments specified at the commandline.')
PARSER.add_argument('--source', '-s', metavar='input.smi',
                    help='Name of the source file (e.g., input.smi).')
PARSER.add_argument('--output_folder', '-o',
                    help='The path to an existing folder where the gypsum ' +
                    'output file(s) will be saved.')
PARSER.add_argument('--num_processors', '-p', metavar='N', default=1,
                    help='Number of processors to use for parallel \
                    calculations.')
PARSER.add_argument('--min_ph', metavar='MIN', type=float,
                    help='Minimum pH to consider.')
PARSER.add_argument('--max_ph', metavar='MAX', type=float,
                    help='Maximum pH to consider.')
PARSER.add_argument('--ph_std_dev', metavar='D', type=float,
                    help='Size of pH substructure ranges. See Dimorphite-DL \
                    publication for details.')
PARSER.add_argument('--thoroughness', '-t',
                    help='How widely to search for low-energy conformers. \
                    Larger values increase run times but can produce better \
                    results.')
PARSER.add_argument('--max_variants_per_compound', '-m', type=int, metavar='V',
                    help='The maximum number of variants to create per input \
                    molecule.')
PARSER.add_argument('--separate_output_files', action='store_true',
                    help='Indicates that the outputs should be split between \
                    files. If true, each output .sdf file will correspond to a \
                    single input file, but different 3D conformers will still \
                    be stored in the same file.')
PARSER.add_argument('--add_pdb_output', action='store_true',
                    help='Indicates that the outputs should also be written in \
                    the .pdb format. Creates one PDB file for each molecular \
                    variant.')
PARSER.add_argument('--add_html_output', action='store_true',
                    help='Indicates that the outputs should also be written in \
                    the .html format, for debugging. Attempts to open a \
                    browser for viewing.')
PARSER.add_argument('--skip_optimize_geometry', action='store_true',
                    help='Skips the optimization step.')
PARSER.add_argument('--skip_alternate_ring_conformations', action='store_true',
                    help='Skips the non-aromatic ring-conformation \
                    generation step.')
PARSER.add_argument('--skip_adding_hydrogen', action='store_true',
                    help='Skips the ionization step.')
PARSER.add_argument('--skip_making_tautomers', action='store_true',
                    help='Skips tautomer-generation step.')
PARSER.add_argument('--skip_ennumerate_chiral_mol', action='store_true',
                    help='Skips the ennumeration of unspecified chiral \
                    centers.')
PARSER.add_argument('--skip_ennumerate_double_bonds', action='store_true',
                    help='Skips the ennumeration of double bonds.')
PARSER.add_argument('--2d_output_only', action='store_true',
                    help='Skips the generate-3D-models step.')
PARSER.add_argument('--multithread_mode', default='multithreading',
                    choices = ["mpi", "multithreading", "serial"],
                    help='Determine what style of multithreading to use: mpi, \
                    multithreading, or serial. If this program is being used \
                    by a program in MPI mode, we recommend setting this to \
                    serial. Serial will override the num_processors flag, \
                    forcing it to be one.')
PARSER.add_argument('--cache_prerun', '-c', action='store_true',
                    help='Run this before running gypsum in mpi mode.')
PARSER.add_argument('--test', action='store_true',
                    help='Tests gypsum to check for programming bugs.')

ARGS_DICT = vars(PARSER.parse_args())
if ARGS_DICT["test"] == True:
    run_test()
elif ARGS_DICT["cache_prerun"] == False:

    INPUTS = copy.deepcopy(ARGS_DICT)

    for k, v in ARGS_DICT.items():
        if v is None:
            del INPUTS[k]

    prepare_molecules(INPUTS)
    Utils.log("Finished Gypsum")
else:
    pass

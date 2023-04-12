#!/usr/bin/env python
# Usage:
# $ python mode2xyz.py mode012.xyz

from ase.io import read, write
import numpy as np
import sys

try:
    fn_modexyz = sys.argv[1]
    fn_poscar = 'POSCAR'
    modexyz = read(fn_modexyz, index=':')
    poscar = read('POSCAR')
except:
    print('''Please provide the filename of the modeXXX.xyz
and make sure the POSCAR is in the current directory.
Example:
$ python mode2xyz.py mode012.xyz''')
    exit()

for i in modexyz:
    i.set_cell(poscar.get_cell())

basename = fn_modexyz.split('.')[0]
write(f'{basename}.gif', modexyz, interval=2)


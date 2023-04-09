#!/usr/bin/env python
# Usage:
# $ python dispmake_indices.py POSCAR 38,39,40,44,45,46,48,49,50,51 0.001

import ase.io
import sys

try:
    fn_poscar = sys.argv[1]
    indices = [int(item) for item in sys.argv[2].split(',')]
    disp = eval(sys.argv[3])
except:
    print('''Please provide all following inputs:
[VASP-format structure filename]
[list of indices to displace, separated by ,]
[displacement, in Angstrom]
Example:
$ python dispmake_indices.py POSCAR 38,39,40,44,45,46,48,49,50,51 0.001''')
    exit()

print(f'Structure file: {fn_poscar}')
print(f'Atoms to displace: {indices}')
print(f'Displacement: {disp} A')
print(f'Total #displacements: {len(indices)*3}')
print(f'Set \"NSW={len(indices)*3+1}\" in INCAR!')

atoms = ase.io.read(fn_poscar)

with open('DISPLACECAR', 'w') as f:
    pos = atoms.get_positions()
    ele = atoms.get_chemical_symbols()
    for i in range(len(atoms)):
        if i in indices:
            f.write(f'{disp}  {disp}  {disp}  {i}  {ele[i]}\n')
        else:
            f.write(f'0  0  0  {i}  {ele[i]}\n')





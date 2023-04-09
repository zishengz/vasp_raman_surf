#!/usr/bin/env python
# Usage:
# $ python dispmake_height.py POSCAR 14 0.001

import ase.io
import sys

try:
    fn_poscar = sys.argv[1]
    height = eval(sys.argv[2])
    disp = eval(sys.argv[3])
except:
    print('''Please provide all following inputs:
[VASP-format structure filename]
[height beyond which all atoms will be displaced]
[displacement, in Angstrom]
Example:
$ python dispmake_height.py POSCAR 14 0.001''')
    exit()

print(f'Structure file: {fn_poscar}')
print(f'Atoms to displace: lower than {height} A')
print(f'Displacement: {disp} A')

atoms = ase.io.read(fn_poscar)
atoms_disp = [a for a in atoms if a.position[2]>height]

print(f'Total #displacements: {len(atoms_disp)*3}')
print(f'Set \"NSW={len(atoms_disp)*3+1}\" in INCAR!')

with open('DISPLACECAR', 'w') as f:
    pos = atoms.get_positions()
    ele = atoms.get_chemical_symbols()
    for i in range(len(atoms)):
        if pos[i][2] > height:
            f.write(f'{disp}  {disp}  {disp}  {i}  {ele[i]}\n')
        else:
            f.write(f'0  0  0  {i}  {ele[i]}\n')





# vasp_raman_surf

A set of scripts for flexible Raman off-resonant activity calculation for surface slabs, using VASP as a DFT back-end.

**Features:**

- Selecting specific atoms to include in the frequancy calculation and Raman simulation without needing to include all atoms!

- Finding and picking specific vibrational modes of interest for Raman calculation.

(Adapted from [raman-sc/VASP](https://github.com/raman-sc/VASP) and [VTSTscripts](https://theory.cm.utexas.edu/vtsttools/scripts.html)

## Installation

Firstly, make sure you have a Python 3.7+ environment with [ASE](https://wiki.fysik.dtu.dk/ase/install.html) installed.

You will also need to have your VASP compiled with [VTSTTools](https://theory.cm.utexas.edu/vtsttools/installation.html) add-on, and with [VTSTscripts](https://theory.cm.utexas.edu/vtsttools/scripts.html) installed.

After installing the dependencies, you can clone the repo to your local directory by:

```shell
git clone https://github.com/zishengz/vasp_raman_surf.git
```

After fetching the `vasp_raman_surf` repo, grant all scripts executing permission:

```bash
chmod +x ./*.py
```

and then add the directory to your `PATH` by:

```shell
export PATH=$PATH:`pwd`/vasp_raman_surf/
```

Remember to add this export line to your `~/.bashrc` or the submission script, so that the scripts are accessible globally.

You need to use the absolute path (you can check it by running `pwd` in Bash shell) for this purpose.

## Usage

There are three `INCAR` files for different purposes:

- `INCAR-opt` is for local optimization of the geometry to a local minimum

- `INCAR-freq` is for finite-difference calculation of vibrational modes and frequencies

- `INCAR-raman` is for calculation of Raman off-resonant activity.

Make sure you modify the INCAR according to your system's setting and do not mix them up!

### Local optimization

Firstly, make three subdirectories to prevent ovewritting files:

```bash
mkdir opt freq raman
cd opt
```

Prepare the `POSCAR`, `INCAR`, `KPOINTS`, and `POTCAR` for your system, and submit the job!

Make sure you are using a `EDIFFG` of at least -0.01 in `INCAR`, to ensure that the system can relax to the local minimum.

### Frequancy calculation

After the local optimization converges, copy the final structure and the pseudopotential file to the subdirectory of frequency calculation:

```bash
cd ../freq
cp ../opt/CONTCAR POSCAR
cp ../opt/POTCAR KPOINTS .
```

Then, you can generate the `DISPLACECAR` using one of the `dispmake_xx.py` scripts.

`dispmake_height.py` can select all atoms above a certain height (Z coordinate) for displacements in X/Y/Z directions:

```bash
$ dispmake_height.py POSCAR 14 0.001
Structure file: POSCAR
Atoms to displace: lower than 14 A
Displacement: 0.001 A
Total #displacements: 48
Set "NSW=49" in INCAR!
```

`dispmake_height.py` can select specific atoms by indices (starting from 0!):

```bash
$ dispmake_indices.py POSCAR 38,39,40,44,45,46,48,49,50,51 0.001
Structure file: POSCAR
Atoms to displace: [38, 39, 40, 44, 45, 46, 48, 49, 50, 51]
Displacement: 0.001 A
Total #displacements: 30
Set "NSW=31" in INCAR!
```

After generating the displacements, edit the `NSW` in `INCAR` according to the output.

Modify the `KPOINTS` and other settings in `INCAR`, and then submit the job!

### Selecting modes

After the frequancy calculation completes, compute all modes and write the Raman-needed files by:

```bash
$ dymmatrix_surf.py
```

You can generate .XYZ movies of each mode for visualization by:

```bash
$ dymmodes2xyz.pl
```

You can also pick modes according to a few frequencies of interest and within a tolerance range:

```bash
$ python ../locate_modes.py freq.dat 200,940 50
mode #15 (154.5 cm-1) is near peak at 200.0 cm-1!
mode #16 (189.3 cm-1) is near peak at 200.0 cm-1!
mode #17 (197.3 cm-1) is near peak at 200.0 cm-1!
mode #18 (200.0 cm-1) is near peak at 200.0 cm-1!
mode #22 (914.8 cm-1) is near peak at 940.0 cm-1!
mode #23 (927.1 cm-1) is near peak at 940.0 cm-1!
mode #24 (986.4 cm-1) is near peak at 940.0 cm-1!
All frequencies in the range of interest:
15,16,17,18,22,23,24
```

### Raman simulation

After deciding on the modes of interest, we can proceed to the Raman simulation! Firstly, copy the needed files to the Raman subdirectory:

```bash
cp *.dat POTCAR KPOINTS ../raman
cp CONTCAR ../raman/POSCAR.phon
cd ../raman
```

Remember to modify the `INCAR-raman` and use it as the `INCAR`! 

In the submission script `vasp_raman.sh`, modify the environment-related lines. The line for Raman simulation is:

```bash
python -u vasp_raman_surf.py 15,16,17,18,22,23,24 0.01
```

Here the 2nd argument is the number of modes (starting from 1!) separated by `,` and the 3rd argument is the displacement in Angstrom.

And then you can submit the job and have some coffee! If the job times out, you can directly resubmit the job without changing anything, as it willfigure out the unfinished subtasks internally.

The results will be written to `vasp_raman.dat`:

```bash
# mode    freq(cm-1)    alpha    beta2    activity
015   154.48643  -116574.2670975  781290191500.5076904  6080561529222.4189453
016   189.31074  -63507.6738502  161451552342.6597900  1311655975102.7124023
017   197.31355  -563241.3837649  3052998388916.0776367  35646827259755.2890625
018   199.98279  134982.8422441  270614106923.9118347  2714215294981.2832031
... ...
```

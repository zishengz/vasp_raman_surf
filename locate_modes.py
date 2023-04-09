#!/usr/bin/env python
# Usage:
# $ python locate_modes.py freq.dat 200,940 50


import sys

try:
    fn_freq = sys.argv[1]
    list_freq = [float(i) for i in sys.argv[2].split(',')]
    freq_range = float(sys.argv[3])
except:
    print('''Please provide all following inputs:
[freq.dat filename]
[list of frequancies of interest, separated by ,]
[tolerance range of frequancy around each freq of interest]
Example:
$ python locate_mode.py freq.dat 200,940 50''')
    exit()

freq = open('freq.dat').readlines()

list_myfreq = []
for f in freq:
    f_split = f.split()
    if f_split[-1] == '1':
        continue
    for l in list_freq:
        myfreq = eval(f_split[0])
        if myfreq > l - freq_range and myfreq < l + freq_range:
            print(f'mode #{freq.index(f)+1} ({myfreq:.1f} cm-1) is near peak at {l} cm-1!')
            list_myfreq.append(freq.index(f)+1)
            break

print('All frequencies in the range of interest:')
print(','.join([str(i) for i in list_myfreq]))



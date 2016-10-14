#coding=gbk

import os
import sys

if len(sys.argv) >= 2:
    c_Target = sys.argv[1]
else:
    #c_Target = 'src.cleaner\Filter.py'
    c_Target = 'Stat2.py'

c_Target_abs = os.path.join(os.getcwd(), c_Target)
c_Key = os.path.basename(c_Target)[:-3]
c_Py2exeDir = '[py2exe]\%s' % (c_Key)
c_SetupPy = 'setup.py'
c_Exe = '%s\dist\%s.exe' % (c_Py2exeDir, c_Key)

if not os.path.exists(c_Py2exeDir):
    os.makedirs(c_Py2exeDir)

with open(os.path.join(c_Py2exeDir, c_SetupPy), 'w') as fout:
    print >>fout, 'from distutils.core import setup'
    print >>fout, 'import py2exe'
    print >>fout, 'setup(console=["%s"])' % c_Target_abs

os.system('cd %s && python %s py2exe' % (c_Py2exeDir, c_SetupPy))
os.system(c_Exe)

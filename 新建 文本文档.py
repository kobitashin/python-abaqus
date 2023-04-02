# coding=utf-8
import sys
import os
import stat
import numpy as np
from abaqus import *
from abaqusConstants import *
from odbAccess import *
#a=getInput('Please enter the file path:')
#os.chdir(a)
x=getInput('OdbName Please:')
odb =openOdb(x+'.odb')
y=odb.steps.keys()
Step= odb.steps[y[1]] #分析步需要注意
r1=Step.frames
ra=len(r1)
f=open("Frequency.txt","w")
for i in range(ra):
    #A1=np.empty([ra,1],dtype=float)
    A1=r1[i].frequency
    AA=A1*2*pi*0.00324619777586024
    f.writelines(str(AA)+"\n")
f.close()
odb.close
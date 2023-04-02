# coding=utf-8
# 功能梯度材料参数化建立多层材料属性
import sys
import os
import stat
import numpy as np
from abaqus import *
from abaqusConstants import *
import material
import __main__
import section
#h=getInput('Thickness:')
h=float(0.2) # 总厚度
#a=getInput('layer number:')
aa=int(10) #层数
a=float(10)
#Em=getInput('Elastic moldule:')
Em=float(70E9) #弹性模量
#roum=getInput('Densty:')
roum=float(2702) #密度
#e=getInput('Porous coefficients:')
e=float(0.2) #孔隙率
#t=getInput('Porou type:')
t=2 #分布形式
#um=getInput('Possion ratio:')
um=float(0.3) #泊松比
em=1-sqrt(1-e)
z=[(2/a*n-(a+2)/a)*(h/2) for n in range(1,aa+1+1,1)]
ra=len(z)
layup=[]
for i in range(ra):
    if t==1:
        Ez=Em*(1-e*cos(pi*z[i]/h))
        rou=roum*(1-em*cos(pi*z[i]/h))
    else:
        Ez=Em*(1-e*cos(pi*z[i]/(h*2)+pi/4))
        rou=roum*(1-em*cos(pi*z[i]/(h*2)+pi/4))
    m=mdb.models['Model-1'].Material('M'+str(i))
    m.Elastic(table=((Ez,um),))
    m.Density(table=((rou,),))
    sectionLayer=section.SectionLayer(material='M'+str(i),thickness=h/(a+1),
                                      orientAngle=0,numIntPts=3,plyName='')
    layup.append(sectionLayer)
mdb.models['Model-1'].CompositeShellSection(name='Section-C', 
        preIntegrate=OFF, idealization=NO_IDEALIZATION, symmetric=False, 
        thicknessType=UNIFORM, poissonDefinition=DEFAULT, 
        thicknessModulus=None, temperature=GRADIENT, useDensity=OFF, 
        integrationRule=SIMPSON, layup=layup)

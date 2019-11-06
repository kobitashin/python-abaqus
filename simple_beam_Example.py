#!/user/bin/python
# -* - coding:utf-8 -*-

# 文件名：simple_beam_Example.py

# 运行该脚本将自动实现悬臂梁在压力荷载作用下的建模、提交分析和后处理
# 等各方面的操作。

from abaqus import *
import testUtils
testUtils.setBackwardCompatibility()
from abaqusConstants import *

# 写欢迎语
print('亲爱的读者朋友，很高兴认识大家！')
print('下面通过最熟悉的简单实例，带领大家进入Python编程的奇妙世界！')

# 建立模型
myModel = mdb.Model(name='Beam')

# 创建新视口来显示模型和分析结果。
myViewport = session.Viewport(name='Cantilever Beam Example',
    origin=(20, 20), width=150, height=120)
    
# 导入part模块。
import part

# 创建基础特征的草图。
mySketch = myModel.ConstrainedSketch(name='beamProfile',sheetSize=250.)

# 绘制矩形截面。
mySketch.rectangle(point1=(-100,10), point2=(100,-10))

# 创建三维变形体部件。
myBeam = myModel.Part(name='Beam', dimensionality=THREE_D,
         type=DEFORMABLE_BODY)

# 通过对草图拉伸25.0来创建部件。
myBeam.BaseSolidExtrude(sketch=mySketch, depth=25.0)

# 导入material模块。
import material

# 创建材料。
mySteel = myModel.Material(name='Steel')

# 定义弹性材料属性，杨氏模量为209.E3，泊松比为0.3。
elasticProperties = (209.E3, 0.3)
mySteel.Elastic(table=(elasticProperties, ) )

# 导入section模块。
import section

# 创建实体截面。
mySection = myModel.HomogeneousSolidSection(name='beamSection',
    material='Steel', thickness=1.0)

# 为部件分配截面属性。
region = (myBeam.cells,)
myBeam.SectionAssignment(region=region,sectionName='beamSection')

# 导入assembly模块。
import assembly

# 创建部件实例。
myAssembly = myModel.rootAssembly
myInstance = myAssembly.Instance(name='beamInstance',part=myBeam, dependent=OFF)

# 导入step模块。
import step

# 在初始分析步Initial之后创建一个分析步。静力分析步的时间为1.0，初始增量为0.1。
myModel.StaticStep(name='beamLoad', previous='Initial', timePeriod=1.0,
   initialInc=0.1,description='Load the top of the beam.')

# 导入load模块。
import load

# 通过坐标找出端部所在面。
endFaceCenter = (-100,0,12.5)
endFace = myInstance.faces.findAt((endFaceCenter,) )

# 在梁端部创建固定端约束。
endRegion = (endFace,)
myModel.EncastreBC(name='Fixed',createStepName='beamLoad',region=endRegion)

# 通过坐标找到上表面。
topFaceCenter = (0,10,12.5)
topFace = myInstance.faces.findAt((topFaceCenter,) )

# 在梁的上表面施加压力荷载。
topSurface = ((topFace, SIDE1), )
myModel.Pressure(name='Pressure', createStepName='beamLoad',
    region=topSurface, magnitude=0.5)

# 导入mesh模块。
import mesh

# 为部件实例指定单元类型。
region = (myInstance.cells,)
elemType = mesh.ElemType(elemCode=C3D8I, elemLibrary=STANDARD)
myAssembly.setElementType(regions=region, elemTypes=(elemType,))

# 为部件实例撒种子。
myAssembly.seedPartInstance(regions=(myInstance,), size=10.0)

# 为部件实例划分网格。
myAssembly.generateMesh(regions=(myInstance,))

# 显示划分网格后的梁模型。
myViewport.assemblyDisplay.setValues(mesh=ON)
myViewport.assemblyDisplay.meshOptions.setValues(meshTechnique=ON)
myViewport.setValues(displayedObject=myAssembly)

# 导入job模块。
import job

# 为模型创建并提交分析作业。
jobName = 'beam_tutorial'
myJob = mdb.Job(name=jobName, model='Beam',description='Cantilever beam tutorial')

# 等待分析作业完成。
myJob.submit()
myJob.waitForCompletion()
print('分析已顺利完成，下面进行后处理。')

# 导入visualization模块。
import visualization

# 打开输出数据库，显示默认的等值线图。
myOdb = visualization.openOdb(path=jobName + '.odb')
myViewport.setValues(displayedObject=myOdb)
myViewport.odbDisplay.display.setValues(plotState=CONTOURS_ON_DEF)
myViewport.odbDisplay.commonOptions.setValues(renderStyle=FILLED)

# 将Mises等值线图输出为PNG格式的文件。
session.printToFile(fileName='Mises', format=PNG,  canvasObjects=(myViewport,))
print('文件Mises.png保存于工作目录下，请查看！')
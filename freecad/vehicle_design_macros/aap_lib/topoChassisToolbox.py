# -*- coding: utf-8 -*-
#***************************************************************************
#*  Deferred for future development
#*See:  Need ot merge techique with 
#*https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/a-template-for-python-toolboxes.htm
#*until then live with topoChassisCabin.py and topoChassisFrame.py
#*   Copyright (c) 1989- 2025 Abbott Analytical Products   <http://abbottanp.com/>*
#*                                                                               *
#* This program module provides support: utilities and common declarations used 
#*     by various other macro modules related directly to the development of the 
#*     the basic chassis components exo cage in roll-out ready state (less defined 
#*     steering and suspension system) to use for prototyping the invisioned 
#*     Abiriba_RG  GM EV vehicle detailed at: 
#*     https://abbottanp.com/artifacts/gm_vehicle_WB/index.html.
"""
#* Helpful references/hints:
Packaging and distributing projects
    https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
    Install build package
        python3 -m pip install build
    Install project in editable/development mode state
        python3 -m pip install -e aap_lib

    Create SOurce Distribution source 
        python3 -m build --sdist

Develop:   Modify topoChassisToolbox.  Reload for FC
             reload a topoChassisToolbox.py module called by macro

Block Copy these five lines to FC Python Console  and insue they are executed
import aap_lib 
from importlib import reload
reload (aap_lib)
from aap_lib import aapfunctions, topoChassisToolbox

Adapt macro of interest to use the modified toolbox
Move the toolbox to the aaplibrary/app_lib folder to test/build
Test:	python setup.py pytest
Build: 	python setup.py bdist_wheel fron the ~*/Macro/aap_library folder
--OR--
Install: pip install /path/to/wheelfile.whl
Actual build to dist/
    ~/.local/share/FreeCAD/Macro/aap_library$ python setup.py bdist_wheel
    Yields aap_lib-0.1.0-py3-none-any.whl archive for extracting aap_lib
    Extract from aap_lib*.whl archive file into the aap_lib folder and aap_lib*dist-info folder
Deploy: 
    1> backup */FreeCAD/Macro/aap_lib
    2> copy contents of aaplibrary/dist/aap_lib folder to FC Macro location
    3> test the aapfunctions.haversine()
    4> test topoChassisToolbox content

*************
Hisory
250123_lu Retruned to the toMM(value * 25.4 *SF) used previsously by topoChaasisFrame.py and 
				topoChassisCabin.  The toolbox will set the SF on call from this object.
250121_lu Ran with topoChassis_003_strutBuildGM_vehicle_999_CabinChassis_Part.FCMacro successfully
	    producing the cabin strut pair.
250116_lu see bottom example at https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
                using "With super first in each method" by Overall <by Zags> for lost linkage of self and using super
250114_lu Continue the employment in chassisData() of super(). for inheritance from chassisTool()
                Will need to use get_* to assign value in respective *.py
250110_lu Discontinued work allow chassisTools to support strut building 
                But halted work on chassisData and chassisShapeOpn
250106_lu started the process of aap_library development via 
                https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
                The development process was addapted directly from Kia Eisinga
		excellent example.

import aap_lib
from importlib import reload
reload (aap_lib)
from aap_lib import aapfunctions, topoChassisToolbox


Topographical scripting https://wiki.freecad.org/Topological_data_scripting

python library
https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
more trash
Python toolbox template:
Main and one subordinate example
https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/a-template-for-python-toolboxes.htm
Define parameters in a Python toolbox
https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/defining-parameters-in-a-python-toolbox.htm
python libraries
https://www.kdnuggets.com/pip-install-you-a-beginners-guide-to-creating-your-python-library
possibple approach to using tools toolbox/library
https://www.brandonrohrer.com/personal_toolbox
https://stackoverflow.com/questions/2601047/import-a-python-module-without-the-py-extension/43602645#43602645
https://dev.to/lavary/about-missing-1-required-positional-argument-self-in-python-2i36

250113_lu satisfactorily achieved the inheritance of toMM() and toMM_PipeDia() functions from
                ChassisTool for use in ChassisData and the calling of get*_values by aapLib_fire1.FCMacro
250106_lu started the process of aap_library development via 
                https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
                Also watch for: 50 Top Python Libraries of 2025
                https://www.analyticsvidhya.com/blog/2024/12/python-libraries/

250105_lu return to dev on this toolbox 

240913_lu Implement the Toolbox template class
"""


__title__="Toolbox for Building the Exo Cage Chassis With A Macro"
__author__ = "Lucca Uzzo"
__url__ = "http://abbottanp.com"

import pdb, math              # python debugger  see python_gdb.sh for shell script
import FreeCAD as App
from FreeCAD import Gui
          
class topoChassisToolbox(object): 
    def __init__(self):
        super(topoChassisToolbox, self).__init__()
        self.label = "Chassis Toolbox"
        self.alias = "toolbox"
        self.name = "aap_topChassisToolbox"
        # is this needed 
        self.self   = self
        # List of tool classes associated with this toolbox
        self.tools = [chassisTool, chassisListVar, chassisShapeOpn]
    def get_title(self):
        return self.name
    def get_self():
        return self.self

class chassisTool(topoChassisToolbox):
    """
    Creates strut parts used to assemble chassis components
    """
    def __init__(self):
        super(chassisTool, self).__init__()
        self.label = "_projTool. "
        self.description = "central place for the project's re-used tools."
        return None

    """
    # Convert gawdawful imperial to mm. Quote from LES_Tower.FCMacro
    # Ariel Nomad 1: Published Length 126.4  (inches) Motor Trend: p231115_0001_dimensions_inches.png
    # Corresponding image length 5.455 (inches) of Ariel Nomad XYZ by Lekostupov
    # 126.4 = 5.455 * SF
    # See also p240120_0001...4*.png frontal view from 057_
    #Inputs 
    # dimension:  a value in inches
    # scale factor: SF default 1  Scale factor for project.  Use DF if needed of one item
    # desgin factor: DF default 1.  Used to adjust a SWAG or dimenstion issue
    # avoid using zero or negative values for scale and design facotrs
    """

    def toMM(self,value, SF=None, DF = None):
        if DF == None:
            DF = 1
        if SF == None:
            SF = 1
        return (value * 25.4 * SF * DF)

    def toMM_pipeDia(self, value, SF=None, DF = None):
        # See toMM() above
        if DF == None:
            DF = 1
        if SF == None:
            SF = 1
        return (value * 25.4 * SF * DF)


    #https://stackoverflow.com/questions/20184992/finding-3d-distances-using-an-inbuilt-function-in-python
    def distance4vector(self, inx1, iny1, inz1, inx2, iny2, inz2):
        #* provides the "actual true 3D spatial distance between two points in space.
        euclidDis = 0.0   #* zero for point1 and point2 if at same 3dLocation
        euclidDis = math.sqrt((inx2 - inx1)**2 + (iny2 - iny1)**2 + (inz2 - inz1)**2)
        return euclidDis

    #Looking for prnFLAGoneVector = aapdata.prnFLAGoneVector() 
    def prnSingleVector(self, inFLAG,vIn,inMsg):
        if inFLAG == 1:
            App.Console.PrintMessage(inMsg + "    ")
            App.Console.PrintMessage(vIn)
            App.Console.PrintMessage('\n')

    #Looking for prnFLAG4Vectors =  aapdata.prnFLAG4Vectors() 
    def prnVectors(self,inFLAG,inMsg,v1, v2):
        if inFLAG == 1:
            App.Console.PrintMessage(inMsg)
            App.Console.PrintMessage('v1\n')
            App.Console.PrintMessage(v1)
            App.Console.PrintMessage('\n')
            App.Console.PrintMessage('v2\n')
            App.Console.PrintMessage(v2)
            App.Console.PrintMessage('\n')


class chassisListVar(chassisTool):
    def __init__(self):
        super(chassisListVar, self).__init__()
        # Global prn flags set to no print value
        #prnSingleVector() All unwanted print statements off. 
        #Force prn at statement with "1" in first arguement position
        self.prnFLAGoneVector = 0 
        self.prnFLAG4Vectors = 0
        self.Y1 = 0.0
        App.Console.PrintMessage("Test For self.Y1 :: " + str(self.Y1) + "\n")
        """
        Y1 = 9999
        Y1 += 1
        App.Console.PrintMessage("Test For Y1 :: " + str(Y1) + "\n")
        Y1 = 0.0
        App.Console.PrintMessage("Good Y1 :: " + str(Y1) + "\n")
        """
        self.X1 = 0.0
        self.Y1 = 0.0
        self.Z1 = 0.0
        self.ZMID = 0.0
        self.XMID = 0.0
        self.YMID = 0.0
        self.SF = 126.4 / 5.455
        #App.Console.PrintMessage("Test For self.Y1 :: " + str(self.Y1) + "\n")
        self.PIPE_3_5_DIAMETER = super().toMM_pipeDia(.114, self.SF)
        self.PIPE_3_5_RADIUS =  self.PIPE_3_5_DIAMETER/2
        self.PIPE_2_5_DIAMETER = super().toMM_pipeDia(0.0684, self.SF)  
        self.PIPE_2_5_RADIUS = self.PIPE_2_5_DIAMETER / 2.0
        self.lenFrntFactor = .8
        self.lenBakFactor  = 1.05
        self.rearTapperFactor  = .12  
        self.CHASSIS_RUN = super().toMM(2.65, self.SF) * self.lenFrntFactor
        self.CHASSIS_AFT_RUN  = self.Y1
        self.CHASSIS_AFT_SPAN = super().toMM(2.05, self.SF)
        self.CHASSIS_AFT_DEPTH = super().toMM(0.55, self.SF)
        #App.Console.PrintMessage("CHASSIS_AFT_DEPTH:: " + str(self.CHASSIS_AFT_DEPTH) + "\n")
        self.CHASSIS_BOW_DEPTH = super().toMM(0.45, self.SF)
        #App.Console.PrintMessage("CHASSIS_BOW_DEPTH : " + str(self.CHASSIS_BOW_DEPTH) + "\n")
        # at bow end: starboard to port length
        self.CHASSIS_BOW_SPAN = super().toMM(0.8, self.SF)  
        # beam  length starboard to port
        # draft length waterline to keel bottom
        self.CHASSIS_MID_DEPTH = self.CHASSIS_AFT_DEPTH  #super().toMM(0.55)
        ## may need -self.CHASSIS_RUN * lenBakFactor
        self.CHASSIS_RR_RUN = -self.CHASSIS_RUN 
        self.CHASSIS_MID_SPAN = self.CHASSIS_AFT_SPAN 
        #App.Console.PrintMessage("CHASSIS_MID_DEPTH:: " + str(self.CHASSIS_MID_DEPTH) + "\n")
        #tapper rear span depth
        self.RELIEF =  self.CHASSIS_MID_SPAN * self.rearTapperFactor
        # same as self.CHASSIS_AFT_DEPTH  - 2xself.RELIEF
        self.CHASSIS_RR_SPAN = self.CHASSIS_MID_SPAN - 2*self.RELIEF
        # same as self.CHASSIS_AFT_DEPTH 
        self.CHASSIS_RR_DEPTH = self.CHASSIS_MID_DEPTH #super().toMM(0.55)
        return None

    def get_SF(self):
        App.Console.PrintMessage("SF::" + str(self.SF) + '\n')
        return self.SF

    def get_PIPE_3_5_DIAMETER(self):
        App.Console.PrintMessage("3-5 Pipe Dia::" + str(self.PIPE_3_5_DIAMETER) + '\n')
        return self.PIPE_3_5_DIAMETER

    def get_PIPE_3_5_RADIUS(self):
        App.Console.PrintMessage("3-5 Pipe Rad::$" + str(self.PIPE_3_5_RADIUS) + '\n')
        return self.PIPE_3_5_RADIUS

    def get_PIPE_2_5_DIAMETER(self):
        App.Console.PrintMessage("PIPE_2_5_DIAMETER: " + str(self.PIPE_2_5_DIAMETER) + '\n')
        return self.PIPE_2_5_DIAMETER

    def get_PIPE_2_5_RADIUS(self):
        App.Console.PrintMessage("PIPE_2_5_RADIUS: " + str(self.PIPE_2_5_RADIUS) + '\n')
        return self.PIPE_2_5_RADIUS

    def get_prnFLAGoneVector(self):  
        App.Console.PrintMessage("prnFLAGoneVector: " + str(self.prnFLAGoneVector) + '\n')
        return self.prnFLAGoneVector

    def get_prnFLAG4Vectors(self):
        App.Console.PrintMessage("prnFLAG4Vectors: " + str(self.prnFLAG4Vectors) + '\n')
        return self.prnFLAG4Vectors

    def get_Z1(self):
        App.Console.PrintMessage("Z1: " + str(self.Z1) + '\n')
        return self.Z1

    def get_X1(self):
        App.Console.PrintMessage("X1: " + str(self.X1) + '\n')
        return self.X1

    def get_Y1(self):
        App.Console.PrintMessage("Y1: " + str(self.Y1) + '\n')
        return self.Y1

    def get_ZMID(self):
        App.Console.PrintMessage("ZMID: " + str(self.ZMID) + '\n')
        return self.ZMID

    def get_XMID(self):
        App.Console.PrintMessage("XMID: " + str(self.XMID) + '\n')
        return self.XMID

    def get_YMID(self):
        App.Console.PrintMessage("XMID: " + str(self.YMID) + '\n')
        return self.YMID

    def get_lenFrntFactor(self):
        App.Console.PrintMessage("lenFrntFactor: " + str(self.lenFrntFactor) + '\n')
        return self.lenFrntFactor

    def get_lenBakFactor(self):
        App.Console.PrintMessage("lenBakFactor: " + str(self.lenBakFactor) + '\n')
        return self.lenBakFactor

    def get_rearTapperFactor(self):
        App.Console.PrintMessage("rearTapperFactor: " + str(self.rearTapperFactor) + '\n')
        return self.rearTapperFactor

    def get_CHASSIS_RUN(self):
        App.Console.PrintMessage("CHASSIS_RUN: " + str(self.CHASSIS_RUN) + '\n')
        return self.CHASSIS_RUN

    def get_CHASSIS_AFT_RUN(self):
        App.Console.PrintMessage("CHASSIS_AFT_RUN: " + str(self.CHASSIS_AFT_RUN) + '\n')
        return self.CHASSIS_AFT_RUN

    def get_CHASSIS_AFT_SPAN(self):
        App.Console.PrintMessage("CHASSIS_AFT_SPAN: " + str(self.CHASSIS_AFT_SPAN) + '\n')
        return self.CHASSIS_AFT_SPAN

    def get_CHASSIS_AFT_DEPTH(self):
        App.Console.PrintMessage("CHASSIS_AFT_DEPTH: " + str(self.CHASSIS_AFT_DEPTH) + '\n')
        return self.CHASSIS_AFT_DEPTH

    def get_CHASSIS_BOW_SPAN(self):
        App.Console.PrintMessage("CHASSIS_BOW_SPAN: " + str(self.CHASSIS_BOW_SPAN) + '\n')
        return self.CHASSIS_BOW_SPAN

    def get_CHASSIS_BOW_DEPTH(self):
        App.Console.PrintMessage("CHASSIS_BOW_DEPTH: " + str(self.CHASSIS_BOW_DEPTH) + '\n')
        return self.CHASSIS_BOW_DEPTH

    def get_CHASSIS_RR_RUN(self):
        App.Console.PrintMessage("CHASSIS_RR_RUN: " + str(self.CHASSIS_RR_RUN) + '\n')
        return self.CHASSIS_RR_RUN

    def get_CHASSIS_MID_SPAN(self):
        App.Console.PrintMessage("CHASSIS_MID_SPAN: " + str(self.CHASSIS_MID_SPAN) + '\n')
        return self.CHASSIS_MID_SPAN

    def get_CHASSIS_MID_DEPTH(self):
        App.Console.PrintMessage("CHASSIS_MID_DEPTH: " + str(self.CHASSIS_MID_DEPTH) + '\n')
        return self.CHASSIS_MID_DEPTH

    def get_RELIEF(self):
        App.Console.PrintMessage("RELIEF: " + str(self.RELIEF) + '\n')
        return self.RELIEF

    def get_CHASSIS_RR_SPAN(self):
        App.Console.PrintMessage("CHASSIS_RR_SPAN: " + str(self.CHASSIS_RR_SPAN) + '\n')
        return self.CHASSIS_RR_SPAN

    def get_CHASSIS_RR_DEPTH(self):
        App.Console.PrintMessage("CHASSIS_RR_DEPTH: " + str(self.CHASSIS_RR_DEPTH) + '\n')
        return self.CHASSIS_RR_DEPTH

"""
Template
    def call_and_store(self, obj_of_subclass2):
        self.value = obj_of_subclass2.calculate_value()

    def get_value(self):
	return self.value
"""

class chassisShapeOpn(topoChassisToolbox):
    """
    Used to launch functions for building the strut saheps, fues into solids, the selected strut components
    It may also be used to help move/rotate entities.
    """

    def __init__(self):    ##, inwrkPrjFile, inwrkShapeObj, inGui):
        super(chassisShapeOpn, self).__init__()
        self.label = "_calcValues. "
        self.description = "placeholder."
        """
        self.wrkPrjFile    = inwrkPrjFile
        self.wrkShapeObj = winrkShapeObj
        self.Gui           = inGui
        """
        return None

"""
***** for testing adjust comment quotes
opnbox  = topoChassisToolbox()
opntool  = chassisTool()
opndata  = chassisListVar()
opnshape = chassisShapeOpn(inwrkPrjFile, inwrkShapeObj, inGui)
"""

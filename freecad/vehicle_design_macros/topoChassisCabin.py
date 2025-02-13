# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                               *
#*   Copyright (c) 1989- 2024 Abbott Analytical Products   <http://abbottanp.com/>*
#*                                                                               *
#* This program parameterically builds cabin component of the chassis entity 
#*     of the exo cage in roll-out ready state (less defined steering and suspension 
#*	   system) to use for prototyping the invisioned Abiriba_RG  GM EV vehicle 
#*     detailed at: https://abbottanp.com/artifacts/gm_vehicle_WB/index.html.
#* Helpful references:
#* Flip vector 90: https://limnu.com/sketch-easy-90-degree-rotate-vectors/
#*      (X, Y, Z) flips 90 using (Z, Y, -X)
#*     	Base.Vector(0,-TOWER_HEIGHT,0) to (0,0,TOWER_HEIGHT)
#*  3D rotation https://en.wikipedia.org/wiki/Rotation_matrix
#*  Topographical scripting https://wiki.freecad.org/Topological_data_scripting
"""
This macro is abstracted stepwise from from Example: Pierced box https://wiki.freecad.org/Topological_data_scripting
	and merged with 00_990_chassisDimensionPlay_yzPlaneAdjust.FCMacro derived from 
	(LES-Tower.py to fabricate the chassis shape/solid

250202_lu Looking at the delta at the 000_799_989 level

250119_lu Incorporate the topoChassisToolbox aap_lib *.py module
         **********  Untested at the moment   **********

240908 tr  Completed basic Chassis Cabin Starboard and Port frame

240906 tr  Employed Euclid distance and analytical geometry along with using a "plane"
				perpendicular to tube's center line for anchoring the circle to be
				extruded.

240827 tr	Split the front/rear chassis module from the Cabin Arch Chassis module.  
				From 00_008_968_topoScript_refineShape.FCMacro to topoChassisFrame.py.  
				This is the Parent module from which 00_008_965_topoScript_cabinShaping.FCMacro
				inherits.  The module topoChassisFrame.py is found in the FreeCAD/Macro directory.
240825 tr Add for future use
            wrkStr = '_03_981_chassis_topoScripting_cabin
			FreeCAD.getDocument('_03_981_chassis_topoScripting_cabin').
			getObject('Clone001').Placement = App.Placement
			(App.Vector(0,0,0),App.Rotation
			(App.Vector(1.000000000000015,0,0),7.5))
240813 tr	added rear chasis section
240808 tr	begin using vLoc vector to define hoizontal and vertical component
240802 tr 	swapped 003-998_chassis_topoScripting for 003_999*
			swapped 00_008_990topo_*_verticaStrutsmacro for 00_008_991_*_chassisRun macro*	

TBD:
1> Brace struts between Starboard-Port
2> Resize and embed front/rear Starboard-Port
"""


__title__="Build An Exo Cage Chassis With A Macro"
__author__ = "Lucca Uzzo"
__url__ = "http://abbottanp.com"



#import topoChassisFrame as pappa
# not used from topoChassisFrame import ChassisLeg as pappa
#uncomment for usage: 
# remove comment when implemented: from topoChassisToolbox import chassisData, chassisTool
# 240914  may no longer needfrom topoChassisFrame import frontChassisSection, rearChassisSection
#uncomment for usage:
# 240913 from topoChassisFrame import rearChassisSection
#from importlib import reload
#reload(topoChassisFrame )
import pdb, math              # python debugger  see python_gdb.sh for shell script
import FreeCAD as App
import Part, math, Draft
import numpy as np			#handles array of vectors
from FreeCAD import Base
import FreeCADGui as Gui

import aap_lib
from aap_lib import topoChassisToolbox

chassisTool_Error = 0
chassisListVar_Error = 0

aap_wrk = topoChassisToolbox.chassisTool()

try:
	aaptool = topoChassisToolbox.chassisTool()
except Exception:
	print("chassisTool issue.  aaptool can not be defined")
	chassisTool_Error = 9
try:
    aapdata = topoChassisToolbox.chassisListVar()
except Exception:
    print("chassisListVar issue.  aapdata can not be defined")
    chassisListVar_Error = 9
try:
	wrkShape= topoChassisToolbox.chassisShapeOpn()
except Exception:
	print("chassisShapeOpn issue.  aaptool can not be defined")
	chassisTool_Error = 9


wrkPrjFile = "_03_963_999_spike_chassis_topoScripting_cabin_mainBuild"
#250202_lu wrkPrjFile = '_03_963_chassis_topoScripting_cabin_mainBuild ' 
#wrkPrjFile = '_03_964_chassis_topoScripting_cabin_SB-Port'          
#wrkPrjFile = "_03_977_chassis_topoScripting_cabin_archShape"
App.Console.PrintMessage(wrkPrjFile)
App.Console.PrintMessage('\n')


"""
should be in ChassisToolbox once implemned
"""

sf = aapdata.get_SF()  #scale factor: set by desired dimensions, 
					#	proposed gm_vehilce images and layout of 
					# 	LEW-Tower.py model
# For trouble shooting recommend 
#	1> copying current function call 
#	2> commnet-out current function call
#	3> paste copy of current function call
#   4> set the first argument to "1" to print on the next run.
"""
# Function Calls
# Global prn flags set to no print value
# Set Local to 1 to print then 
# reset
All print statements off curretnly.  
Force prn at statement with "1" in first arguement position
"""
prnFLAGoneVector = aapdata.get_prnFLAGoneVector()  #prnSingleVector() 
prnFLAG4Vectors =  aapdata.get_prnFLAG4Vectors()   #prnVectors() Same as above


PIPE_3_5_DIAMETER = aapdata.get_PIPE_3_5_DIAMETER()
"""
250122_lu Python aap_lib Learning Point
This declaration assign the Pipe-3.5-Radius value to a specific location
by making the assignment PIPE_3_5_RADIUS = PIPE_3_5_DIAMETER / 2.0
instead Python assigns a local value (see topoChassisFrame
This may be the reason for the dia/radius diff expereinced.  More testing
needed.
"""
#PIPE_3_5_RADIUS = aapdata.get_PIPE_3_5_RADIUS
# as seen in topoChassisFrame.py
# 250123_lu PIPE_3_5_RADIUS = PIPE_3_5_DIAMETER / 2.0
PIPE_3_5_RADIUS = aapdata.get_PIPE_3_5_RADIUS()
PIPE_2_5_DIAMETER = aapdata.get_PIPE_2_5_DIAMETER()
PIPE_2_5_RADIUS = aapdata.get_PIPE_2_5_RADIUS


Z1 = aapdata.get_Z1()  # Front Section or desired offset from origin
X1 = aapdata.get_X1()
Y1 = aapdata.get_Y1()



#Section Allocated ChassisID 
# 10: assigned to AFT
# 19: assigned to BOW
# 20: assigned to MID
# 30: assigned to RR
CHASSIS_CABIN_STARBOARD = 40
CHASSIS_CABIN_PORT         = 60 
#240914  CHASSIS_CABIN			= chassisTool.toMM(-.085)   #Hold for topoCHassisToolbox dev
CHASSIS_CABIN			= aaptool.toMM(-.085)  # by trial and error centering on xa,ya,za

	
# Y,Z Acquired by ZX sketch X developed by eye Top View
ptsStarboard = [
App.Vector(-458.483,-597.607,1.23674),      
App.Vector(-448,-482.865,75.4962),   
App.Vector(-438,-215.526,226.742),   
App.Vector(-428,-163.644,249.578),   
App.Vector(-418,5.65772,317.877),      
App.Vector(-414,248.77,395.994),   
App.Vector(-410,506.379,440.779),   
App.Vector(-410,632.081,441.291),   
App.Vector(-408,754.514,423.253),   
App.Vector(-404,1032.19,311.289),   
App.Vector(-400,1106.45,259.192),   
App.Vector(-396,1267.68,122.755),   
App.Vector(-395,1352.01,7.90844),   
App.Vector(-394.089,1425.48,-212.338)]  # forget tail,
#240905 App.Vector(-394.089,1425.48,-315.)] #straight tail for thin disk


# Y,Z Acquired by ZX sketch X developed by eye Top View
ptsPort = [
App.Vector(458.483,-597.607,1.23674),      
App.Vector(448,-482.865,75.4962),   
App.Vector(438,-215.526,226.742),   
App.Vector(428,-163.644,249.578),   
App.Vector(418,5.65772,317.877),      
App.Vector(414,248.77,395.994),   
App.Vector(410,506.379,440.779),   
App.Vector(410,632.081,441.291),   
App.Vector(408,754.514,423.253),   
App.Vector(404,1032.19,311.289),   
App.Vector(400,1106.45,259.192),   
App.Vector(396,1267.68,122.755),   
App.Vector(395,1352.01,7.90844),   
App.Vector(394.089,1425.48,-212.338)]  # forget tail,
#240905 App.Vector(394.089,1425.48,-315.)]    #straight tail for thin disk



class ChassisArch(object):   #no longer child of ChassisLeg
#class ChassisArch(object):   #no longer child of ChassisLeg	# def setupArchHndlr(pts, subChassisID):
	def __init__(self, pts, subChassisID):  #xa, ya, za, xb, yb, zb, subChassisID):
		rtnMessage = "Nobody Home\n"
		if subChassisID == CHASSIS_CABIN_STARBOARD:
			self.fabChassisArch(ptsStarboard)
		if subChassisID == CHASSIS_CABIN_PORT:
			self.fabChassisArch(ptsPort)
		rtnMessage = "\ndone\n"
		#App.getDocument(wrkPrjFile).recompute()
		App.Console.PrintMessage(rtnMessage)


	def fabChassisArch(self,pts4Wrk):
		#See Example3 of spike 005_999_spline_pipe.FCStd 
		#	and Macro 005_999_buildsplinePipe.FCMacro
		np_Arr   = np.array(pts4Wrk)  #vLoc
		spline1 = Draft.make_bspline(pts4Wrk, closed=False)
		#Last point for circle shape point 14 (-394.089,1425.48,-212.338)
		#	occurs at len(ptsStarboard)-1	
		#load from 0: loopNdx = 0  #one fewer than number of elments lin pts list
		loopNdx = 13   #one fewer than number of elments lin pts list
		
		xa = 0.0
		ya = 0.0
		za = 0.0
		while loopNdx > 0: # len(ptsStarboard)-1:
		#load from 0: while loopNdx < len(ptsStarboard)-1:
			pntNdx = loopNdx
			wrkArrNa   = np_Arr[pntNdx]
			xa         = wrkArrNa[0]		#yields the x-axis vector component of bow 2d cross-section	 
			ya         = wrkArrNa[1]		#yields the sections length from aft to bow
			za         = wrkArrNa[2]	
			wrkArrNb   = np_Arr[pntNdx-1]
			xb         = wrkArrNb[0]		#yields the x-axis vector component of bow 2d cross-section	 
			yb         = wrkArrNb[1]		#yields the sections length from aft to bow
			zb         = wrkArrNb[2]	
			App.Console.PrintMessage("wrkArrNa:: xa,ya, za\n")
			App.Console.PrintMessage(wrkArrNa)
			App.Console.PrintMessage("\n")
			#
			euclidVector = self.findEuclidPoint(xa, ya, za, xb, yb, zb)
			xbe = euclidVector[0]
			ybe = euclidVector[1]
			zbe = euclidVector[2]
			App.Console.PrintMessage("euclidVector")
			App.Console.PrintMessage(euclidVector)
			App.Console.PrintMessage("\n")
			#Panel1 Note: use plane1 to identify the targetAngle value
			#   then comment-out all plane1 entries.
			#	Use the shape Increments Translation and Rotational
			#	
			plane1 = Part.makePlane(100, 100, App.Vector(xa, ya, za), App.Vector(0, 1, 0))
			plane1.translate(App.Vector(CHASSIS_CABIN, 0, CHASSIS_CABIN))
			#Next two lines for reference only				
			#myShape.rotate(App.Vector(0, 0, 0),App.Vector(0, 0, 1), 180)				
			##plane1.rotate(App.Vector(xa,ya, za),App.Vector(1, 0, 0), 180)
			#pulled chunck_001
			if loopNdx == 13: #83.2020
				targetAngle = 276.798  #the the plane1 note 
				#Gui.Selection.addSelection(wrkPrjFile,'Shape','',-444.116,1375.8,-218.26)
			if loopNdx == 12: #71.9680
				targetAngle = 288.032
			if loopNdx == 11: #66.6010
				targetAngle = 293.399
			if loopNdx == 10: #51.6550
				targetAngle = 308.345
			if loopNdx == 9:  #36.6570
				targetAngle = 323.343
			if loopNdx == 8:  #18.6220     
				targetAngle = 341.378    
			if loopNdx == 7:  #352.2770    
				targetAngle = 352.2770    ##Watchout for flip of as approaches 360
			if loopNdx == 6:       
				targetAngle = 180.462    
			if loopNdx == 5:     
				targetAngle = 206.2480   
			if loopNdx == 4:   
				targetAngle = 202.8600    
			if loopNdx == 3:     
				targetAngle = 204.3820   
			if loopNdx == 2:     
				targetAngle = 213.7470    

				
			plane1.rotate(App.Vector(xa,ya, za),App.Vector(1, 0, 0), targetAngle)
		
			#Part.show(plane1)  #turn-on to see plane1 for targetAngle approximation
			rtnRadius = aapdata.get_PIPE_3_5_RADIUS()
			App.Console.PrintMessage("PIPE_3_5_RADIUS *::" + str(rtnRadius)+  " \n")
			aaptool.prnSingleVector(1,App.Vector(xa, ya, za),"App.Vector(xa, ya, za)")
			aaptool.prnSingleVector(1,App.Vector(0,1,0), "App.Vector(0, 1, 0)")
			circle = Part.makeCircle(PIPE_3_5_RADIUS, App.Vector(xa, ya, za), App.Vector(0,1.0,0))
			
			circle.translate(App.Vector(0, -1, 0))
			circle.rotate(App.Vector(xa, ya, za),App.Vector(1, 0, 0), targetAngle)
			wire=Part.Wire(circle)
			face=Part.Face(wire)
			self._tube = face.extrude(Base.Vector(xa-xbe,ya-ybe,za-zbe))
			#App.Console.PrintMessage('Check for Port/Starboard required placement\n')
			Part.show(self._tube)
			#self._tube = super().__init__(xa,ya, za, xbe, ybe, zbe, CHASSIS_CABIN_STARBOARD)
			loopNdx -= 1


	def getAngle(self, pnt1, pnt2,eDistance):
		cosValue = (pnt2 - pnt1)/eDistance
		return cosValue
     
	def findEuclidPoint(self, x1, y1, z1, x2, y2, z2):
		euclidDis = aaptool.distance4vector(x1, y1, z1, x2, y2, z2)
		App.Console.PrintMessage("d Distance from pnt1 to pnt2 in 3D\n" )
		App.Console.PrintMessage(euclidDis)
		App.Console.PrintMessage("\n")
		alpha = self.getAngle(x1,x2,euclidDis)
		beta  = self.getAngle(y1,y2,euclidDis)
		gamma = self.getAngle(z1,z2,euclidDis)
		App.Console.PrintMessage("cosAngles_values\n")
		App.Console.PrintMessage(Base.Vector(alpha, beta, gamma))
		App.Console.PrintMessage("\n")
		xdif   = alpha / euclidDis
		ydif   = beta  / euclidDis
		zdif   = gamma / euclidDis
		#xdif = x1 - x2e
		x2e   = x1 - euclidDis * alpha
		y2e   = y1 - euclidDis * beta
		z2e   = z1 - euclidDis * gamma
		return App.Vector(x2e, y2e, z2e)




def cabinChassisSection():
	arch40 = ChassisArch(ptsStarboard, CHASSIS_CABIN_STARBOARD)
	arch60 = ChassisArch(ptsStarboard, CHASSIS_CABIN_PORT)
		

#frontChassisSection()
#rearChassisSection()
cabinChassisSection()

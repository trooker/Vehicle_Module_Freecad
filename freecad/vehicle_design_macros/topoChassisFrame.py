# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                                    *
#*   Copyright (c) 1989- 2025 Abbott Analytical Products   <http://abbottanp.com/>*
#*                                                                               *
#* This program parameterically builds the basic chassis components exo cage 
#*     in roll-out ready state (less defined steering and suspension system) 
#*     to use for prototyping the invisioned Abiriba_RG  GM EV vehicle 
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
	LES-Tower.py to fabricate the chassis shape/solid

250119_lu Incorporate the topoChassisToolbox aap_lib *.py module
         **********   Untested at the moment   **********
250105_lu Resolved __init()__ return value issue.  The FrntChassis was miss using the self.tube.  
				The __init__() ...return serves to "set()" values neeeded at constructor level.  
250103_lu Working the __init()__ return value.  Relearned usage self._tube being Shape*
import topoChassisFrame 
from importlib import reload
reload (topoChassisFrame)
			1> https://stackoverflow.com/questions/2491819/how-to-return-a-value-from-init-in-python
			2> https://www.geeksforgeeks.org/constructors-in-python/ 
			3> https://builtin.com/data-science/new-python
				__new__ happens first, then __init__.
				__new__ can return any object, while __init__ must return None.
			4> https://www.geeksforgeeks.org/dunder-magic-methods-python/
				4.1> https://www.geeksforgeeks.org/__new__-in-python/
			5> Searcl on tutorial example pythonusage __new__() and __init__() with arguments ==>>
				Example

241122_lu Corrected comment mark error had four quotes rather than three see BOB
			backup for erroenous version
240923_lu Removed Shape004 and Shape009 to cleanup Fusion further downstream....
240827_lu	Split the front/rear chassis module from the Cabin Arch Chassis module.  
				From 00_008_968_topoScript_refineShape.FCMacro to topoChassisFrame.py.  
				This is the Parent module from which 00_008_965_topoScript_cabinShaping.FCMacro
				inherits.  The module topoChassisFrame.py is found in the FreeCAD/Macro directory.
240823_lu	added rear chasis section
240808_tr	begin using vLoc vector to define hoizontal and vertical component
240802_tr 	swapped 003-998_chassis_topoScripting for 003_999*
			swapped 00_008_990topo_*_verticaStrutsmacro for 00_008_991_*_chassisRun macro*	




https://www.w3schools.com/python/trypython.asp?filename=demo_while
beam = 8
draft = 5
vLoc = [(-beam, 0, -draft), (beam, 0, -draft), (beam, 0, draft), (-beam, 0, draft), (-beam, 0, -draft)]

i = 0
while i < len(vLoc):
  print(i)
  i += 1

Printed:
0
1
2
3
4

"""		
"""
example adapted from https://www.w3schools.com/python/numpy/trypython.asp?filename=demo_numpy_array_index1
import numpy as np

beam = 8
draft = 5
vLoc = [(-beam, 0, -draft), (beam, 0, -draft), (beam, 0, draft), (-beam, 0, draft), (-beam, 0, -draft)]

arr = np.array(vLoc)

print(arr[1])np.array(vLoc)
"""
"""
		np_Arr = np.array(vLoc)
		wrkArr0  = np_Arr[0]
		vxbow0	= wrkArr0[0]		#yields the x-axis vector component of bow 2d cross-section	 
		vybow0  = wrkArr0[0]		#yields the sections length from aft to bow
		vzbow0  = wrkArr0[2]		#yields the z-axis vector component
		wrkArr1  = np_Arr[1]
		vxbow1	= wrkArr0[0]
		vzbow1  = wrkArr0[2]
		wrkArr2  = np_Arr[2]
		vxbow2	= wrkArr0[0]
		vzbow2  = wrkArr0[2]
		wrkArr3  = np_Arr[3]
		vxbow3	= wrkArr0[0]
		vzbow3  = wrkArr0[2]
"""


__title__="Build An Lower Main Chassis of an Exo Cage Vehicle With A Macro"
__author__ = "Lucca Uzzo"
__url__ = "http://abbottanp.com"


# remove comment when implemented: from topoChassisToolbox import chassisData, chassisTool
import pdb, math              # python debugger  see python_gdb.sh for shell script
import FreeCAD as App
import Part, math,Draft
import numpy as np 
from FreeCAD import Base
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


"""
should be in ChassisToolbox once implemned
"""
sf = aapdata.get_SF()  #scale factor: set by desired dimensions, 

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
PIPE_3_5_RADIUS = PIPE_3_5_DIAMETER / 2.0
PIPE_2_5_DIAMETER = aapdata.get_PIPE_2_5_DIAMETER()
PIPE_2_5_RADIUS = PIPE_2_5_DIAMETER / 2.0


Z1 = aapdata.get_Z1()  # Front Section or desired offset from origin
X1 = aapdata.get_X1()
Y1 = aapdata.get_Y1()

ZMID = aapdata.get_ZMID()  #Rear Section or desired offsetfrom origin
XMID = aapdata.get_XMID()
YMID = aapdata.get_YMID()

lenFrntFactor = aapdata. get_lenFrntFactor()
lenBakFactor  = aapdata.get_lenBakFactor()
rearTapperFactor  = aapdata.get_rearTapperFactor()  #If set to 0.00 there will be an error thrown for divide by zero

CHASSIS_RUN = aapdata.get_CHASSIS_RUN() * aapdata. get_lenFrntFactor()      # length from bow to aft section was 5.455  looks good at 3.25..3.80  squared at 4.0
CHASSIS_AFT_RUN  = aapdata.get_CHASSIS_AFT_RUN()
CHASSIS_AFT_SPAN = aapdata.get_CHASSIS_AFT_SPAN()  # at aft end: widest starboard to port aap_wrk.toMM(1.209)    #2.65)  #was 1.209
CHASSIS_AFT_DEPTH = aapdata.get_CHASSIS_AFT_DEPTH()
CHASSIS_BOW_SPAN = aapdata.get_CHASSIS_BOW_SPAN()   # at bow end: starboard to port length 
CHASSIS_BOW_DEPTH = aapdata.get_CHASSIS_BOW_DEPTH()
# beam  length starboard to port
# draft length waterline to keel bottom
CHASSIS_RR_RUN = -aapdata.get_CHASSIS_RR_RUN () ##* lenBakFactor
CHASSIS_MID_SPAN = aapdata.get_CHASSIS_MID_SPAN() 
CHASSIS_MID_DEPTH = aapdata.get_CHASSIS_MID_DEPTH()
RELIEF =  aapdata.get_RELIEF()   #tapper rear span depth
CHASSIS_RR_SPAN = aapdata.get_CHASSIS_RR_SPAN()
CHASSIS_RR_DEPTH = aapdata.get_CHASSIS_RR_DEPTH() ##- RELIEF



class ChassisLeg(object):
	"""
	def __new__(self, xa, ya, za, xb, yb, zb, subChassisID):
		App.Console.PrintMessage('Calling instance\n')
		instance = super().__new__(self)
		App.Console.PrintMessage('__init__() done.  Begin Drawing\n')
		#*250103_lu was if self._sectionID == 1:  #front chassis scetion legs i.e working on the negative side of Y-Axis
		return instance._tube # instance of a "new" shape
	"""
	def __init__(self, xa, ya, za, xb, yb, zb, subChassisID):
		#sub_ChassisI_D = 1
		# a: aft    or rr   or centerline Arch shape
		# b: bow    or mid
		'''
		App.Console.PrintMessage("ChassisLeg(object)")
		App.Console.PrintMessage("xa, ya, za\n")
		App.Console.PrintMessage(xa)
		App.Console.PrintMessage("\n")
		App.Console.PrintMessage(ya)  
		App.Console.PrintMessage("\n")
		App.Console.PrintMessage(za)
		App.Console.PrintMessage("\n")
		App.Console.PrintMessage(xb)
		App.Console.PrintMessage("\n")
		App.Console.PrintMessage(yb)
		App.Console.PrintMessage("\n")
		App.Console.PrintMessage(zb)
		App.Console.PrintMessage("\n")
		
		App.Console.PrintMessage("subChassisID\n")
		App.Console.PrintMessage(subChassisID)
		App.Console.PrintMessage("\n")
		'''
		#* abstract suspect
		self._sectionID = subChassisID
		if self._sectionID > 2:
			App.Console.PrintMessage('Setup for Port/Starboard placement')
			self._isChildFlag = 1
			self._sectionID = 1
		else:   # already equals 1 or 2
			self._isChildFlag = 0
		#for Dev
		self._message = 'self._sectionID:   ' +   str(self._sectionID)
		App.Console.PrintMessage(self._message + '\n')
		if self._sectionID == 1:  #front chassis scetion legs i.e working on the negative side of Y-Axis
			self._aft = Base.Vector(xa,ya,za)     # aft and rr   was (x1,y1,z1) where z1 = 0
			self._bow = Base.Vector(xb,yb,zb)   # bow and mid was(x2,y2,z2)
			self._run = yb   # was z2
			self._tan_x =  ya  / float(xa-xb)  # was z2 / float(x1-x2)
			self._tan_z =  ya / float(za-zb)  # was z2 / float(y1-y2)
			# Draw separately here, as the pipe ends are level with the main plane
			rtnRadius = aapdata.get_PIPE_3_5_RADIUS()

			App.Console.PrintMessage("PIPE_3_5_RADIUS =::" + str(aapdata.get_PIPE_3_5_RADIUS())+  " \n")
			aaptool.prnSingleVector(1,App.Vector(xa, ya, za),"App.Vector(xa, ya, za)")
			aaptool.prnSingleVector(1,App.Vector(0,1,0), "App.Vector(0, 1, 0)")

			circle = Part.makeCircle(aapdata.get_PIPE_3_5_RADIUS(), self._bow,App.Vector(0,1,0))
			circle.translate(App.Vector(0, -ya, 0))
			#circle.rotate(App.Vector(0, 0, 0),App.Vector(0, 0, 1), 90)
			wire=Part.Wire(circle)
			face=Part.Face(wire)
			#self._tube = face.extrude(Base.Vector(xb-xa,yb-ya,zb-za))
			self._tube = face.extrude(Base.Vector(xa-xb,ya-yb,za-zb))
			App.Console.PrintMessage('Check for Port/Starboard required placement\n')
			Part.show(self._tube)
			"""
			if self.subChassisID == 40:  # CHASSIS_CABIN_STARBOARD
				self._message = 'CHASSIS_CABIN_STARBOARD required placement executed\n'
				App.Console.PrintMessage(self._message)
				self._tube.translate(App.Vector(0, -126, 0))  #Counted squares of Draft grid top view
			elif self.subChassisID == 60:  # CHASSIS_CABIN_PORT
				self._message = 'CHASSIS_CABIN_PORT required placement executed\n'
				App.Console.PrintMessage(self._message)
				self._tube.translate(App.Vector(0, -126, 0))  #Counted squares of Draft grid
			"""
		elif self._sectionID ==2: #rear chassis section legs i.e working on the positive side of Y-Axis
			self._aft = Base.Vector(xa,ya,za)   # aft and rr  was(x1,y1,z1) where z1 = 0
			self._bow = Base.Vector(xb,yb,zb)   # bow and mid was(x2,y2,z2)
			self.run = ya
			if xa == xb:  #experienced divide by zero error during development
				self._tan_x =  ya
			else:
				self._tan_x =  ya  / float(xa-xb)  # was z2 / float(x1-x2)
			if za == zb:
				self._tan_z =  ya
			else:
				self._tan_z =  ya  / float(za-zb)  # was z2 / float(y1-y2)
			# Draw separately here, as the pipe ends are level with the main plane
			circle = Part.makeCircle(PIPE_3_5_RADIUS, self._aft,App.Vector(0,1,0))
			circle.translate(App.Vector(0, -ya, 0))
			#circle.rotate(App.Vector(0, 0, 0),App.Vector(0, 0, 1), 90)
			wire=Part.Wire(circle)
			face=Part.Face(wire)
			self._tube = face.extrude(Base.Vector(xb-xa,yb-ya,zb-za))
			Part.show(self._tube)
		return None


 

	def getVector(self, vLoc, pntNdx):
		np_Arr    = np.array(vLoc)
		wrkArrN   = np_Arr[pntNdx]
		spanLocX  = wrkArrN[0]		#yields the x-axis vector component of bow 2d cross-section	 
		yRun      = wrkArrN[1]		#yields the sections length from aft to bow
		spanLocZ  = -wrkArrN[2]		#yields the z-axis vector component
		vV = Base.Vector(spanLocX, yRun, spanLocZ)
		outMsg =('weld-> getVector vertical strut vector spanLocX spanLocZ \n')
		aaptool.prnSingleVector(prnFLAGoneVector, vV,outMsg)
		return vV

	def weldPoint(self, vLoc, pntNdx, flowID, isZ):
		"""
		v2 #on targetItem but assuming symmetry of shape
		v1 #on chassisLeg
		"""
		outMsg =('Enter weld point from flowID \n')
		aaptool.prnSingleVector(prnFLAGoneVector, flowID,outMsg)

		v = Base.Vector([0,0,0])
		newV = Base.Vector([0,0,0])
		if flowID == 20 or flowID == 29 or flowID == 30 or flowID == 39:
			newV = self.getVector(vLoc, pntNdx)
			spanLocX = newV[0]
			yRun     = newV[1]
			spanLocZ	 = newV[2]
			if isZ == 1:
				spanLocX = -spanLocX
				spanLocZ =  spanLocZ
			elif isZ == 0:
				spanLocX = spanLocX		#yields the z-axis vector component
				spanLocZ = spanLocZ
			if flowID == 29 or flowID == 39:
				p = [spanLocZ, 0] #240822  use 2D vector definition
				q = [-spanLocZ, 0] 
				# Calculate Euclidean distance https://www.w3schools.com/python/showpython.asp?filename=demo_ref_math_dist
				spanLocZ = math.dist(p, q)/2 #need to reset mirror image of shape to compensate for this work-around
			v = Base.Vector(spanLocX, yRun, spanLocZ) #240806 was beamSpanLoc)
		if flowID == 21 or flowID == 22 or flowID == 31 or flowID == 32:
			isX = isZ
			newV = self.getVector(vLoc, pntNdx)
			spanLocX = newV[0]
			yRun     = newV[1]
			spanLocZ	 = newV[2]
			if isX == 1:
				spanLocX = -spanLocX
				spanLocZ =  spanLocZ
			elif isX ==0:
				spanLocX = spanLocX		#yields the z-axis vector component
				spanLocZ = spanLocZ
			outMsg =('weld point vLoc spanLocX & spanLocZ \n')
			aaptool.prnSingleVector(prnFLAGoneVector, v,outMsg)

			v = Base.Vector(spanLocX, yRun, spanLocZ) #240806 was beamSpanLoc)
		outMsg =('weld point formed Vector for strut \n')
		aaptool.prnSingleVector(prnFLAGoneVector, v,outMsg)
		return v

		
		
		
		
	def intersection(self, inValue, flowID):
		"""
		Uses the LES_Tower.py model
		Generates the vector connection between legs of the chassis
		  for the horizontal/vertica strut
		"""
		x = 0
		y = 0
		z = 0  #(height / self._tan_x) + self._base.x
		v = 0
		beamSpanLoc = inValue
		#Following the LES_Tower.py model
		if flowID ==1 or flowID == 9: # bow horizontal
			#beamSpanLoc = inValue #/ 2  # Assumed split down x axis centerline
			x = self._bow.x #- (beamSpanLoc / self._tan_x)
			z = self._bow.z #- (beamSpanLoc / self._tan_z)  #was tan_y
			y = self._bow.y # section length
			v = Base.Vector(x, y, z) #240806 was beamSpanLoc)
			outMsg =('v:...bow horizontal \n')
			aaptool.prnSingleVector (prnFLAGoneVector, v,outMsg)
			outMsg = '\nself.intersection  bow horizontal flowID: 1\n'
			aaptool.prnSingleVector(prnFLAGoneVector, v,outMsg)
		elif flowID == 2 or flowID == 19: # aft horizontal
			#beamSpanLoc = inValue #/ 2  # Assumed split down  x axis centerline
			x = self._aft.x #- (beamSpanLoc / self._tan_x)
			y = 0 # section length
			z = self._aft.z #- (beamSpanLoc / self._tan_z)  #was tan_y
			v = Base.Vector(x, y, z) #240806 was beamSpanLoc)beamSpanLoc)
			outMsg = 'self.intersection aft horizontal  flowID: 2\n'
			aaptool.prnSingleVector(prnFLAGoneVector, v,outMsg)
		elif flowID == 3:
			#beamSpanLoc = inValue #/2 # Assumed split down centerline
			x = self._bow.x #- (beamSpanLoc / self._tan_x)
			y = self._bow.y # section length
			z = self._bow.z #- (beamSpanLoc / self._tan_z)  #was tan_y
			v = Base.Vector(-x, y, -z)
			outMsg = 'self.intersection flowID: 3\n'
			aaptool.prnSingleVector(prnFLAGoneVector, v,outMsg)
		elif flowID == 4:
			#beamSpanLoc = inValue #/2  # Assumed split down centerline
			x = self._bow.x #- (beamSpanLoc / self._tan_x)
			y = self._bow.y # section length
			z = self._bow.z #- (beamSpanLoc / self._tan_z)  #was tan_y
			v = Base.Vector(x, y, z) #240806 was beamSpanLoc)
			outMsg = 'self.intersection flowID: 4\n'
			aaptool.prnSingleVector(prnFLAGoneVector, v,outMsg)
		elif flowID == 5:
			#beamSpanLoc = inValue #/2  # Assumed split down centerline
			x = self._aft.x #- (beamSpanLoc / self._tan_x)
			y = self._aft.y
			z = self._aft.z #- (beamSpanLoc / self._tan_z)  #was tan_y
			v = Base.Vector(-x, y, -z) #240806 was beamSpanLoc)beamSpanLoc)
			outMsg = 'self.intersection flowID: 4\n'	
			aaptool.prnSingleVector(prnFLAGoneVector, v,outMsg)
		elif flowID == 6:
			#beamSpanLoc = inValue #/2  # Assumed split down centerline
			x = self._aft.x #- (beamSpanLoc / self._tan_x)
			y = self._aft.y
			z = self._aft.z #- (beamSpanLoc / self._tan_z)  #was tan_y
			v = Base.Vector(x, y, z) #240806 was beamSpanLoc)beamSpanLoc)
			outMsg = 'self.intersection flowID: 4\n'
			aaptool.prnSingleVector(prnFLAGoneVector, v,outMsg)
		return v


	"""
#Problem here need better vector math model for "p2.sub(p1)
https://www.w3schools.com/ai/tryit.asp?filename=tryai_tensor_sub
Javascript Tensor Math example
const tensorA = tf.tensor([[1, 2], [3, 4], [5, 6]]);
const tensorB = tf.tensor([[1,-1], [2,-2], [3,-3]]);

// Tensor Subtraction
const tensorNew = tensorA.sub(tensorB);

// Result: [ [0, 3], [1, 6], [2, 9] ]
const tensorA = tf.tensor([-603.2674610449129, 0.0, 161.85224564619617]);
const tensorB = tf.tensor([603.2674610449129, 0.0, 161.85224564619617]);

// Tensor Subtraction
const tensorNew = tensorA.sub(tensorB);

Tensor [-1206.5349121, 0, 0]
	"""
        
	def handleVectorFunction(self,p2,p1,vFlag):
		newV = ([0,0,0])
		if vFlag == 0:
			if p2[0]> 0:
				outMsg = '---  p2.add(p1) ---\n\n'	
				aaptool.prnVectors                                (prnFLAG4Vectors, outMsg,p2,p1)
				aaptool.prnVectors                                (1, outMsg,p2,p1)
				newV = p2.add(p1)
			else:
				outMsg = '---  p2.sub(p1) ---\n"'	
				aaptool.prnVectors(prnFLAG4Vectors, outMsg,p2,p1)
				newV = p2.sub(p1)
		outMsg = '**** rtn from handleVectorFunc vFlag: 0\n'	
		aaptool.prnSingleVector(prnFLAGoneVector,newV,outMsg)
		return newV
		
		

	def drawVerticalTube(self, radius, p1, p2, yRun, zDirFlag, flowFlag):
			outMsg = '######### drawVerticalTube\n'	
			aaptool.prnVectors(prnFLAG4Vectors, outMsg,p2,p1)
			if zDirFlag == 0 and flowFlag == 3:
				circle = Part.makeCircle(radius, p1, App.Vector(0, 0, -1))
			if zDirFlag == 1 and flowFlag == 4:
				circle = Part.makeCircle(radius, p1, App.Vector(0, 0, 1))
			if zDirFlag == 0 and flowFlag == 5:
				circle = Part.makeCircle(radius, p1, App.Vector(0, 0, -1))
			if zDirFlag == 1 and flowFlag == 6:
				circle = Part.makeCircle(radius, p1, App.Vector(0, 0, 1))
			if zDirFlag == 0 and flowFlag == 21:
				circle = Part.makeCircle(radius, p1, App.Vector(0, 0, -1))
			if zDirFlag == 1 and flowFlag == 22:
				circle = Part.makeCircle(radius, p1, App.Vector(0, 0, 1))
			if zDirFlag == 0 and flowFlag == 31:
				circle = Part.makeCircle(radius, p1, App.Vector(0, 0, -1))
			if zDirFlag == 1 and flowFlag == 32:
				circle = Part.makeCircle(radius, p1, App.Vector(0, 0, 1))
			try:
				circle.translate(App.Vector(0, yRun, 0))	
				#circle.rotate(App.Vector(0, 0, 0),App.Vector(1, 0, 0), 90)		
				wire=Part.Wire(circle)
				face=Part.Face(wire)
				tube = face.extrude(App.Vector(0, 0, -p1[2]*2))
				tube.translate(App.Vector(0, -yRun, 0))	 
				return tube 
			except:
				App.Console.PrintMessage("drawVerticalTube can not return tube for flowFlag!")
				App.Console.PrintMessage(flowFlag)
				App.Console.PrintMessage("\nslogging forward\n")
				return None				

		

	def drawHorizontalTube(self, radius, p1, p2, yRun, dropFlag, flowFlag):
			outMsg = '######### drawHorizontalTube\n'	
			#250121_lu aaptool.prnVectors(prnFLAG4Vectors, outMsg,p2,p1)
			aaptool.prnVectors(1, outMsg,p2,p1)
			strutVector = self.handleVectorFunction(p2,p1,0)
			outMsg = '********** Post p2.sub(p1)\n'
			#250121_lu aaptool.prnVectors(prnFLAG4Vectors, outMsg,strutVector, p1)
			aaptool.prnVectors(1, outMsg,strutVector, p1)
			circle = Part.makeCircle(radius, p1, strutVector)
			circle.translate(App.Vector(0, yRun, 0))			
			wire=Part.Wire(circle)
			face=Part.Face(wire)
			tube = face.extrude(strutVector)
			if dropFlag == 0 and flowFlag == 1:
				tube.translate(App.Vector(0, -yRun, 0)) #upper horizontal for bow
			elif dropFlag == 1 and flowFlag == 9:
				tube.translate(App.Vector(0, -yRun, (-2*self._bow.z)))  #lower horizontal for bow
			elif dropFlag == 0 and flowFlag == 2:
				tube.translate(App.Vector(0, -yRun, 0)) #upper horizontal for aft
			elif dropFlag == 1 and flowFlag == 19:
				tube.translate(App.Vector(0, -yRun, (-2*self._aft.z)))  #lower horizontal for aft
			elif dropFlag == 0 and flowFlag == 20:
				tube.translate(App.Vector(0, yRun, 0)) #upper horizontal for MID
			elif dropFlag == 1 and flowFlag == 29:
				tube.translate(App.Vector(0, yRun, (-2*self._aft.z)))  #lower horizontal for MID
			elif dropFlag == 0 and flowFlag == 30:
				tube.translate(App.Vector(0, -yRun, 0)) #upper horizontal for RR
			elif dropFlag == 1 and flowFlag == 39:
				tube.translate(App.Vector(0, -yRun, (-2*self._aft.z))) #lower horizontal for RR
			try:
				return tube 
			except:
				App.Console.PrintMesage("drawHorizontalTube can not return tube for flowFlag!")
				App.Console.PrintMessage(flowFlag)
				App.Console.PrintMessage("\nslogging forward\n")
				return None				

	def drawStrut(self, radius, p1, p2, yRun, flowFlag):
		"""
		Sets the Circle direction for future drawing
		Parameters
		p1: vector for leg10
		p2: vector for targetLeg
		Definitions used in function
		0: Z = -1 direction of Circle
		1: Z =  1 direction of Circle
		"""
		outMsg = "------ yRun -------\n"
		aaptool.prnSingleVector(prnFLAGoneVector,yRun,outMsg)
		outMsg = '######### drawStrut\n'	
		#250121_lu aaptool.prnVectors(prnFLAG4Vectors, outMsg,p2,p1)
		aaptool.prnVectors(1, outMsg,p2,p1)

		if flowFlag == 1:  # horizontal bow
			tube = self.drawHorizontalTube(radius, p1, p2, yRun, 0, flowFlag) 
		if flowFlag == 9:  # horizontal bow
			tube = self.drawHorizontalTube( radius, p1, p2, yRun, 1, flowFlag) 
		if flowFlag == 2:  # horizontal aft
			tube = self.drawHorizontalTube( radius, p1, p2, yRun, 0, flowFlag) 
		if flowFlag == 19:  # horizontal aft
			tube = self.drawHorizontalTube( radius, p1, p2, yRun, 1, flowFlag) 
			# no trans needed tube.translate(App.Vector(0, -yRun, 0)) #240809 was-yRun, 0))	 
		if flowFlag == 20:  # horizontal mid upper
			tube = self.drawHorizontalTube( radius, p1, p2, yRun, 0, flowFlag)
		if flowFlag == 29:  # horizontal mid lower
			tube = self.drawHorizontalTube( radius, p1, p2, yRun, 1, flowFlag)
		if flowFlag == 30:  # horizontal RR upper
			tube = self.drawHorizontalTube( radius, p1, p2, yRun, 0, flowFlag)
			#tube.translate(App.Vector(0, -yRun, 0))	 
		if flowFlag == 39:  # horizontal RR lower
			tube = self.drawHorizontalTube( radius, p1, p2, yRun, 1, flowFlag)
			#tube.translate(App.Vector(0, -yRun, 0))	 
		elif flowFlag == 3: # vertical connect 3..6
			tube = self.drawVerticalTube( radius, p1, p2, yRun, 0, flowFlag) #Z = -1 direction of Circle
		elif flowFlag == 4: # vertical connect
			tube = self.drawVerticalTube( radius, p1, p2, yRun, 1, flowFlag) #Z =  1 direction of Circle
		elif flowFlag == 5: # vertical aft connect
			# no trans needed 
			tube = self.drawVerticalTube( radius, p1, p2, 0, 0, flowFlag) #Z = -1 direction of Circle
			# no trans needed tube.translate(App.Vector(0, -yRun, 0))	 
		elif flowFlag == 6: # vertical aft connect
			# no trans needed tube.translate(App.Vector(0, -yRun, 0))	 
			tube = self.drawVerticalTube( radius, p1, p2, 0, 1, flowFlag) #Z =  1 direction of Circle
		elif flowFlag == 21: # vertical MID left 
			tube = self.drawVerticalTube( radius, p1, p2, 0, 0, flowFlag) #Z = -1 direction of Circle
			# no trans needed tube.translate(App.Vector(0, -yRun, 0))	 
		elif flowFlag == 22: # vertical MID right 
			tube = self.drawVerticalTube( radius, p1, p2, 0, 1, flowFlag) #Z =  1 direction of Circle
			# no trans needed tube.translate(App.Vector(0, -yRun, 0))	 
		elif flowFlag == 31: # vertical RR left
			# no trans needed 
			tube = self.drawVerticalTube( radius, p1, p2, 0, 0, flowFlag) #Z = -1 direction of Circle
			#tube.translate(App.Vector(0, yRun, 0))	 
		elif flowFlag == 32: # vertical RR right
			# no trans needed tube.translate(App.Vector(0, -yRun, 0))	 
			tube = self.drawVerticalTube( radius, p1, p2, 0, 1, flowFlag) #Z =  1 direction of Circle
			#tube.translate(App.Vector(0, yRun, 0))	 
		try:
			Part.show(tube)
			return tube
		except:
			App.Console.PrintMessage("Part.Show(tube) throws error as not reference before usage.\n")
		return None

	def horzStrut(self, targetTower, radius, vLoc, pntNdx, spanID):    #spanLoc2, spanLoc1, yRun,
		#if height2 is Null:
		#	height2 = height;
		"""
		Need to resolve x and z axiz componet of position
		"""
		np_Arr   = np.array(vLoc)
		wrkArrN   = np_Arr[pntNdx]
		spanLoc1 = wrkArrN[0]		#yields the x-axis vector component of bow 2d cross-section	 
		yRun     = wrkArrN[1]		#yields the sections length from aft to bow
		spanLoc2 = wrkArrN[2]		#yields the z-axis vector component
		outMsg = "____ self.horzStrut inComing Array z x\n"
		#250121_lu aaptool.prnVectors(prnFLAG4Vectors, outMsg,wrkArrN[2], wrkArrN[0])
		aaptool.prnVectors(1, outMsg,wrkArrN[2], wrkArrN[0])
		
		if self._sectionID == 1:		#using LES_Tower.py model
			v2 = self.intersection(wrkArrN[2], spanID)          # as spanLoc2
			v1 = targetTower.intersection(wrkArrN[0], spanID) #was spanLoc1
		elif self._sectionID ==2:	#using symmetric crossesction approach
			v2 = self.weldPoint(vLoc, pntNdx, spanID, 1)   #on targetItem but assuming symmetry of shape
			v1 = self.weldPoint(vLoc, pntNdx, spanID, 0)	#on chassisLeg
		outMsg = "self.horzStrut v2_4z and v1_4x\n"
		#250121_lu aaptool.prnVectors(prnFLAG4Vectors, outMsg,v2, v1)
		aaptool.prnVectors(1, outMsg,v2, v1)
		self.drawStrut(radius, v2, v1, wrkArrN[1],spanID) #yRun  spanID was 0
		#edge = Part.makeLine(v1, v2)
		#Part.show(edge)


	def vertStrut(self, targetTower, radius, vLoc, pntNdx, spanID):   # SpanLoc2, SpanLoc1, yRun,
		"""
		Need to resolve x and z axiz component of position
		"""
		np_Arr   = np.array(vLoc)
		wrkArrN   = np_Arr[pntNdx]
		spanLoc1 = wrkArrN[0]		#yields the x-axis vector component of bow 2d cross-section	 
		yRun     = wrkArrN[1]		#yields the sections length from aft to bow
		spanLoc2 = wrkArrN[2]		#yields the z-axis vector component
		if self._sectionID == 1:  #LES_Tower.py model
			v2 = self.intersection(wrkArrN[0], spanID) #as spanDoc1
			v1 = targetTower.intersection(wrkArrN[2], spanID)  #was SpanLoc2
		elif self._sectionID ==2:
			v2 = self.weldPoint(vLoc, pntNdx, spanID, 1)   #on targetItem but assuming symmetry of shape
			v1 = self.weldPoint(vLoc, pntNdx, spanID, 0)	#on chassisLeg
			outMsg = "self.vertStrut pre-drawStrut\n"
			aaptool.prnVectors(prnFLAG4Vectors, outMsg,v2, v1)
			aaptool.prnVectors(1, outMsg,v2, v1)
		self.drawStrut(radius, v2, v1, wrkArrN[1], spanID) # should be 3,4,5,6



	def buildStrut(self, targetTower, spanID, vLoc):
		"""
		Splits flow into bow and aft section 1 
		mid and RR section2 with appropriate 
		vLoc and flowID for processing 
		Provides index for reading vLoc elements
        """
		#if spanID == 1:# bow section
		#	ndx = 0
		if spanID == 1:# bow section
			loopNdx = 0	  # while loop counter
			arrayNdx = 0   # points to the polygon array vector
			while loopNdx < len(vLoc)-1:  # should not need the closing edge of polygon shape
				outMsg = 'top While bow buildStrut ndx: \n'
				aaptool.prnSingleVector(prnFLAGoneVector,loopNdx,outMsg)
				if loopNdx == 0:
					arrayNdx = 0
					self.horzStrut(targetTower, PIPE_3_5_RADIUS,  vLoc, arrayNdx, spanID)   #1 bow bottom horizontal span span_zpnt1,  span_xpnt1, sectionLength,
				elif loopNdx == 1:
					arrayNdx = 2
					self.vertStrut(targetTower, PIPE_3_5_RADIUS,  vLoc, arrayNdx, spanID+2) #3 bow span_vertical zpnt3,  span_xpnt3, sectionLength,
				elif loopNdx == 2:
					adjSpanID = 9 # bow horizontal lower strut
					outMsg = 'buildStrut 9 bow z from base\n'
					aaptool.prnSingleVector(prnFLAGoneVector,self._bow.z,outMsg)
					arrayNdx = 1	#see bow polygon description for second element
					self.horzStrut(targetTower, PIPE_3_5_RADIUS,  vLoc, arrayNdx, adjSpanID)   #9 bow upper span_zpnt2, -span_xpnt2, sectionLength,
				elif loopNdx ==3:
					arrayNdx = 3
					self.vertStrut(targetTower, PIPE_3_5_RADIUS,  vLoc, arrayNdx, spanID+3) #4 bow span_zpnt4, -span_xpnt4, sectionLength,
				outmsg ="bottom While bow buildStrut loopNdx: \n"
				aaptool.prnSingleVector(prnFLAGoneVector,loopNdx,outMsg)
				loopNdx += 1
		elif spanID == 2: # aft section
			ndx = 0
			loopNdx = 0	  # while loop counter
			arrayNdx = 0   # points to the polygon array vector
			while loopNdx < len(vLoc)-1:  # should neot need the closing edge of polygon shape
				if loopNdx == 0:
					arrayNdx = 0
					self.horzStrut(targetTower, PIPE_3_5_RADIUS, vLoc, arrayNdx, spanID)   #2 aft bottom horizontal span -span_zpnt,  span_xpnt, 0,
				elif loopNdx == 1:
					arrayNdx = 2				
					self.vertStrut(targetTower, PIPE_3_5_RADIUS, vLoc, arrayNdx, spanID+3) #5 aft vertical span -span_zpnt,  span_xpnt, 0,
				elif loopNdx == 2:
					arrayNdx = 1
					adjSpanID = 19 # bow horizontal lower strut
					outMsg = 'buildStrut 9 bow z from base\n'
					aaptool.prnSingleVector                                (prnFLAGoneVector,self._aft.z,outMsg)
					#aaptool.prnSingleVector                                (1,self._aft.z,outMsg)
					arrayNdx = 1	#see bow polygon description for second element
					self.horzStrut(targetTower, PIPE_3_5_RADIUS,  vLoc, arrayNdx, adjSpanID)   #19aft lower horizontal span  span_zpnt, -span_xpnt, 0,
				elif loopNdx ==3:
					arrayNdx = 3
					self.vertStrut(targetTower, PIPE_3_5_RADIUS, vLoc, arrayNdx, spanID+4)  #6 aft vertical span   span_zpnt, -span_xpnt, 0, 
				outMsg ="bottom While aft buildStrut loopNdx: \n"
				aaptool.prnSingleVector(prnFLAGoneVector,loopNdx,outMsg)
				loopNdx += 1
		#New Approach based on symetric crosssection assumption
		"""
		Need to decode vLoc four node points suc that the macro unwraps
			the shapes for a rectanlge ploygon as:
			upper horizontal, left vertical, lower horizontal, right vertical
			   [rectangle polygon
				pntNdx 0:  (-603.2674610449129, 0, -161.85224564619617), 20 horizontal upper
				pntNdx 1:  (603.2674610449129, 0, -161.85224564619617), 
				pntNdx 2:  (603.2674610449129, 0, 161.85224564619617), 
				pntNdx 3:  (-603.2674610449129, 0, 161.85224564619617),  29 horizontal lower
				pntNdx 4:  (-603.2674610449129, 0, -161.85224564619617)
   ]
		"""
		if spanID == 20:# MID section new numbering/index 
			loopNdx = 0	  # while loop counter
			arrayNdx = 0   # points to the polygon array vector
			while loopNdx < len(vLoc)-1:  # should not need the closing edge of polygon shape
				outMsg = "\ntop While bow buildStrut ndx: "
				aaptool.prnSingleVector(prnFLAGoneVector,vLoc,outMsg)
				if loopNdx == 0:
					arrayNdx = 0
					outMsg = "\nbuildStrut MID section Horizontal upper arrayNdx SpanID 20:\n"
					aaptool.prnSingleVector(prnFLAGoneVector,arrayNdx,outMsg)
					self.horzStrut(targetTower, PIPE_3_5_RADIUS,  vLoc, arrayNdx, spanID)   #1 mid bottom horizontal span span_zpnt1,  span_xpnt1, sectionLength,
				elif loopNdx == 1:
					arrayNdx = 1
					outMsg = "\nbuildStrut MID section arrayNdx SpanID 21\n"
					aaptool.prnSingleVector(prnFLAGoneVector,arrayNdx,outMsg)
					self.vertStrut(targetTower, PIPE_3_5_RADIUS,  vLoc, arrayNdx, spanID+1) #21 mid span_vertical zpnt3,  span_xpnt3, sectionLength,
				elif loopNdx == 2:
					adjSpanID = 29 # bow horizontal lower strut
					arrayNdx = 3 #see MID polygon description for second element
					outMsg = 'buildStrut 29 MID horizontal lower arrayNdx \n'
					aaptool.prnSingleVector(prnFLAGoneVector,arrayNdx,outMsg)
					self.horzStrut(targetTower, PIPE_3_5_RADIUS,  vLoc, arrayNdx, adjSpanID)   #29 mid upper span_zpnt2, -span_xpnt2, sectionLength,
				elif loopNdx ==3:
					arrayNdx = 4
					outMsg = "\nbuildStrut MID section SpanID 22\n"
					aaptool.prnSingleVector(prnFLAGoneVector,arrayNdx,outMsg)
					self.vertStrut(targetTower, PIPE_3_5_RADIUS,  vLoc, arrayNdx, spanID+2) #22 mid span_zpnt4, -span_xpnt4, sectionLength,
				outmsg ="bottom While MID buildStrut spanID: 22   loopndx: \n"
				aaptool.prnSingleVector(prnFLAGoneVector,loopNdx,outMsg)
				loopNdx += 1
		elif spanID == 30: # aft section
			ndx = 0
			loopNdx = 0	  # while loop counter
			arrayNdx = 0   # points to the polygon array vector
			while loopNdx < len(vLoc)-1:  # should neot need the closing edge of polygon shape
				if loopNdx == 0:
					arrayNdx = 0
					self.horzStrut(targetTower, PIPE_3_5_RADIUS, vLoc, arrayNdx, spanID)   #2 rr bottom horizontal span -span_zpnt,  span_xpnt, 0,
				elif loopNdx == 1:
					arrayNdx = 1				
					self.vertStrut(targetTower, PIPE_3_5_RADIUS, vLoc, arrayNdx, spanID+1) #31 rr vertical span -span_zpnt,  span_xpnt, 0,
				elif loopNdx == 2:
					adjSpanID = 39 # rr horizontal lower strut
					arrayNdx = 3	#see rr polygon description for second element
					outMsg = 'buildStrut 9 rr z from base\n'
					aaptool.prnSingleVector(prnFLAGoneVector,loopNdx,outMsg)
					self.horzStrut(targetTower, PIPE_3_5_RADIUS,  vLoc, arrayNdx, adjSpanID)   #39 rrr lower horizontal span  span_zpnt, -span_xpnt, 0,
				elif loopNdx ==3:
					arrayNdx = 4
					self.vertStrut(targetTower, PIPE_3_5_RADIUS, vLoc, arrayNdx, spanID+2)  #32 rrt vertical span   span_zpnt, -span_xpnt, 0, 
				outMsg = "RR buildStrut SpanID: 30    loopNdx: "	
				aaptool.prnSingleVector(prnFLAGoneVector,loopNdx,outMsg)
				loopNdx += 1


	def centerXZ_Poly(self, vLoc):  # 240808 was beam, draft ):
		#fixPoly =  Part.makePolygon([(-beam/2, 0, -draft/2), (beam/2, 0, -draft/2), (beam/2, 0, draft/2), (-beam/2, 0, draft/2), (-beam/2, 0, -draft/2)])   
		fixPoly =  Part.makePolygon(vLoc)   
		disk = Part.makeCircle(PIPE_3_5_RADIUS,)
		tube = fixPoly.extrude(App.Vector(0, 0, 2))	
		return fixPoly

#redfine and add tower legs 3 & 4
		"""
example adapted from https://www.w3schools.com/python/numpy/trypython.asp?filename=demo_numpy_array_index1
import numpy as np

beam = 8
draft = 5
vLoc = [(-beam, 0, -draft), (beam, 0, -draft), (beam, 0, draft), (-beam, 0, draft), (-beam, 0, -draft)]

arr = np.array(vLoc)

print(arr[1])  ==>> [ 8  0 -5]

		"""
	def adj_yRun_vLoc(self, vLoc, changeValue):
		np_Arr   = np.array(vLoc)
		pntNdx = 0	  # while loop counter
		while pntNdx < len(vLoc):
			wrkArrN   = np_Arr[pntNdx]
			spanLoc1 = wrkArrN[0]		#yields the x-axis vector component of bow 2d cross-section	 
			yRun     = wrkArrN[1]		#yields the sections length from aft to bow
			spanLoc2 = wrkArrN[2]		#yields the z-axis vector component
			adj_yRun_vLoc = self.fill_Loc(spanLoc1, spanLoc2, changeValue)
		return adj_yRunvLoc
	
	def fill_vLoc(self, beam, draft, sectionRun):
		vLoc = [(-beam, sectionRun, -draft), (beam, sectionRun, -draft), (beam, sectionRun, draft), (-beam, sectionRun, draft), (-beam, sectionRun, -draft)]
		return vLoc

	def build4RectanglePoly(self, beam, draft, sectionRun):
		vLoc = self.fill_vLoc(beam, draft, sectionRun)
		#240923_lu [(-beam, sectionRun, -draft), (beam, sectionRun, -draft), (beam, sectionRun, draft), (-beam, sectionRun, draft), (-beam, sectionRun, -draft)]
		#240923_lu polyNew = self.centerXZ_Poly(vLoc) # (beamSize, draftSize)
		#240923_lu polyNew.translate(App.Vector(0, -sectionRun, 0))
		#240923_lu 
		outMsg = "\nRectangle Polygon Vector Locations\n"
		aaptool.prnSingleVector(prnFLAGoneVector,vLoc,outMsg)
		#240923_lu polyNew.translate(App.Vector(0, sectionRun, 0))
		#240923_lu Part.show(polyNew)
		return vLoc


		"""
		Creates an appropriate location vector describing the bow cross-section
		Assign process flow ID for handling just the bow section
		Generates a helpful polyBow 2D rendering for placement
		during development
		"""

	def buildBowPoly(self, targetTower, beamSize, draftSize, sectionRun):
		vLoc = self.build4RectanglePoly(beamSize, draftSize, sectionRun)
		### testing 
		#240923_lu bow frame
		self.buildStrut(targetTower,1,vLoc) #beamSize, draftSize, sectionRun)
		

	def buildAftPoly(self, targetTower,beamSize, draftSize, sectionRun):
		vLoc = self.build4RectanglePoly(beamSize, draftSize, 0)  # want at originsectionRun)
		### testing 
		self.buildStrut(targetTower,2,vLoc) #beamSize, draftSize, sectionRun)beamSize, draftSize, sectionRun)

	def buildMIDPoly(self, targetTower,beamSize, draftSize, sectionRun):
		vLoc = self.build4RectanglePoly(beamSize, draftSize, 0)  #force to origin
		outMsg = "\nRectangle Polygon Vector MID section Locations\n"
		aaptool.prnSingleVector(prnFLAGoneVector,vLoc,outMsg)
		self.buildStrut(targetTower,20,vLoc) #beamSize, draftSize, sectionRun)beamSize, draftSize, sectionRun)


	def buildRRPoly(self, targetTower,beamSize, draftSize, sectionRun):
		#Adjust the bend to center line at Rear 
		vLoc = self.build4RectanglePoly(beamSize, draftSize, sectionRun)
		outMsg = "\nRectangle Polygon Vector RR section Locations\n"
		aaptool.prnSingleVector(prnFLAGoneVector,vLoc,outMsg)
		#aaptool.prnSingleVector(1,vLoc,outMsg)
		self.buildStrut(targetTower,30,vLoc) #beamSize, draftSize, sectionRun)beamSize, draftSize, sectionRun)


	

def frontChassisSection():
	
	Y1 = -CHASSIS_RUN   # CHASSIS_RUN negative from y-Origin to bow
	# 240623 Needed z1 to truly initialize TowerLeg object works seamlessly now
	subChassisID = 1
	#four shell-shapes created
	# Using /2 to build down the x,z-axis center line
	#  (aft values | bow values) (x2, y2, z2  x1, y1, z1 )                     	
	
	
	leg1 = ChassisLeg( CHASSIS_AFT_SPAN/2,  CHASSIS_AFT_RUN,  CHASSIS_AFT_DEPTH/2,   CHASSIS_BOW_SPAN/2, Y1,  CHASSIS_BOW_DEPTH/2, subChassisID)
	leg2 = ChassisLeg(-CHASSIS_AFT_SPAN/2,  CHASSIS_AFT_RUN,  CHASSIS_AFT_DEPTH/2,  -CHASSIS_BOW_SPAN/2, Y1,  CHASSIS_BOW_DEPTH/2, subChassisID)
	leg3 = ChassisLeg( CHASSIS_AFT_SPAN/2,  CHASSIS_AFT_RUN, -CHASSIS_AFT_DEPTH/2,   CHASSIS_BOW_SPAN/2, Y1, -CHASSIS_BOW_DEPTH/2, subChassisID)
	leg4 = ChassisLeg(-CHASSIS_AFT_SPAN/2,  CHASSIS_AFT_RUN, -CHASSIS_AFT_DEPTH/2,  -CHASSIS_BOW_SPAN/2, Y1, -CHASSIS_BOW_DEPTH/2, subChassisID)
	
	#mySolid = Part.makeSolid(myShell)
	"""  Essential for creating solid """
	leg1Solid = Part.makeSolid(leg1._tube)
	leg2Solid = Part.makeSolid(leg2._tube)
	leg3Solid = Part.makeSolid(leg3._tube)
	leg4Solid = Part.makeSolid(leg4._tube)
	Part.show(leg1Solid)
	Part.show(leg2Solid)
	Part.show(leg3Solid)
	Part.show(leg4Solid)
	'''' end of comment '''
	
	leg1.buildBowPoly(leg2,CHASSIS_BOW_SPAN/2,CHASSIS_BOW_DEPTH/2, -CHASSIS_RUN)
	leg1.buildAftPoly(leg2,CHASSIS_AFT_SPAN/2,CHASSIS_AFT_DEPTH/2, 0)
	
	#compensated for by the usage of buildstrut() with adjSpanID = 9
	#leg4.buildBowPoly(leg3,CHASSIS_BOW_SPAN/2,CHASSIS_BOW_DEPTH/2, CHASSIS_RUN)
	#leg4.buildAftPoly(leg3,CHASSIS_AFT_SPAN/2,CHASSIS_AFT_DEPTH/2, CHASSIS_RUN)
	


def rearChassisSection():
	YMID =  0  # CHASSIS_RR_RUN starts at origin and goes posiitve Y-Axis
	# 240623 Needed z1 to truly initialize TowerLeg object works seamlessly now
	# Using /2 to build down the x,z-axis center line
	#  (aft values | bow values) (x2, y2, z2  x1, y1, z1 )                     	
	subChassisID = 2
	leg10 = ChassisLeg( CHASSIS_MID_SPAN/2,  CHASSIS_RR_RUN,  CHASSIS_MID_DEPTH/2,   CHASSIS_RR_SPAN/2, YMID,  CHASSIS_RR_DEPTH/2, subChassisID)
	leg20 = ChassisLeg(-CHASSIS_MID_SPAN/2,  CHASSIS_RR_RUN,  CHASSIS_MID_DEPTH/2,  -CHASSIS_RR_SPAN/2, YMID,  CHASSIS_RR_DEPTH/2, subChassisID)
	leg30 = ChassisLeg( CHASSIS_MID_SPAN/2,  CHASSIS_RR_RUN, -CHASSIS_MID_DEPTH/2,   CHASSIS_RR_SPAN/2, YMID, -CHASSIS_RR_DEPTH/2, subChassisID)
	leg40 = ChassisLeg(-CHASSIS_MID_SPAN/2,  CHASSIS_RR_RUN, -CHASSIS_MID_DEPTH/2,  -CHASSIS_RR_SPAN/2, YMID, -CHASSIS_RR_DEPTH/2, subChassisID)

	
	#240820: Assuming a symmetric shape starboard to port with Y-axis centerline
	#	so leg30 can be ignored as opposed to LES_Tower.py.  Used
	#	intersect() for SpanID 1, 2, 9, and 19 of buildsrtut
	leg10.buildMIDPoly(leg20,CHASSIS_MID_SPAN/2,CHASSIS_MID_DEPTH/2, 0)
	#flip global variable CHASSIS_RR_RUN to negative for sectionRun
	#	played with yRun: CHASSIS_RR_RUN due to -sectionRun usage in buildPoygon xsecetion
	leg10.buildRRPoly(leg20,CHASSIS_RR_SPAN/2,CHASSIS_RR_DEPTH/2,-CHASSIS_RR_RUN)  
	
#frontChassisSection()
#rearChassisSection()

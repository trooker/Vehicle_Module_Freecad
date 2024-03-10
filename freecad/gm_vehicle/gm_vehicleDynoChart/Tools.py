#***************************************************************************
#*                                                                         *
#*
#*   Copyright (c) 2023 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
#*   
#*   Used general Ship flow for Tools.py substituting gm_vehicle content     *
#*                                                                         *
#*   Copyright (c) 2011, 2016 Jose Luis Cercos Pita <jlcercos@gmail.com>   *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************
"""
240220_tr  For readbility the various Point_* classes do not seek to consolidate common
               placement order of the incoming data.  
            A future tweak could be made to accomplish this minor task.  
"""
import math
import random
from FreeCAD import Vector, Rotation, Matrix, Placement
import Part
from FreeCAD import Units
import FreeCAD as App
try:
    import FreeCADGui as Gui
except ImportError:
    pass
from .. import Instance
from ..gm_vehicleUtils import Math


DENS = Units.parseQuantity("1025 kg/m^3")  # Salt water
COMMON_BOOLEAN_ITERATIONS = 10



class Point_dyno:
    def __init__(self, gm_vehicle, rpm, torque, pwr):
        # Create data storage bin
        self.rpm      = rpm
        self.torque    = torque 
        self.rpm       = rpm


        

class Point_axlTrq:                 # B       E       C       D       F         G
    """
    Defineds a single point with seven columns from a spreadsheet
        using the order   B   E   C   D    F.   G     **
        The unique column names can be self.what_ever in this code module
        since the PlotAux_* redefines the work version as it is read-in to the 
        module.
        ** There is no assignable Axle Speed for AWD for assumed straight
            and level hardsurface travel.  No AWDRpm was acquired from 
            Cascadia Motion EVBot graphs.
            self.awdrpm  = fwdrpm   # either fwdrpm or rwdrpm  
                             axle rpm do not sum
    """
    def __init__(self, gm_vehicle, gndspd, awdtrq, fwdtrq, rwdtrq, awdrpm, fwdrpm, rwdrpm):
        # Create data storage bin
        # for Axle Troque and Axle Speed for FWD, RWD, and AWD::just the torque
        self.gndspd   = gndspd
        self.awdtrq   = awdtrq 
        self.fwdtrq   = fwdtrq
        self.rwdtrq   = rwdtrq
        self.awdrpm  = fwdrpm   # either fwdrpm or rwdrpm  axle rpm do not sum
        self.fwdrpm  = fwdrpm
        self.rwdrpm  = rwdrpm

class Point_vehFrc:                 # B       E       C       D       F          
    """
    Defineds a single point with five columns from a spreadsheet
        using the order   B   E   C   D    F.
        The unique column names can be self.what_ever in this code module
        since the PlotAux_* redefines the work version as it is read-in to the 
        module.
    """
    def __init__(self, gm_vehicle, gndspd, awdfrc, fwdfrc, rwdfrc, awdcdg):
        # Create data storage bin
        # for Axle Troque and Axle Speed for FWD, RWD, and AWD::just the torque
        self.gndspd   = gndspd
        self.awdfrc   = awdfrc 
        self.fwdfrc   = fwdfrc
        self.rwdfrc   = rwdfrc
        self.awdcdg  = awdcdg
 
class Point_whlPwr:                 # B       E       C       D       F         G      
    """
    Defineds a single point with six columns from a spreadsheet
        using the order   B   E   C   D    F.
        The unique column names can be self.what_ever in this code module
        since the PlotAux_* redefines the work version as it is read-in to the 
        module.
    """
    def __init__(self, gm_vehicle, gndspd, awdpwr, fwdpwr, rwdpwr, rbatlim, fbatlim):
        self.gndspd   = gndspd
        self.awdpwr   = awdpwr 
        self.fwdpwr   = fwdpwr
        self.rwdpwr   = rwdpwr
        self.rbatlim   = rbatlim
        self.fbatlim   = fbatlim
 

class Point_accTrc:                 # B       E       C       D       F         G
    """
    Defineds a single point with seven columns from a spreadsheet
        using the order   B   E   C   D    F.   G     **
        The unique column names can be self.what_ever in this code module
        since the PlotAux_* redefines the work version as it is read-in to the 
        module.
        ** There is no assignable Axle Speed for AWD for assumed straight
            and level hardsurface travel.  No AWDRpm was acquired from 
            Cascadia Motion EVBot graphs.
           fwdtrc and rwdtrc differ due to front wheel to rear wheel weight distribution  
           awdtrc is not relevent
    """
    def __init__(self, gm_vehicle, gndspd, awdacc, fwdacc, rwdacc, fwdtrc, rwdtrc):
        # Create data storage bin
        # for Axle Troque and Axle Speed for FWD, RWD, and AWD::just the torque
        self.gndspd   = gndspd
        self.awdacc   = awdacc 
        self.fwdacc   = fwdacc
        self.rwdacc   = rwdacc
        self.awdtrc  = fwdtrc   # either fwdtrc or rwdtrc  axle trc do not sum
        self.fwdtrc  = fwdtrc
        self.rwdtrc  = rwdtrc



class Point_batCap:                 # A      C       E       C       D       F         G    H
    """
    Defineds a single point with seven columns from a spreadsheet
        using the order   B   E   C   D    F.   G     H **
        The unique column names can be self.what_ever in this code module
        since the PlotAux_* redefines the work version as it is read-in to the 
        module.
        ** There is no assignable Axle Speed for AWD for assumed straight
            and level hardsurface travel.  No AWDRpm was acquired from 
            Cascadia Motion EVBot graphs.
           fwdtrc and rwdtrc differ due to front wheel to rear wheel weight distribution  
           awdtrc is not relevent
    """
    def __init__(self, gm_vehicle, cellcur, cellvolt, pekpwr, vsag, pckcur, pckvolt, mopwr, modui):
        # Create data storage bin
        # for Axle Troque and Axle Speed for FWD, RWD, and AWD::just the torque
        self.cellcur   = cellcur
        self.cellvolt   = cellvolt 
        self.pekpwr    = pekpwr
        self.vsag       = vsag
        self.pckcur     = pckcur   # either fwdtrc or rwdtrc  axle trc do not sum
        self.pckvolt    = pckvolt
        self.mopwr    = mopwr
        self.modui      = modui


#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2023, 2024 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
#*                                                                         *
#*   Used general Ship flow for GM_VehicleGui.py substituting gm_vehicle content     *
#*
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
#* 
#* SeeShipGui.py for template                                                                        *
#***************************************************************************

import FreeCAD as App
import FreeCADGui 
import os

from . import GM_Vehicle_rc
from .gm_vehicleUtils import Selection
#from . import Ship_rc
# redundant  from .gm_vehicleUtils import Selection


#FreeCADGui.addLanguagePath(":/GM_Vehicle/translations")  TBD
FreeCADGui.addIconPath(":/resources/icons")


def QT_TRANSLATE_NOOP(context, text):
   return text


class LoadExample:
    def Activated(self):
        from . import gm_vehicleLoadExample
        App.Console.PrintMessage("GM: LoadExample imported \n")
        gm_vehicleLoadExample.load()
        App.Console.PrintMessage("GM: LoadExample loaded \n")

    def GetResources(self):
        MenuText = 'Load a new GM_Vehicle example'
        ToolTip   = 'Load an example of a Wheeled Ground Mobile Vehicle rolling chassis'
        App.Console.PrintMessage("GM_VehicleGUI: LoadExample() retrun from Resources doit\n")
        

        return {'Pixmap': 'GM_Vehicle_Load',     # GM_Vehicle_Load
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class CreateGM_Vehicle:
    def IsActive(self):
        return bool(Selection.get_solids())

    def Activated(self):
        from . import gm_vehicleCreateGM_Vehicle
        gm_vehicleCreateGM_Vehicle.load()


    def GetResources(self):
        MenuText = 'Create a new GM_Vehicle'
        ToolTip   = 'Create a new Wheeled Ground Mobile Vehicle rolling chassis'
        App.Console.PrintMessage("GM_VehicleGui.py CreateGM_Vehicle() retrun from Resources doit\n")
        return {'Pixmap': 'GM_Vehicle_Module',           # works with Ship  but not  GM_Vehicle_Module',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class DynoChart:
    def IsActive(self):
        return bool(Selection.get_objects()) # for dev only bool(Selection.get_ships())

    def Activated(self):
        from . import gm_vehicleDynoChart  #shipHydrostatics
        gm_vehicleDynoChart.load()  #shipHydrostatics.load()

    def GetResources(self):
        MenuText = 'Dyno Chart'
        ToolTip =  'Plot the vehicle dyno chart'
        App.Console.PrintMessage("Accessing Dyno Chart :: TBD ")        
        return {'Pixmap': 'GM_Vehicle_DynoChart',  #corrected Vehicle ommission
                'MenuText': MenuText,
                'ToolTip': ToolTip}


class WebEVBot:
    def IsActive(self):
        return bool(Selection.get_objects()) # for dev only bool(Selection.get_ships())

    def Activated(self):
        from . import gm_vehicleWebEVBot  #shipHydrostatics
        gm_vehicleWebEVBot.load()  #shipHydrostatics.load()

    def GetResources(self):
        MenuText = 'Access Cascadia Motion EVBot App'
        ToolTip =  'Maximize FC! CloseCombo/Tree Panel to engage EVBot Tool'
        App.Console.PrintMessage("Rendering Cascadia Motion EVBot Design Tool")  
        App.Console.PrintMessage(ToolTip)       
        return {'Pixmap': 'WebEVBot',  
                'MenuText': MenuText,
                'ToolTip': ToolTip}



FreeCADGui.addCommand('GM_Vehicle_LoadExample', LoadExample())
FreeCADGui.addCommand('GM_Vehicle_CreateGM_Vehicle', CreateGM_Vehicle())
FreeCADGui.addCommand('GM_Vehicle_DynoChart',DynoChart ())
FreeCADGui.addCommand('GM_Vehicle_WebEVBot',WebEVBot ())

#FreeCADGui.addCommand('Ship_Hydrostatics', Hydrostatics())


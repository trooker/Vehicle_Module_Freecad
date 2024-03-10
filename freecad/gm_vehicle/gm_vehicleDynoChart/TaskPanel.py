#***************************************************************************
#*   
#*   Copyright (c) 2023...2024 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
#*   
#*   Used general Ship flow for Task.py substituting gm_vehicle content     *
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

import math
import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Base, Vector
import Part
from FreeCAD import Units
from PySide import QtGui, QtCore
from . import PlotAux_01_fntDyno
from . import PlotAux_02_rrDyno
from . import PlotAux_03_axlTrq
from . import PlotAux_04_vehForces
from . import PlotAux_05_whlPwr
from . import PlotAux_06_accTrc
from . import PlotAux_07_fntBat
from . import PlotAux_08_rrBat

from . import Tools
from .. import Instance
from .. import GM_Vehicle_rc  # replaces Ship_rc
from ..gm_vehicleUtils import Locale
from ..gm_vehicleUtils import Selection
#implement post desgin from ..init_gui import QT_TRANSLATE_NOOP


class TaskPanel:
    def __init__(self):
        self.name = "gm_vehicle dyno chart plotter"
        self.ui = ":/ui/TaskPanel_gm_vehicleDynoChart.ui"
        self.form = Gui.PySideUic.loadUi(self.ui)
        self.gm_vehicle = None    # was ship
        self.running = False
        # zero based list of charts/plots/graphs
        self.menuList = ["fntDyno", "rrDyno", "axlTrq", "vehFrc", "whlPwr", "accTrc", "fntBat", "rrBat"]

    def accept(self):
        if not self.gm_vehicle:     # was ship
            return False
        if self.running:
            return
        #self.form.group_pbar.show()
        self.save()
		##********
        n_minimum = 2 #DEV 240209 start with the third row or nbr 2 (0,1,2: thr third row
        n_draft = self.form.spinbx_Rows.value() + 1 #DEV 240209 skip the first two rows of each spreadsheet
		
        if (self.form.chkbx_FntMotorDyno.isChecked() == True): 
            #PlotAux_01_fntDyno
            menuId0 = self.menuList[0]  #fntDyno
            msg = "Fire Front Motor Dyno Chart Plot"
            App.Console.PrintMessage(msg + '\n')
            self.doDynoCharts(menuId0, n_draft, n_minimum)
        if (self.form.chkbx_RrMotorDyno.isChecked() == True):
            #PlotAux_02_rrDyno
            menuId1 = self.menuList[1]  #rrDyno
            msg = "Fire Rear Motor Dyno Chart Plot"
            App.Console.PrintMessage(msg + '\n')
            self.doDynoCharts(menuId1, n_draft, n_minimum)
        if (self.form.chkbx_AxleTorque.isChecked() ==True):
            menuId2 = self.menuList[2]  #"axlTrq"
            msg = "Fire Axle Torque Plot"
            App.Console.PrintMessage(msg + '\n')
            self.doAxleTorqueChart(menuId2, n_draft, n_minimum) 
        if (self.form.chkbx_VehForces.isChecked() ==True):
            menuId3 = self.menuList[3]  #"vehFrc"
            msg = "Fire Vehicle Forces and Drag Force Plot"
            App.Console.PrintMessage(msg + '\n')
            self.doVehForcesChart(menuId3, n_draft, n_minimum) 
        if (self.form.chkbx_WheelPwr.isChecked() ==True):
            menuId4 = self.menuList[4]  #"whlPwr"
            msg = "Fire Wheel Power - Battery Limit Plot"
            App.Console.PrintMessage(msg + '\n')
            self.doWheelPwrChart(menuId4, n_draft, n_minimum) 
        if (self.form.chkbx_AccelTraction.isChecked() ==True):
            menuId5 = self.menuList[5]  #"accTrc"
            msg = "Fire Acceleration and Traction Plot"
            App.Console.PrintMessage(msg + '\n')
            self.doAccelTractionChart(menuId5, n_draft, n_minimum) 
        if (self.form.chkbx_FnBatteryCapa.isChecked() == True):
            menuId6 = self.menuList[6]  #"fntBat"
            msg = "Fire Front Battery Capbility Plot"
            App.Console.PrintMessage(msg + '\n')
            self.dofntBatChart(menuId6, n_draft, n_minimum) 
        if (self.form.chkbx_RrBatteryCapa.isChecked() ==True):
            menuId7 = self.menuList[7]  #"rrBat"
            msg = "Fire Rear Battery Capbility Plot"
            App.Console.PrintMessage(msg + '\n')
            self.dorrBatChart(menuId7, n_draft, n_minimum) 
                       
        return True
     


        
		##********        
        """ may not need
        """
    def  doDynoCharts(self, menuId_in, n_draft, n_minimum):       
        """
        Dyno Charts have torque and power as function of rpm
        x-axis as RPM
        y-axis as torque and power
        process handles three columns
        As long as Front and Rear DynoCharts have same Y -axis Torque * Power
            The X-Axis must remain RPM.  Otherwise a new category of chart/plot
            will need to be generated
        """
        msg = "Dev: Accept Creating dyno chart plot"
        App.Console.PrintMessage(msg + '...\n')
        points = []
        plt = None
        # Process for Dyno Charts Front & Rear Motors       
        for i in range(n_draft):   #len(drafts)):
            # 240208   self.form.pbar.setValue(i + 1)
            point = Tools.Point_dyno(self.gm_vehicle, 0, 0, 0) #DEV 240209  added 0,'s  and don't need:   ,
            points.append(point)
         
         #240207 reshuffled from above  trying to drive plot   
        if plt is None:
            msg = "Dev: plt = None."
            App.Console.PrintMessage(msg + '...\n')
            # DEV 240213   _01_fntMotorDyno
            msg = "menuId_in: " +  menuId_in
            App.Console.PrintMessage(msg + '...\n')
            if menuId_in == "fntDyno":
                msg = "Graph Front Dyno."
                App.Console.PrintMessage(msg + '...\n')
                plt = PlotAux_01_fntDyno.Plot(self.gm_vehicle, points)
            if menuId_in == "rrDyno":                   
                msg = "Graph Rear Dyno."
                App.Console.PrintMessage(msg + '...\n')
                plt = PlotAux_02_rrDyno.Plot(self.gm_vehicle, points)               
        else:
            msg = "Dev: plt is active."
            App.Console.PrintMessage(msg + '...\n')
            plt.update(self.gm_vehicle)  #240207  , points)
           
        return True


        
    def doAxleTorqueChart(self, menuId_in, n_draft, n_minimum): 
        """
        FWD, RWD, AWD Axle Torque and RPM are displayed as a function of Ground Speed
            for the given designed vehicle (weight, drag, and propulsion) assuming flat hard surface.
        """
        msg = "Dev: Accept Creating Axle Torque & Speed plot"
        App.Console.PrintMessage(msg + '...\n')
        points = []
        plt = None
        # Process for Dyno Charts Front & Rear Motors       
        for i in range(n_draft):   #len(drafts)):
            # 240208   self.form.pbar.setValue(i + 1)
            point = Tools.Point_axlTrq(self.gm_vehicle, 0, 0, 0, 0, 0, 0, 0) #DEV 240209  added 0,'s  and don't need:   ,
            points.append(point)
         
         #240207 reshuffled from above  trying to drive plot   
        if plt is None:
            msg = "Dev: plt = None."
            App.Console.PrintMessage(msg + '...\n')
            # DEV 240213   _01_fntMotorDyno
            msg = "menuId_in: " +  menuId_in
            App.Console.PrintMessage(msg + '...\n')
            if menuId_in == "axlTrq":
                msg = "Graph Axle Torque & Speed of Vehicle"
                App.Console.PrintMessage(msg + '...\n')
                plt = PlotAux_03_axlTrq.Plot(self.gm_vehicle, points)
               
            """    
            ##Hold for another six column plot
            if menuId_in == "rrDyno":                   
                msg = "Graph Rear Dyno."
                App.Console.PrintMessage(msg + '...\n')
                plt = PlotAux_02_rrDyno.Plot(self.gm_vehicle, points)      
            """             
        else:
            msg = "Dev: plt is active."
            App.Console.PrintMessage(msg + '...\n')
            plt.update(self.gm_vehicle)  #240207  , points)

        return True

    def doVehForcesChart(self, menuId_in, n_draft, n_minimum):
        """
        FWD, RWD, AWD Axle Torque and RPM are displayed as a function of Ground Speed
            for the given designed vehicle (weight, drag, and propulsion) assuming flat hard surface.
        """
        msg = "Dev: Accept Creating vehicle force plot"
        App.Console.PrintMessage(msg + '...\n')
        points = []
        plt = None
        # Process for Dyno Charts Front & Rear Motors       
        for i in range(n_draft):   #len(drafts)):
            # 240208   self.form.pbar.setValue(i + 1)
            point = Tools.Point_vehFrc(self.gm_vehicle, 0, 0, 0, 0, 0) #DEV 240209  added 0,'s  and don't need:   ,
            points.append(point)
         
         #240207 reshuffled from above  trying to drive plot   
        if plt is None:
            msg = "Dev: plt = None."
            App.Console.PrintMessage(msg + '...\n')
            # DEV 240213   _01_fntMotorDyno
            msg = "menuId_in: " +  menuId_in
            App.Console.PrintMessage(msg + '...\n')
            if menuId_in == "vehFrc":
                msg = "Graph Forces Acting on Vehicle"
                App.Console.PrintMessage(msg + '...\n')
                plt = PlotAux_04_vehForces.Plot(self.gm_vehicle, points)
        else:
            msg = "Dev: plt is active."
            App.Console.PrintMessage(msg + '...\n')
            plt.update(self.gm_vehicle)  #240207  , points)

        return True

 
 
    def doWheelPwrChart(self, menuId_in, n_draft, n_minimum):
        """
        FWD, RWD, AWD Axle Torque and RPM are displayed as a function of Ground Speed
            for the given designed vehicle (weight, drag, and propulsion) assuming flat hard surface.
        """
        msg = "Dev: Accept Creating Axle Torque & Speed plot"
        App.Console.PrintMessage(msg + '...\n')
        points = []
        plt = None
        # Process for Dyno Charts Front & Rear Motors       
        for i in range(n_draft):   #len(drafts)):
            # 240208   self.form.pbar.setValue(i + 1)
            point = Tools.Point_whlPwr(self.gm_vehicle, 0, 0, 0, 0, 0, 0) #DEV 240209  added 0,'s  and don't need:   ,
            points.append(point)
         
         #240207 reshuffled from above  trying to drive plot   
        if plt is None:
            msg = "Dev: plt = None."
            App.Console.PrintMessage(msg + '...\n')
            # DEV 240213   _01_fntMotorDyno
            msg = "menuId_in: " +  menuId_in
            App.Console.PrintMessage(msg + '...\n')
            if menuId_in == "whlPwr":
                msg = "Graph Axle Torque & Speed of Vehicle"
                App.Console.PrintMessage(msg + '...\n')
                plt = PlotAux_05_whlPwr.Plot(self.gm_vehicle, points)
        else:
            msg = "Dev: plt is active."
            App.Console.PrintMessage(msg + '...\n')
            plt.update(self.gm_vehicle)  #240207  , points)

        return True

 
    def doAccelTractionChart(self, menuId_in, n_draft, n_minimum):
        """
        FWD, RWD, AWD Acceleration and Traction are displayed as a function of Ground Speed
            for the given designed vehicle (weight, drag, and propulsion) assuming flat hard surface.
        """
        msg = "Dev: Accept Creating Acceleration and Traction plot"
        App.Console.PrintMessage(msg + '...\n')
        points = []
        plt = None
        # Process for Acceleration & Traction       
        for i in range(n_draft):   #len(drafts)):
            # 240208   self.form.pbar.setValue(i + 1)
            point = Tools.Point_accTrc(self.gm_vehicle, 0, 0, 0, 0, 0, 0) #DEV 240209  added 0,'s  and don't need:   ,
            points.append(point)
         
         #240207 reshuffled from above  trying to drive plot   
        if plt is None:
            msg = "Dev: plt = None."
            App.Console.PrintMessage(msg + '...\n')
            # DEV 240213   _01_fntMotorDyno
            msg = "menuId_in: " +  menuId_in
            App.Console.PrintMessage(msg + '...\n')
            if menuId_in == "accTrc":
                msg = "Graph Acceleration & Traction of Vehicle"
                App.Console.PrintMessage(msg + '...\n')
                plt = PlotAux_06_accTrc.Plot(self.gm_vehicle, points)
        else:
            msg = "Dev: plt is active."
            App.Console.PrintMessage(msg + '...\n')
            plt.update(self.gm_vehicle, points)

        return True
 
 
    def dofntBatChart(self, menuId_in, n_draft, n_minimum):
        msg = "Dev: Accept Creating Front Battery Capability plot"
        App.Console.PrintMessage(msg + '...\n')
        points = []
        plt = None
        # Process for  Front Battery Capability      
        for i in range(n_draft):   #len(drafts)):
            # 240208   self.form.pbar.setValue(i + 1)
            point = Tools.Point_batCap(self.gm_vehicle, 0, 0, 0, 0, 0, 0, 0, 0) #DEV 240209  added 0,'s  and don't need:   ,
            points.append(point)
         
         #240207 reshuffled from above  trying to drive plot   
        if plt is None:
            msg = "Dev: plt = None."
            App.Console.PrintMessage(msg + '...\n')
            # DEV 240213   _01_fntMotorDyno
            msg = "menuId_in: " +  menuId_in
            App.Console.PrintMessage(msg + '...\n')
            if menuId_in == "fntBat":
                msg = "Graph Front Battery Capability "
                App.Console.PrintMessage(msg + '...\n')
                plt = PlotAux_07_fntBat.Plot(self.gm_vehicle, points)
        else:
            msg = "Dev: plt is active."
            App.Console.PrintMessage(msg + '...\n')
            plt.update(self.gm_vehicle)  #240207  , points)

        return True

 
    def dorrBatChart(self, menuId_in, n_draft, n_minimum):
        msg = "Dev: Accept Creating Front Battery Capability plot"
        App.Console.PrintMessage(msg + '...\n')
        points = []
        plt = None
        # Process for  Front Battery Capability      
        for i in range(n_draft):   #len(drafts)):
            # 240208   self.form.pbar.setValue(i + 1)
            point = Tools.Point_batCap(self.gm_vehicle, 0, 0, 0, 0, 0, 0, 0, 0) #DEV 240209  added 0,'s  and don't need:   ,
            points.append(point)
         
         #240207 reshuffled from above  trying to drive plot   
        if plt is None:
            msg = "Dev: plt = None."
            App.Console.PrintMessage(msg + '...\n')
            # DEV 240213   _01_fntMotorDyno
            msg = "menuId_in: " +  menuId_in
            App.Console.PrintMessage(msg + '...\n')
            if menuId_in == "rrBat":
                msg = "Graph Rear Battery Capability "
                App.Console.PrintMessage(msg + '...\n')
                plt = PlotAux_08_rrBat.Plot(self.gm_vehicle, points)
        else:
            msg = "Dev: plt is active."
            App.Console.PrintMessage(msg + '...\n')
            plt.update(self.gm_vehicle)  #240207  , points)

        return True 


    def reject(self):
        if not self.gm_vehicle:   # was ship
            return False
        if self.running:
            self.running = False
            return
        return True

    def clicked(self, index):
        pass

    def open(self):
        pass

    def needsFullSpace(self):
        return True

    def isAllowedAlterSelection(self):
        return False

    def isAllowedAlterView(self):
        return True

    def isAllowedAlterDocument(self):
        return False

    def helpRequested(self):
        pass

    def setupUi(self):
        self.form.chkbx_FntMotorDyno = self.widget(QtGui.QCheckBox, "chkbx_FntMotorDyno")		
        if (self.form.chkbx_FntMotorDyno.isChecked() == True): 
            msg = "setupUi: Fire Front Motor Dyno Chart Plot"
            App.Console.PrintMessage(msg + '\n')
        self.form.chkbx_RrMotorDyno = self.widget(QtGui.QCheckBox, "chkbx_RrMotorDyno")		
        if (self.form.chkbx_RrMotorDyno.isChecked() == True): 
            msg = "setupUi: Fire Rear Motor Dyno Chart Plot"
            App.Console.PrintMessage(msg + '\n')
        self.form.chkbx_FnBatteryCapa = self.widget(QtGui.QCheckBox, "chkbx_FnBatteryCapa")		
        if (self.form.chkbx_FnBatteryCapa.isChecked() == True): 
            msg = "setupUi: Fire Front Battery Capability Plot"
            App.Console.PrintMessage(msg + '\n')
        self.form.chkbx_RrBatteryCapa = self.widget(QtGui.QCheckBox, "chkbx_RrBatteryCapa")		
        if (self.form.chkbx_RrBatteryCapa.isChecked() == True): 
            msg = "setupUi: Fire Rear Battery Capability Plot"
            App.Console.PrintMessage(msg + '\n')
        self.form.chkbx_AccelTraction = self.widget(QtGui.QCheckBox, "chkbx_AccelTraction")		
        if (self.form.chkbx_AccelTraction.isChecked() == True): 
            msg = "setupUi: Fire Acceleration - Traction Plot"
            App.Console.PrintMessage(msg + '\n')
        self.form.chkbx_AxleTorque = self.widget(QtGui.QCheckBox, "chkbx_AxleTorque")		
        if (self.form.chkbx_AxleTorque.isChecked() == True): 
            msg = "setupUi: Fire Axle Torque Plot"
            App.Console.PrintMessage(msg + '\n')
        self.form.chkbx_VehForces = self.widget(QtGui.QCheckBox, "chkbx_VehForces")	
        if (self.form.chkbx_VehForces.isChecked() == True): 
            msg = "setupUi: Fire Vehicle Forces Plot"
            App.Console.PrintMessage(msg + '\n')
        self.form.chkbx_WheelPwr = self.widget(QtGui.QCheckBox, "chkbx_WheelPwr")	
        if (self.form.chkbx_WheelPwr.isChecked() == True): 
            msg = "setupUi: Fire Wheel Power Plot"
            App.Console.PrintMessage(msg + '\n')
        

        msg = "Dev: just prior to self.initValues function call"
        App.Console.PrintMessage(msg + '\n')

        # Initial values
        if self.initValues():
            return True
        msg = "Dev: just above QtCore.QObject.connect"
        App.Console.PrintMessage(msg + '\n')

        # Connect Signals and Slots
        QtCore.QObject.connect(self.form.chkbx_FntMotorDyno,
                               QtCore.SIGNAL("valueChanged(const Base::Quantity&)"),
                               self.onData)
        msg = "Dev:  Just after connect for Front Motor Dyno"
        App.Console.PrintMessage(msg + '\n')

        QtCore.QObject.connect(self.form.chkbx_RrMotorDyno,
                               QtCore.SIGNAL("valueChanged(const Base::Quantity&)"),
                               self.onData)
        msg = "Dev: Just after connect for Rear Motor Dyno"
        App.Console.PrintMessage(msg + '\n')

    def getMainWindow(self):
        toplevel = QtGui.QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                return i
        raise RuntimeError("No main window found")

    def widget(self, class_id, name):
        """Return the selected widget.

        Keyword arguments:
        class_id -- Class identifier
        name -- Name of the widget
        """
        mw = self.getMainWindow()            
        form = mw.findChild(QtGui.QWidget, "DynoChartTaskPanel")
        return form.findChild(class_id, name)

    def initValues(self):
        """ Set initial values for fields
            ship or gm_vehicle are instances of objects
        """
        msg = "Dev: initValues"
        App.Console.PrintMessage(msg + '\n')
 
        sel_objects = Selection.get_objects()    # was ship plural
        if not sel_objects:
            msg = "A object instance must be selected before using this tool"
            App.Console.PrintError(msg + '\n')
            return True
        self.gm_vehicle = sel_objects[0]
        msg = "Dev: self.gm_vehicle = sel_objects[0]"
        App.Console.PrintMessage(msg + '\n')
        if len(sel_objects) > 1:
            msg = "More than one object have been selected (just the one labelled '{}' is considered)".format(self.gm_vehicle.Label)
            App.Console.PrintWarning(msg + '\n')
        return False

    def clampValue(self, widget, val_min, val_max, val):
        pass

    def onData(self, value):
        pass
                
    def save(self):
        pass
                
    def lineFaceSection(self, line, surface):
        pass
    def externalFaces(self, shape):
        pass


def createTask():
    panel = TaskPanel()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
        Gui.Control.closeDialog()
        return None
    return panel

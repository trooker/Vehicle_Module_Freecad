#***************************************************************************
#*  
#*   Copyright (c) 2024 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
#*                                                                       *
#*   Used general Ship flow for TaskPanel.py substituting gm_vehicle content     *
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
#*                                                                         *
#***************************************************************************

import FreeCAD as App
import FreeCADGui as Gui
import Web
import WebGui
from PySide import QtGui, QtCore
from .. import GM_Vehicle_rc
#from ..gm_vehicleUtils import Paths


class TaskPanel:
    def __init__(self):
        self.name = "Launch Cascadia Motion EVBot Design Tool"
        self.ui = ":/ui/TaskPanel_gm_vehicleEVBot.ui"
        self.form = Gui.PySideUic.loadUi(self.ui)
        App.Console.PrintMessage("Launching EVBot.  Close Combo/Tree Panel and Maximize FC Window\n")
        WebGui.openBrowser('https://www.cascadiamotion.com/evbot')

    def accept(self):
        ""'Handles Ok Button""'
        return True

    def reject(self):
        '""Handles Cancel Button""'
        return True



    def setupUi(self):
        """Setup the task panel user interface."""                
        self.form.gm_vehicle = self.widget(QtGui.QGroupBox, "GM_VehicleProcessBox")
        self.form.mainLogo = self.widget(QtGui.QLabel, "MainLogo")
        self.form.mainLogo.setPixmap(QtGui.QPixmap(":/icons/WebEVBot.svg"))


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
        form = mw.findChild(QtGui.QWidget, "TaskPanel")
        return form.findChild(class_id, name)



def createTask():
    panel = TaskPanel()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
       Gui.Control.closeDialog()
       return None
    return panel

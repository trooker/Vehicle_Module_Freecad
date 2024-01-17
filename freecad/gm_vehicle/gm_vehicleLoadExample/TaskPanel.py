#***************************************************************************
#*  
#*   Copyright (c) 2023 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
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
from PySide import QtGui, QtCore
from .. import GM_Vehicle_rc
from ..gm_vehicleUtils import Paths


class TaskPanel:
    def __init__(self):
        self.name = "Example gm_vehicle loader"
        self.ui = ":/ui/TaskPanel_gm_vehicleLoadExample.ui"
        self.form = Gui.PySideUic.loadUi(self.ui)

    def accept(self):
        """Load the selected gm_vehicle example."""
        path = Paths.modulePath() + "/resources/examples/"
        if(self.form.gm_vehicle.currentIndex() == 0):   # Areil Nomad
            App.open(path + "aao_gm_vehicle_basic_ready.FCStd")
        elif(self.form.gm_vehicle.currentIndex() == 1):   # Areil Nomad
            App.open(path + "057_004_009_999_nomad_stl.FCStd")
        elif(self.form.gm_vehicle.currentIndex() == 2):   # Hog Jackson Weapons Platoform
            App.open(path + "057_004_999_998_hogJackson_FWD.FCStd")
        elif(self.form.gm_vehicle.currentIndex() == 3):   # Tabby
            App.open(path + "022_998_2seat_tabbyChassis.FCStd")
        return True

    def reject(self):
        """Cancel the job"""
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
        """Setup the task panel user interface."""
        self.form.gm_vehicle = self.widget(QtGui.QComboBox, "GM_VehicleLdExamples")
        self.form.mainLogo = self.widget(QtGui.QLabel, "MainLogo")
        self.form.mainLogo.setPixmap(QtGui.QPixmap(":/icons/GM_Vehicle_Logo.svg"))
        ## 231210_tr disregard self.retranslateUi()

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
'''
231210_tr disregard 
    def retranslateUi(self):
        """Set the user interface locale strings."""
        ##231209 self.form.setWindowTitle(App.Qt.translate("gm_vehicle_load", "Load example gm_vehicle"))
        self.form.setWindowTitle("Load example gm_vehicle")
        ##self.widget(QtGui.QGroupBox, "GM_VehicleSelectionBox").setTitle(
        ##    App.Qt.translate("gm_vehicle_load", "Select gm_vehicleexample geometry"))
        self.widget("GM_VehicleSelectionBox").setTitle("gm_vehicle_load", "Select gm_vehicle example geometry")
'''
def createTask():
    panel = TaskPanel()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
        Gui.Control.closeDialog()
        return None
    return panel

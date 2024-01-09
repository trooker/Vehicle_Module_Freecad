#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2023 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
#*                                                                         *
#*   Used general Ship flow for TaskPanel.y substituting gm_vehicle content     *
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

import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Units
from PySide import QtGui, QtCore
from . import Preview
from . import Tools
from .. import Instance  # from .gm_vehicle
from .. import GM_Vehicle_rc
from ..gm_vehicleUtils import Locale
from ..gm_vehicleUtils import Selection

class TaskPanel:
    def __init__(self):
        """Constructor"""
        self.name = "GM_Vehicle"
        App.Console.PrintMessage("TaskPanel setup for createGM_Vehicle\n")

        self.ui = ":/ui/TaskPanel_gm_vehicleCreateGM_Vehicle.ui"
        self.form = Gui.PySideUic.loadUi(self.ui)
        App.Console.PrintMessage("TaskPanel Preview ready\n")
        self.preview = Preview.Preview()

    def accept(self):
        """Create the gm_vehicle instance"""
        self.preview.clean()
        App.Console.PrintMessage("TaskPanel callingcreateGM_Vehicle\n")
        Tools.createGM_Vehicle(self.solids,
                         Locale.fromString(self.form.length.text()),
                         Locale.fromString(self.form.width.text()),
                         Locale.fromString(self.form.height.text()))
        return True

    def reject(self):
        """Cancel the job"""
        self.preview.clean()
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
        """Create and configurate the user interface"""
        self.form.length = self.widget(QtGui.QLineEdit, "length")
        self.form.width = self.widget(QtGui.QLineEdit, "width")
        self.form.height = self.widget(QtGui.QLineEdit, "height")
        if self.initValues():
            return True
        self.preview.update(self.L, self.W, self.H)
        QtCore.QObject.connect(
            self.form.length,
            QtCore.SIGNAL("valueChanged(const Base::Quantity&)"),
            self.onLength)
        QtCore.QObject.connect(
            self.form.width,
            QtCore.SIGNAL("valueChanged(const Base::Quantity&)"),
            self.onWidth)
        QtCore.QObject.connect(
            self.form.height,
            QtCore.SIGNAL("valueChanged(const Base::Quantity&)"),
            self.onHeight)



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
        form = mw.findChild(QtGui.QWidget, "CreateGM_VehicleTaskPanel")
        return form.findChild(class_id, name)

    def initValues(self):
        """Setup the initial values"""
        self.solids = Selection.get_solids()
        if not self.solids:
            #msg = App.Qt.translate("gm_vehicle_console","GM_Vehicle objects can only be created on top of hull geometry")
            msg = "GM_Vehicle objects can only be created on top of hull geometry"
            App.Console.PrintError(msg + '\n')
            #msg = App.Qt.translate("gm_vehicle_console","Please create or load a gm_vehicle geometry before using"" this tool")
            msg = "Please create or load a gm_vehicle geometry before using this tool"
            App.Console.PrintError(msg + '\n')
            return True
        # Get the gm_vehicle bounds. The  instance can not have dimensions
        # out of these values.
        self.bounds = [0.0, 0.0, 0.0]
        bbox = self.solids[0].BoundBox
        minX = bbox.XMin
        maxX = bbox.XMax
        minY = bbox.YMin
        maxY = bbox.YMax
        minZ = bbox.ZMin
        maxZ = bbox.ZMax
        for i in range(1, len(self.solids)):
            bbox = self.solids[i].BoundBox
            if minX > bbox.XMin:
                minX = bbox.XMin
            if maxX < bbox.XMax:
                maxX = bbox.XMax
            if minY > bbox.YMin:
                minY = bbox.YMin
            if maxY < bbox.YMax:
                maxY = bbox.YMax
            if minZ > bbox.ZMin:
                minZ = bbox.ZMin
            if maxZ < bbox.ZMax:
                maxZ = bbox.ZMax
        self.bounds[0] = maxX - minX
        self.bounds[1] = max(maxY - minY, abs(maxY), abs(minY))
        self.bounds[2] = maxZ - minZ

        qty = Units.Quantity(self.bounds[0], Units.Length)
        self.form.length.setText(qty.UserString)
        self.L = self.bounds[0] / Units.Metre.Value
        qty = Units.Quantity(self.bounds[1], Units.Length)
        self.form.width.setText(qty.UserString)
        self.W = self.bounds[1] / Units.Metre.Value
        qty = Units.Quantity(self.bounds[2], Units.Length)
        self.form.height.setText(qty.UserString)
        self.H = 0.5 * self.bounds[2] / Units.Metre.Value
        return False

    def clampVal(self, widget, val_min, val_max, val):
        if val >= val_min and val <= val_max:
            return val
        val = min(val_max, max(val_min, val))
        qty = Units.Quantity(val, Units.Length)
        widget.setText(qty.UserString)
        return val

    def onData(self, widget, val_max):
        """Updates the 3D preview on data changes.

        Keyword arguments:
        value -- Edited value. This parameter is required in order to use this
        method as a callback function, but it is not useful.
        """
        val_min = 0.001
        qty = Units.parseQuantity(Locale.fromString(widget.text()))
        try:
            val = qty.getValueAs('m').Value
        except ValueError:
            return
        return self.clampVal(widget, val_min, val_max, val)

    def onLength(self, value):
        """Answer to length changes

        Keyword arguments:
        value -- Edited value. This parameter is required in order to use this
        method as a callback function, but it is not useful.
        """
        L = self.onData(self.form.length,
                        self.bounds[0] / Units.Metre.Value)
        if L is not None:
            self.L = L
            self.preview.update(self.L, self.W, self.H)

    def onWidth(self, value):
        """Answer to breadth changes

        Keyword arguments:
        value -- Edited value. This parameter is required in order to use this
        method as a callback function, but it is not useful.
        """
        W = self.onData(self.form.width,
                        self.bounds[1] / Units.Metre.Value)
        if W is not None:
            self.W = W
            self.preview.update(self.L, self.W, self.H)

    def onHeight(self, value):
        """Answer to height changes

        Keyword arguments:
        value -- Edited value. This parameter is required in order to use this
        method as a callback function, but it is not useful.
        """
        H = self.onData(self.form.height,
                        self.bounds[2] / Units.Metre.Value)
        if H is not None:
            self.H = H
            self.preview.update(self.L, self.W, self.H)


def createTask():
    panel = TaskPanel()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
        Gui.Control.closeDialog()
        return None
    return panel

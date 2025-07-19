# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                               *
#*   Copyright (c) 1989- 2025 Abbott Analytical Products   <http://abbottanp.com/>*
#*                                                                               *
#* This program is a spike for bringa simple QtDesign layout into the FreeCAD - Abbott
#*    prototyping the invisioned Abiriba_RG  GM EV vehicle 
#*     detailed at: https://abbottanp.com/artifacts/gm_vehicle_WB/index.html.
#*Helpful Sites:
'''

250406_lu Morphed aap0037_998.  then followed AI
    ==>> Python QtDeigner  Signals/Slots embedded in FreeCAD macro
    https://www.google.com/search?client=ubuntu-sn&channel=fs&q=Python+QtDeigner++Signals%2FSlots+embedded+in+FreeCAD+macro
    
250404_lu See 250402 gaugeClock-slider_btns
    =>> FreeCAD how to receive signals from QtDesigner *.ui file sender at the receiver slot
https://www.google.com/search?client=ubuntu-sn&channel=fs&q=FreeCAD+how+to+receive+signals+from+QtDesigner+*.ui+file+sender+at+the+receiver+slot
'''
"""
older prior attempt
import os
import sys

import FreeCAD,FreeCADGui,Part
from PySide import QtGui, QtCore
from PySide2.QtWidgets import (QApplication, QWidget, QPushButton, QDial, QSlider, QVBoxLayout, QHBoxLayout, QLabel)
from PySide2.QtGui import QFont, QColor
from PySide2.QtCore import (Qt, Slot, QTimer)
from PySide2.QtUiTools import QUiLoader  ## <<<=== Lookup doc for tools
#does not apply for QUiLoader.load  from PySide2.QtCore import QFile, QIODevice, QTextStream

#from PySide import  uic

#like aap0035_test_001_popUI and aap0037_test996
#must be in same folder as Macro
#works but need resources/ui 
#print("Path to file.ui " + os.path.dirname(__file__) + '\n')
#path_to_ui = os.path.dirname(__file__) + "/resources/ui/aap0037_hehJayAccRejCheckBx.ui"
#print(path_to_ui + '\n')
#as a Qt Designer text file or pyuic5 convert to 
path_to_ui = os.path.dirname(__file__) #+ "/resources/ui/aap0037_hehJayAccRejCheckBx.ui"
print(path_to_ui + '\n')
#path_to_ui = os.path.dirname(__file__) + "/resources/aap0035_hehJayVehicle.qrc_rc.py"

class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        #example
        #self.ui_path = os.path.join(os.path.dirname(__file__), "my_ui.ui")
        self.ui_path = os.path.join(path_to_ui, "/resources/ui/aap0037_hehJayAccRejCheck.bx.ui")
        self.ui = QUiLoader.load(self.ui_path, self)

        # Connect the signal to the slot
        QtCore.Qt.connect(self.ui.DynoChartTaskPanel_Bx, "accept()", self, "accept")
	    
	
    def setupUi(self, MainWindow):
        self.centralWidget = FreeCADGui.PySideUic.loadUi(path_to_ui)
        MainWindow.setCentralWidget(self.centralWidget)

    @Slot()
    def reject(self):
        print('Update::    just happ reject\n')	    
 
    @Slot()
    def accept(self):
        print('Update::    just happy accept\n')
         	    

  
    
    @Slot()
    def update(self):
         #self.steerHoldValue = self.dialUI.self.dial.value()
         #App.Console.PrintMessage
         print('Update::   ' + str(50) +'\n')


    @Slot()
    def on_sliderAccel_valueChanged(self, value):
        #print('anything!!!\n')
        print('Speed: ' + str(value)+ ' kph\n')

    @Slot()
    def on_sliderFuel_valueChanged(self, value):
        #print('anything!!!\n')
        print('Speed: ' + str(value)+ ' kwh remaining\n')





MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
"""


import FreeCAD as App
import FreeCADGui as Gui

from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import (Qt, Slot, QTimer)
# Import the converted UI file
#from your_design_ui import Ui_Dialog
#See --class WindowName = Ui_DynoChartTaskPanel_exp
from aap0037_hehJayAccRejCheckBx import Ui_DynoChartTaskPanel_exp



__title__="Melt the QtDesign layout with signals/slots into a usable AAP macro for development"
__author__ = "Lucca Uzzo"
__url__ = "http://abbottanp.com"

                                       


class TestDialog(QtWidgets.QDialog):
    def __init__(self):
        super(TestDialog, self).__init__()
        self.ui = Ui_DynoChartTaskPanel_exp()
        self.ui.setupUi(self)
        self.speedValue = 0
        self.fuelValue = 1000
        # Connect signals to slots
        self.ui.DynoChartTaskPanel_Bx.accepted.connect(self.accept)
        self.ui.DynoChartTaskPanel_Bx.rejected.connect(self.reject)
        self.ui.DynoChartTaskPanel_Bx.clicked.connect(self.update)
        self.ui.DynoChartTaskPanel_Bx.accepted.connect(self.on_sliderFuel_valueChanged)
        self.ui.DynoChartTaskPanel_Bx.rejected.connect(self.spinValueChanged)
        self.ui.DynoChartTaskPanel_Bx.clicked['QAbstractButton*'].connect(self.close)

    """
    def createTask():
        panel = TestDialog()
        Gui.Control.showDialog(panel)
        if panel.setupUi():
            Gui.Control.closeDialog()
            return None
        return panel
    """

    """

    def on_button_clicked(self):
        # Action to perform when button is clicked
        print("Button Clicked!")
        # Example: Add a cube in FreeCAD
        box = FreeCAD.ActiveDocument.addObject("Part::Box","MyBox")
        FreeCAD.ActiveDocument.recompute()
    """
    @Slot()
    def reject(self):
        print('Status::    just happy reject.  Closing window\n')	
        self.close() 
        #try 1
        QtGui.qApp.quit()  
        #try 2
        #mw=FreeCADGui.getMainWindow()
        #mw.deleteLater()
        #try 3
        #FreeCADGui.getMainWindow().close()
        return False
 
    @Slot()
    def accept(self):
        print('Status::    just happy accept.  Keep going\n')
        return True	    

    @Slot()
    def close(self):
       pass
    
    @Slot()
    def update(self):
         #self.steerHoldValue = self.dialUI.self.dial.value()
         #App.Console.PrintMessage
         print('Status::   ' + str(self.speedValue) + ' mph     '+  str(self.fuelValue) +' KWHr Remaining\n')


    @Slot()
    def spinValueChanged(self):  #on_sliderAccel_valueChanged(self):
        #print('anything!!!\n')
        self.speedValue +=1
        print('Speed: ' + str(speedValue)+ ' kph\n')
        self.close()

    
    @Slot()
    def on_sliderFuel_valueChanged(self):
        self.Fuel -= 1
        #print('anything!!!\n')
        print('Fuel: ' + str(fuelValuealue)+ ' kwh remaining\n')
   
def createTask():
    panel = TestDialog()
    Gui.Control.showDialog(panel)
    if panel.setupUi():
        Gui.Control.closeDialog()
        return None
    return panel

  
# Create and show the dialog
import __main__

__main__.dialog = TestDialog()

"""
dialog = TestDialog()
dialog.exec_()
 """


    
    


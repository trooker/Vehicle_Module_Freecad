# -*- coding: utf-8 -*-
#***************************************************************************
#*                                                                               *
#*   Copyright (c) 1989- 2025 Abott Analytical Products   <http://abbottanp.com/>*
#*                                                                               *
#* This program seeks to provide a virtual interface between the HehJay gm_vheicle  and the user. 
#*    allowing a level of simulation of virtual vehicle performance.
"""
Helpful Resources:
1> ==>> See 250323_1103_examples_PySide for AI questions/inputs of valuein building program


250330_lu Introduce watchdog and executive loops


250323_lu Looking into window structure for HehJay
"""



import sys
from PySide2.QtWidgets import (QApplication, QWidget, QPushButton, QDial, QSlider, QVBoxLayout, QLabel)
from PySide2.QtCore import (Qt, Slot, QTimer)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler 
#import freecad as App

"""
app = QApplication.instance()
if app is not None:
    app.quit()
    QApplication.instance().deleteLater()
    app = None  # Remove the old reference
"""





timeout = 0.001
degPerRad = 57.2958
#raInc4_45 = 0.785398 <<==  45÷57.2958  where 360/8 = 45
raInc4_36 = .628318306  #36 # radians = 0.628318306 # <<== 36÷57.2958       360 ÷10 = 36 degrees/tooth

cycleKnt        = 0
cycleStepsTotal = 10 # number of teeth required for the AxleDrv gear to complete on revolution 



# 231101_tr copy from Python Console for 057_004_701_990_MotoDrv
# ('_57_004_701_990_MotorDrv').getObject('b_701_997_DrvGear_001_')

# testflg = 0  # uncomment for production
testflg = 1   #  shows trouble shooting items

#Controls Speed of Cranking/Cycling/Revolutions
#watchalarm = 100000000  # uuperslow mode
#watchalarm = 50000000   #almost slow
#watchalarm = 10000000  # slow mode
#watchalarm = 1000000   # normal speed for 0002
#watchalarm = 100000     # fast mode by default unless commented-out
watchalarm = 10


#for testing only 
#wrkStr = '_00_641_997_steeringAssy'   
#wrkStr = "_00_641_994_steeringAssy_tweakstepper"
#wrkStr = '_00_641_993_steeringAssy_portTieBarYoke'
#wrkStr = '_00_641_992_steeringAssy_adjTieBarPort'
#wrkStr = '_00_641_991_steeringAssy'
#wrkStr = '_00_641_990_steeringAssy'
wrkStr = '_00_641_988_steeringAssy'
#wrkStr = '_00_641_997_steeringAssy'

wrkObjDrvShaft = 'Binder' #'BinderShapeDrvShaft'     #'Body.Binder'
#App.Console.PrintMessage
print('Drives:: ' + wrkStr + '.'+ wrkObjDrvShaft+'\n')


def create_button(label, callback):
    button = QPushButton(label)
    button.clicked.connect(callback)
    return button

def create_dial(min_val, max_val, center_val, callback):
    dial = QDial()
    dial.setMinimum(min_val)
    dial.setMaximum(max_val)
    dial.setValue(center_val)
    dial.setNotchesVisible(True)
    dial.lastvalue = center_val
    dial.valueChanged.connect(callback)
    return dial


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        """
class HehJayWindow(QWidget):
    def __init__(self):
        super(HehJayWindow,self).__init__()
        """       
        self.setWindowTitle("Mouse Tracker")
        self.setGeometry(300, 300, 300, 200)
        self.isRunning = False
        self.timer = QTimer(self)
        self.millisecond = 10
        self.timer.timeout.connect(self.update)

        self.steerLabel = QLabel("Click Start Stop to Activate/Halt")

        self.btnStarter = create_button("Start/Stop", self.on_button_clicked)
        self.dialMin = 0
        self.dialMax = 100
        self.dialCenter = 50
        self.dialUI = create_dial(self.dialMin, self.dialMax, self.dialCenter, self.on_dial_changed)
        self.dialLastValue =  self.dialCenter
        self.steerHoldValue = self.dialUI.value()
        #self.speed = create_slider(Qt.Horizontal, self)
        self.slider = QSlider(Qt.Vertical, self)
        self.slider.setGeometry(30, 40, 200, 30)
        #self.slidervalueChanged = self[int].connect(slider.changeValue)
        layout = QVBoxLayout()
        layout.addWidget(self.btnStarter)
        layout.addWidget(self.steerLabel)
        layout.addWidget(self.dialUI)
        layout.addWidget(self.slider)
        self.setLayout(layout)


    @Slot()
    def valueChanged(self, value):
        print(value)


    @Slot()
    def update(self):
         self.steerHoldValue = self.dialUI.self.dial.value()
         #App.Console.PrintMessage
         print('Update::   ' + str(self.steerHoldValue) +'\n')


    @Slot()
    def on_button_clicked(self):
        if self.isRunning:
            #App.Console.PrintMessage
            print('Stoping\n')
            self.steerLabel.setText("X-out of window to terminate!")
            self.isRunning = False
            self.timer.stop()
            #self.dialUI.value() = self.dialCenter
            #self.steerHoldValue = self.dialUI.self.dial.value()
        else:
            #App.Console.PrintMessage
            print('Starting\n')
            self.isRunning = True
            self.steerLabel.setText("Rotate  dial handle Port/Starboard to steer")
            self.timer.start(self.millisecond)
            
            #self.dialUI.value() = self.dialCenter

    @Slot()
    def on_dial_changed(self, value):
        if self.isRunning:
            if value > self.dialLastValue:
                self.steerLabel.setText("Starboard")
                self.dialLastValue = value
            elif value <  self.dialLastValue:
                self.steerLabel.setText("Port")
                self.dialLastValue = value
            if  47 <= value <53:
                self.steerLabel.setText("Forward")
                self.dialLastValue = value
        else:    
            self.steerLabel.setText('Click the Start/Stop')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())



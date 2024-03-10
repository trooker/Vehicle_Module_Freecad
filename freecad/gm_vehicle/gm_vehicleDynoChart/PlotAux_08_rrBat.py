#***************************************************************************
#*   Copyright (c) 2024 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
#*                                                                         *
#*   Used general Ship flow for PlotAux.py substituting gm_vehicle content     *
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
240218_tr  1> Need to find way to put all three AWD, FWD, RWD plots on same graph for dyno
            2> Need way to eliminate X-axis collision with grid and tick marks as well as Y2
                see https://cmdlinetips.com/2019/10/how-to-make-a-plot-with-two-different-y-axis-in-python-with-matplotlib/
                see 240218_1620_twinxFunction.FCMacro.
            3> Need to improve *.ui to address Axle Torque as Axle Torque and Speed
            4> Add disclaimer that emprical data collected from bench test, straight line 
                hard surface travel, or other form of operational qualification unless otherwise noted.    
"""

import os
import sys
import math
import FreeCAD as App
import Spreadsheet
from ..gm_vehicleUtils import Paths
from ..gm_vehicleUtils.MathPyPlot import autolim   ## Home of autolim(ax) 
import matplotlib.pyplot as plt  ## 240211 https://stackoverflow.com/questions/60733837/typeerror-unhashable-type-numpy-ndarray-when-attempting-to-make-plot-using-n



class Plot(object):
    def __init__(self, gm_vehicle, points):    #sub for ship
        """ Constructor. performs plot and show it (Using pyxplot).
        @param gm_vehicle Selected object instance
        @param points List of computed hydrostatics.
        """
        msg = "Dev: Arrived Plot constructor"
        App.Console.PrintMessage(msg + '...\n')
        
        self.points = points[:]
        self.plt1 = self.plt2 = self.plt3 = None
        # activate a spreadsheet as a data source
        # fill array with points for plotting
        self.plotEndRow = 0
        self.spreadSheet(gm_vehicle)  #sub for ship
        self.plotRr_NomVI() 
        self.plotRr_PackVI() 
        self.plotRr_Volt()       # Pack Voltage and Voltage Sag dependnet on Cell Current
        self.plotRr_MoPwr()    #  Motor Power and Module Current dependnet on Cell Current
        msg = "Dev: Exit Plot constructor"
        App.Console.PrintMessage(msg + '...\n')


    def update(self, gm_vehicle):  #240207  , points):   #sub for ship
        #240207 self.points = points[:]
        
        msg = "Dev: Arrived Plot update"
        App.Console.PrintMessage(msg + '...\n')
        '''
        DEV 240212 see content of Ship Hydrostatic update for path to restore content
        '''
        pass

    def plotRr_NomVI(self):
        """ 
        Leave all content as it is now for AWD, FWD, and RWD 
        encase we discover method to handle  all three at once
        
        Graph the Acceleration - Traction of Vehicle
        @return True if error happens.
        """
        msg = "Dev: Arrived plotAxleTrq()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "RrBat::  Cell Current To Pack Voltage"
        try:
            from FreeCAD.Plot import Plot
        except ImportError:
            try:
                from freecad.plot import Plot
            except ImportError:
                msg = "Plot module is disabled, so plots cannot be created"
                App.Console.PrintWarning(msg + '\n')
                return True
        plt = Plot.figure(pltTitle)
        self.plt1 = plt

        # Generate the set of axes
        Plot.grid(False)    #DEV 240218 (True)
        # Sets up the working three axis
        for i in range(0, 3):
            ax = Plot.addNewAxes()
            # Y axis can be placed at right
            ax.yaxis.tick_right()
            ax.spines['right'].set_color((1.0, 0.0, 0.0))   #Y2 red
            ax.spines['left'].set_color((0.0, 1.0, 0.0))     #Y1 green
            ax.yaxis.set_ticks_position('right')
            #DEV 240217  Places label on the y2 axis right most y-axis
            ax.yaxis.set_label_position('right')
        
        Plot.grid(False)   #DEV 240218   (True)


        cellcur    = []
        pckpwr  = []
        pckvolt    = []   # The AWD axle speed must be either RWD or FWD 


        # 240208 xcb = []
        msg = "Dev: Arrived above for loop for reading points[] content"
        App.Console.PrintMessage(msg + '...\n')
        
        msg = "Dev: 240211 self.plotEndRow: " + str(self.plotEndRow)
        App.Console.PrintWarning(msg + '\n')


#        for i in range(len(self.points)):
        for i in range(self.plotEndRow):
            msg = "Dev: 240211 1705  i: " + str(i)
            App.Console.PrintWarning(msg + '\n')
            cellcur.append(self.points[i].cellcur)
            pckpwr.append((self.points[i].pckpwr))
            pckvolt.append(self.points[i].pckvolt)

            
        
        for i in range(self.plotEndRow):    
            msg = "Cheery picked  Ground Speed: " + str(cellcur[i]) + "     AWD Accel: " + str(pckpwr[i])  +  "     AWD:RWD : " + str(pckvolt[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])
        
        plt.axes = axes[0]
        series = Plot.plot(cellcur, pckpwr, r"$\ Pack \; Power \left( kW  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('*')
        series.line.set_markersize(13)
        series.line.set_linewidth(2.0)
        series.line.set_color((0.0, 1.0, 0.0))  # green 
        # DEV 240212 need to define series.ygridline.set_color((0.0, 1.0, 0.0))
        self.pckpwr = series
        Plot.xlabel(r'$Cell \; Current \; \left[ \mathrm{A} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{Pack \;  Power \; kV} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((0.0, 1.0, 0.0))   # green color


        plt.axes = axes[1]
        series = Plot.plot(cellcur, pckvolt, r"$\ Pack \; Voltage \left( V  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))   # Red
        self.pckvolt = series
        Plot.ylabel(r'$ \left[ \mathrm{Pack \; Voltage \; V} \right]$')
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((1.0, 0.0, 0.0))  #Red
        #DEV 240217 has no set_pos  Plot.legend.set_position([0.1, 0.35, 0.8, 0.65])
        Plot.legend(True)
        for ax in self.plt1.axesList:
            msg = "Dev: 240228  Jump to autolim:: "
            App.Console.PrintWarning(msg + '\n')
            autolim(ax)
 
 
 
        ## DEV 240210 why here  plt.update()
        return False
 
 

#FWD*****************
    def plotRr_PackVI(self):
        """ Graph the Accel - Traction of Vehicle
        @return True if error happens.
        """
        msg = "Dev: Arrived lotRr_PackVI()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "RrBat::  Cell Current To Pack Current & Power"
        try:
            from FreeCAD.Plot import Plot
        except ImportError:
            try:
                from freecad.plot import Plot
            except ImportError:
                msg = "Plot module is disabled, so plots cannot be created"
                App.Console.PrintWarning(msg + '\n')
                return True
        plt = Plot.figure(pltTitle)
        self.plt2 = plt

        # Generate the set of axes
        Plot.grid(False)   #DEV 240218  (True)
        # Sets up the working three axis
        for i in range(0, 3):
            ax = Plot.addNewAxes()
            # Y axis can be placed at right
            ax.yaxis.tick_right()
            ax.spines['right'].set_color((1.0, 0.0, 0.0))   #Y2 red
            ax.spines['left'].set_color((0.0, 1.0, 1.0))     #Y1 light bright blue
            ax.yaxis.set_ticks_position('right')
            #DEV 240217  Places label on the y2 axis right most y-axis
            ax.yaxis.set_label_position('right')
        
        Plot.grid(False)   #DEV 240218   (True)


        cellcur      = []
        pckpwr      = []
        pckcur    = []


        # 240208 xcb = []
        msg = "Dev: Arrived above for loop for reading points[] content"
        App.Console.PrintMessage(msg + '...\n')
        
        msg = "Dev: 240211 self.plotEndRow: " + str(self.plotEndRow)
        App.Console.PrintWarning(msg + '\n')


#        for i in range(len(self.points)):
        for i in range(self.plotEndRow):
            msg = "Dev: 240211 1705  i: " + str(i)
            App.Console.PrintWarning(msg + '\n')
            cellcur.append(self.points[i].cellcur)
            pckpwr.append((self.points[i].pckpwr))
            pckcur.append(self.points[i].pckcur)

            
        
        for i in range(self.plotEndRow):    
            msg = "Cheery picked  Ground Speed: " + str(cellcur[i]) + "     FWD Wheel Power: " + str(pckpwr[i])  +  "   FWD Battery Limit: " + str(pckcur[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])
       
        plt.axes = axes[0]
        series = Plot.plot(cellcur, pckpwr, r"$\ Pack\; Power \left( kW  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('D')
        series.line.set_linewidth(2.0)
        series.line.set_color((0.0, 1.0, 1.0))   #bright blue-green
        self.pckpwr = series
        Plot.xlabel(r'$Cell \; Current \; \left[ \mathrm{A} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{Pack \; Power \; kW} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((0.0, 1.0, 1.0))   #bright blue green color
        
        
        plt.axes = axes[1]
        series = Plot.plot(cellcur, pckcur, r"$\ Pack \; Current  \left( A  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))   # Red
        self.pckcur = series
        Plot.ylabel(r'$ \left[ \mathrm{Pack \; Current \;  A} \right]$')
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((1.0, 0.0, 0.0)) 

        #DEV 240217 has no set_pos  Plot.legend.set_position([0.1, 0.35, 0.8, 0.65])
        Plot.legend(True)
        for ax in self.plt2.axesList:
            msg = "Dev: 240228  Jump to autolim:: "
            App.Console.PrintWarning(msg + '\n')
            autolim(ax)
 
 
 
        ## DEV 240210 why here  plt.update()
        # Returns True if Error
        return False





    def plotRr_Volt(self):
        """
        Graph the plotRrt_Volt
        @return True if error happens.
        """
        msg = "Dev: Arrived ()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "RrBat:: Cell Current to Voltage Response"
        try:
            from FreeCAD.Plot import Plot
        except ImportError:
            try:
                from freecad.plot import Plot
            except ImportError:
                msg = "Plot module is disabled, so plots cannot be created"
                App.Console.PrintWarning(msg + '\n')
                return True
        plt = Plot.figure(pltTitle)
        self.plt3 = plt

        # Generate the set of axes
        Plot.grid(False)       #DEV 240218 (True)
        # Sets up the working three axis
        for i in range(0, 3):
            ax = Plot.addNewAxes()
            # Y axis can be placed at right
            ax.yaxis.tick_right()
            #draw Y2 as red line
            ax.spines['right'].set_color((1.0, 0.0, 0.0))    #Y2 red
            ax.spines['left'].set_color((1.0, 0.0, 1.0))      #Y1 off purple
            ax.yaxis.set_ticks_position('right')
            #DEV 240217  Places label on the y2 axis right most y-axis
            ax.yaxis.set_label_position('right')
        
        Plot.grid(False)   #DEV 240228    (True)


        cellcur     = []
        vsag      = []
        pckvolt    = []


        # 240208 xcb = []
        msg = "Dev: Arrived above for loop for reading points[] content"
        App.Console.PrintMessage(msg + '...\n')
        
        msg = "Dev: 240211 self.plotEndRow: " + str(self.plotEndRow)
        App.Console.PrintWarning(msg + '\n')


    #        for i in range(len(self.points)):
        for i in range(self.plotEndRow):
            msg = "Dev: 240211 1705  i: " + str(i)
            App.Console.PrintWarning(msg + '\n')
            cellcur.append(self.points[i].cellcur)
            vsag.append(self.points[i].vsag)
            pckvolt.append(self.points[i].pckvolt)

            
        
        for i in range(self.plotEndRow):    
            msg = "Cheery picked  Ground Speed: " + str(cellcur[i]) + "     RWD Accel: " + str(vsag[i])  +  "     RWD Traction: " + str(pckvolt[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])

        plt.axes = axes[0]   # was 4
        series = Plot.plot(cellcur, vsag, r"$\ Voltage \; Sag \left( V  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('P')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 1.0))   # Purplish color
        self.vsag = series
        Plot.xlabel(r'$Cell \; Current \; \left[ \mathrm{A} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{Voltage \;  Sag \; V} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((1.0, 0.0, 1.0))   #purplish color


        plt.axes = axes[1]   #  was 5
        series = Plot.plot(cellcur, pckvolt, r"$\ Pack \; Voltage \left( V  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))  # Unknow was yellow
        self.pckvolt = series
        Plot.ylabel(r'$ \left[ \mathrm{Pack \; Voltage \; V} \right]$')
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((1.0, 0.0, 0.0)) 
        
        #DEV 240217 has no set_pos  Plot.legend.set_position([0.1, 0.35, 0.8, 0.65])
        Plot.legend(True)
        for ax in self.plt3.axesList:
            msg = "Dev: 240228  Jump to autolim:: "
            App.Console.PrintWarning(msg + '\n')
            autolim(ax)
 
        ## DEV 240210 why here  plt.update()
        return False
    


            
    def plotRr_MoPwr(self):
        """
        Graph the plotRr_Volt
        @return True if error happens.
        """
        msg = "Dev: Arrived ()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "RrBat:: Cell Current to Motor Pwr & Module Current"
        try:
            from FreeCAD.Plot import Plot
        except ImportError:
            try:
                from freecad.plot import Plot
            except ImportError:
                msg = "Plot module is disabled, so plots cannot be created"
                App.Console.PrintWarning(msg + '\n')
                return True
        plt = Plot.figure(pltTitle)
        self.plt4 = plt

        # Generate the set of axes
        Plot.grid(False)       #DEV 240218 (True)
        # Sets up the working three axis
        for i in range(0, 3):
            ax = Plot.addNewAxes()
            # Y axis can be placed at right
            ax.yaxis.tick_right()
            ax.spines['right'].set_color((1.0, 0.0, 0.0))
            ax.spines['left'].set_color((1.0, 0.0, 1.0))
            ax.yaxis.set_ticks_position('right')
            #DEV 240217  Places label on the y2 axis right most y-axis
            ax.yaxis.set_label_position('right')
        
        Plot.grid(False)   #DEV 240228    (True)


        cellcur     = []
        mopwr     = []
        modui      = []


        # 240208 xcb = []
        msg = "Dev: Arrived above for loop for reading points[] content"
        App.Console.PrintMessage(msg + '...\n')
        
        msg = "Dev: 240211 self.plotEndRow: " + str(self.plotEndRow)
        App.Console.PrintWarning(msg + '\n')


    #        for i in range(len(self.points)):
        for i in range(self.plotEndRow):
            msg = "Dev: 240211 1705  i: " + str(i)
            App.Console.PrintWarning(msg + '\n')
            cellcur.append(self.points[i].cellcur)
            mopwr.append(self.points[i].mopwr)
            modui.append(self.points[i].modui)

            
        
        for i in range(self.plotEndRow):    
            msg = "Cheery picked  Cell Current: " + str(cellcur[i]) + "     Mo Pwr: " + str(mopwr[i])  +  "     Module I: " + str(modui[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])

        plt.axes = axes[0]   # was 4
        series = Plot.plot(cellcur, mopwr, r"$\ Motor \; Power \left( kW  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('P')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 1.0))   # Purplish color
        self.mopwr = series
        Plot.xlabel(r'$Cell \; Current \; \left[ \mathrm{A} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{Motor \;  Power \; kW} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((1.0, 0.0, 1.0))  #purplish color


        plt.axes = axes[1]   #  was 5
        series = Plot.plot(cellcur, modui, r"$\ Module \; Current \left(A  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))  # Unknow was yellow
        self.modui = series
        Plot.ylabel(r'$ \left[ \mathrm{Module \; Current \; A} \right]$')
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((1.0, 0.0, 0.0)) 
        
        #DEV 240217 has no set_pos  Plot.legend.set_position([0.1, 0.35, 0.8, 0.65])
        Plot.legend(True)
        for ax in self.plt4.axesList:
            msg = "Dev: 240228  Jump to autolim:: "
            App.Console.PrintWarning(msg + '\n')
            autolim(ax)
 
 
 
        ## DEV 240210 why here  plt.update()
        return False

        
        
    # pltSpreadsheet
    def getDataByRow(self, gm_vehicle):
        s = self.sheet
        # Print the data
        for i in range(len(self.points)):
            indx = i + 3  # need to skip first two rows staart reading on row 3
            msg = "Dev: 240210 getDataByRow() indx: " + str(indx)
            App.Console.PrintWarning(msg + '\n')
            try:
                point = self.points[i]
                point.cellcur   = s.get("A" + str(indx)),
                point.cellvolt = s.get("B" + str(indx))
                point.pckpwr  = s.get("C" + str(indx))
                point.vsag  = s.get("D" + str(indx))
                point.pckcur  = s.get("E" + str(indx))   # AWD Axle Speed is not cummulative it must be either RWD or FWD
                point.pckvolt  = s.get("F" + str(indx))
                point.mopwr  = s.get("G" + str(indx))
                point.modui  = s.get("H" + str(indx))
                msg = "Cell Current A::  " + str(point.cellcur) + "  C:: Peak Pwr: " +  str(point.cellvolt)   + "   G:: Motor Pwr Capability: " + str(point.pckpwr)           
                App.Console.PrintWarning(msg + '\n')
            except ValueError:
                break # exit for loop with filled points
            except AttributeError:    #240211
                break # exit for loop with filled points
            except TypeError:
                msg = "B: mph " + s.get("B" + str(indx)) + "   E: cellvolt: " + s.get("E" + str(indx))   + "   C: pckpwr: " + s.get("C" + str(indx))           
                App.Console.PrintWarning(msg + '\n')
                
        # 240211 do not need the decrement  i -= 1
        self.plotEndRow = i   # setting value for sheets shorter than the default 16
        msg = "Dev: 240210 self.plotEndRow just set: " + str(self.plotEndRow)
        App.Console.PrintWarning(msg + '\n')
        


    def fillSpreadSheet(self, gm_vehicle):  # suf for ship
            #See the Ship's version for writing to spreadsheet
        pass

    def spreadSheet(self, gm_vehicle):    # sub for ship
        """ Write data file.
        @param ship Selected ship instance
        @param trim Trim angle.
        @return True if error happens.
        """
        #DEV 240210 activate Spreadsheet for reading was addObject
        self.sheet = App.activeDocument().getObjectsByLabel('08_RrBattery-Capa')[0]
        #DEV 240209 do not need self.fillSpreadSheet(gm_vehicle)
        self.getDataByRow(gm_vehicle)

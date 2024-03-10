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
        self.plotAWD_WhlPwr() 
        self.plotFWD_WhlPwr() 
        self.plotRWD_WhlPwr() 
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
        
    def plotAWD_WhlPwr(self):
        """ 
        Leave all content as it is now for AWD, FWD, and RWD 
        encase we discover method to handle  all three at once
        
        Graph the Axle Torque of Vehicle
        @return True if error happens.
        """
        msg = "Dev: Arrived plotAxleTrq()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "Ground Speed: AWD Wheel Power and Rear Battery Limit"
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
            ax.spines['left'].set_color((0.0, 1.0, 0.0))    #Y1 green
            ax.yaxis.set_ticks_position('right')
            #DEV 240217  Places label on the y2 axis right most y-axis
            ax.yaxis.set_label_position('right')
       
        Plot.grid(False)   #DEV 240218   (True)


        gndspd      = []
        awdpwr      = []
        rBatLim    = []   # The AWD axle speed must be either RWD or FWD 


        # 240208 xcb = []
        msg = "Dev: Arrived above for loop for reading points[] content"
        App.Console.PrintMessage(msg + '...\n')
        
        msg = "Dev: 240211 self.plotEndRow: " + str(self.plotEndRow)
        App.Console.PrintWarning(msg + '\n')


#        for i in range(len(self.points)):
        for i in range(self.plotEndRow):
            msg = "Dev: 240211 1705  i: " + str(i)
            App.Console.PrintWarning(msg + '\n')
            gndspd.append(self.points[i].gndspd)
            awdpwr.append(self.points[i].awdpwr)
            rBatLim.append(self.points[i].fBatLim)

            
        
        for i in range(self.plotEndRow):    
            msg = "Cheery picked  Ground Speed: " + str(gndspd[i]) + "     AWD Wheel Power: " + str(awdpwr[i])  +  "     Battery Limit: " + str(rBatLim[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])
        
        plt.axes = axes[0]
        series = Plot.plot(gndspd, awdpwr, r"$\ AWD \; Wheel \; Power \left( KW  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('*')
        series.line.set_markersize(13)
        series.line.set_linewidth(2.0)
        series.line.set_color((0.0, 1.0, 0.0))  # not Blue 
        # DEV 240212 need to define series.ygridline.set_color((0.0, 1.0, 0.0))
        self.awdpwr = series
        Plot.xlabel(r'$Vehicle \; Ground \; Speed \; \left[ \mathrm{mph} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{AWD \; Wheel \; Power \; KW} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((0.0, 1.0, 0.0))   # green color


        plt.axes = axes[1]
        series = Plot.plot(gndspd, rBatLim, r"$\ Rear \; Battery \; Limit \left( KW  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))   # Red
        self.rBatLim = series
        Plot.ylabel(r'$ \left[ \mathrm{Rear \; Battery \; Limit \; KW} \right]$')
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
    def plotFWD_WhlPwr(self):
        """ Graph the Axle Torque of Vehicle
        @return True if error happens.
        """
        msg = "Dev: Arrived plotWhlPwr()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "Ground Speed: FWD Wheel Power & Battery Limit"
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


        gndspd      = []
        fwdpwr      = []
        fBatLim    = []


        # 240208 xcb = []
        msg = "Dev: Arrived above for loop for reading points[] content"
        App.Console.PrintMessage(msg + '...\n')
        
        msg = "Dev: 240211 self.plotEndRow: " + str(self.plotEndRow)
        App.Console.PrintWarning(msg + '\n')


#        for i in range(len(self.points)):
        for i in range(self.plotEndRow):
            msg = "Dev: 240211 1705  i: " + str(i)
            App.Console.PrintWarning(msg + '\n')
            gndspd.append(self.points[i].gndspd)
            fwdpwr.append((self.points[i].fwdpwr))
            fBatLim.append(self.points[i].fBatLim)

            
        
        for i in range(self.plotEndRow):    
            msg = "Cheery picked  Ground Speed: " + str(gndspd[i]) + "     FWD Wheel Power: " + str(fwdpwr[i])  +  "   FWD Battery Limit: " + str(fBatLim[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])
       
        plt.axes = axes[0]
        series = Plot.plot(gndspd, fwdpwr, r"$\ FWD \; Wheel \; Power \left( KW  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('D')
        series.line.set_linewidth(2.0)
        series.line.set_color((0.0, 1.0, 1.0))   #bright blue-green
        self.fwdpwr = series
        Plot.xlabel(r'$Vehicle \; Ground \; Speed \; \left[ \mathrm{mph} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{Wheel \; Power \; KW} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((0.0, 1.0, 1.0))   #bright blue-green
        
        
        plt.axes = axes[1]
        series = Plot.plot(gndspd, fBatLim, r"$\ FWD \; Battery \; Power \; Limit \left( KW  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))   # Red
        self.fBatLim = series
        Plot.ylabel(r'$ \left[ \mathrm{FWD \; Battery \; Power \; Limit \; KW} \right]$')
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((1.0, 0.0, 0.0)) 

        #DEV 240217 has no set_pos  Plot.legend.set_position([0.1, 0.35, 0.8, 0.65])
        Plot.legend(True)
        for ax in self.plt2.axesList:
            msg = "Dev: 240228  Jump to autolim:: "
            App.Console.PrintWarning(msg + '\n')
            autolim(ax)
 
 
 
        ## DEV 240210 why here  plt.update()
        return False





#RWD*****************
    def plotRWD_WhlPwr(self):
        """ Graph the Axle Torque of Vehicle
        @return True if error happens.
        """
        msg = "Dev: Arrived plotAxleTrq()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "Ground Speed: RWD Wheel Power & Battery Limit"
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
            ax.spines['right'].set_color((1.0, 0.0, 0.0))  #Y2 red
            ax.spines['left'].set_color((1.0, 0.0, 1.0))    #Y1 off purlpe
            ax.yaxis.set_ticks_position('right')
            #DEV 240217  Places label on the y2 axis right most y-axis
            ax.yaxis.set_label_position('right')
        
        Plot.grid(False)   #DEV 240228    (True)


        gndspd     = []
        rwdpwr      = []
        rBatLim    = []


        # 240208 xcb = []
        msg = "Dev: Arrived above for loop for reading points[] content"
        App.Console.PrintMessage(msg + '...\n')
        
        msg = "Dev: 240211 self.plotEndRow: " + str(self.plotEndRow)
        App.Console.PrintWarning(msg + '\n')


#        for i in range(len(self.points)):
        for i in range(self.plotEndRow):
            msg = "Dev: 240211 1705  i: " + str(i)
            App.Console.PrintWarning(msg + '\n')
            gndspd.append(self.points[i].gndspd)
            rwdpwr.append(self.points[i].rwdpwr)
            rBatLim.append(self.points[i].rBatLim)

            
        
        for i in range(self.plotEndRow):    
            msg = "Cheery picked  Ground Speed: " + str(gndspd[i]) + "     RWD Torque: " + str(rwdpwr[i])  +  "     RWD AxleSpeec: " + str(rBatLim[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])

        plt.axes = axes[0]   # was 4
        series = Plot.plot(gndspd, rwdpwr, r"$\ RWD \; Wheel \; Power \left( KW  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('P')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 1.0))   # Purplish color
        self.rwdpwr = series
        Plot.xlabel(r'$Vehicle \; Ground \; Speed \; \left[ \mathrm{mph} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{Wheel \; Power \; KW} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((1.0, 0.0, 1.0))  #purplish color


        plt.axes = axes[1]   #  was 5
        series = Plot.plot(gndspd, rBatLim, r"$\ RWD \; Battery \; Limit \left( KW  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))  # Unknow was yellow
        self.rBatLim = series
        Plot.ylabel(r'$ \left[ \mathrm{Rear \; Battery \; Limit \; KW} \right]$')
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
                point.gndspd   = s.get("B" + str(indx)),
                point.awdpwr = s.get("E" + str(indx))
                point.fwdpwr  = s.get("C" + str(indx))
                point.rwdpwr  = s.get("D" + str(indx))
                point.rBatLim  = s.get("F" + str(indx))   # AWD Axle Speed is not cummulative it must be either RWD or FWD
                point.fBatLim  = s.get("F" + str(indx))
                msg = "03:: B: mph " + str(point.gndspd) + "   E: awdpwr: " +  str(point.awdpwr)   + "   C: fwdpwr: " + str(point.fwdpwr)           
                App.Console.PrintWarning(msg + '\n')
            except ValueError:
                break # exit for loop with filled points
            except AttributeError:    #240211
                break # exit for loop with filled points
            except TypeError:
                msg = "B: mph " + s.get("B" + str(indx)) + "   E: awdpwr: " + s.get("E" + str(indx))   + "   C: fwdpwr: " + s.get("C" + str(indx))           
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
        self.sheet = App.activeDocument().getObjectsByLabel('05_WheelPwr-BattLimit')[0]
        #DEV 240209 do not need self.fillSpreadSheet(gm_vehicle)
        self.getDataByRow(gm_vehicle)

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
240229_tr  Resolved the tick mark values for X, Y1, Y2 using the autolim and placed in 
            utilities for reuse of code.  Leveraged to other seven plotaux_*.py modules.
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
import numpy as np
import matplotlib.pyplot as plt  ##   see https://stackoverflow.com/questions/60733837/typeerror-unhashable-type-numpy-ndarray-when-attempting-to-make-plot-using-n

"""
#DEV 240228 
def autolim(ax):
    xmin, xmax = sys.float_info.max, -sys.float_info.max
    ymin, ymax = sys.float_info.max, -sys.float_info.max
    #msg = "autolim    xmin: " + str(xmin) + "     xmax: " + str(xmax)  +  "     ymin: " + str(ymin)  +  "     ymax: " +str(ymax)   
    #App.Console.PrintWarning(msg + '\n')

    msg = "top of autolim for l statement"
    App.Console.PrintWarning(msg + '\n')
    for l in ax.get_lines():
        msg = "autolim    xmin: " + str(xmin) + "   l.get_xdata: " + str(l.get_xdata()) 
        App.Console.PrintWarning(msg + '\n')
        
        App.Console.PrintWarning(msg + '\n')
        xmin = min(xmin, min(l.get_xdata()))
        xmax = max(xmax, max(l.get_xdata()))
        ymin = min(ymin, min(l.get_ydata()))
        ymax = max(ymax, max(l.get_ydata()))
        msg = "autolim    xmin: " + str(min(xmin, min(l.get_xdata()))) + "     xmax: " + str(max(xmax, max(l.get_xdata())))  +  "     ymin: " + str(min(ymin, min(l.get_ydata())))  +  "     ymax: " +str(max(ymax, max(l.get_ydata())))   
        App.Console.PrintWarning(msg + '\n')
    try:
        ax.set_xlim(xmin, xmax)
    except TypeError:
        pass
    try:
        ax.set_ylim(ymin, ymax)
    except TypeError:
        pass
    return ax
"""


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
        self.plotAWD_AccTrc() 
        self.plotFWD_AccTrc() 
        self.plotRWD_AccTrc() 
        msg = "Dev: Exit Plot constructor"
        App.Console.PrintMessage(msg + '...\n')


    def update(self, gm_vehicle, points):   #sub for ship

        self.points = points[:]
        msg = "Dev: Arrived Plot update"
        App.Console.PrintMessage(msg + '...\n')
        '''
        DEV 240212 see content of Ship Hydrostatic update for path to restore content
        '''        
        pass
        
    def plotAWD_AccTrc(self):
        """ 
        Leave all content as it is now for AWD, FWD, and RWD 
        encase we discover method to handle  all three at once
        
        Graph the Acceleration - Traction of Vehicle
        @return True if error happens.
        """
        msg = "Dev: Arrived plotAxleTrq()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "Ground Speed: AWD Accel - Traction"
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
			# see https://matplotlib.org/stable/users/explain/axes/axes_ticks.html
            ax = Plot.addNewAxes()
            ax.yaxis.tick_right()  # Y axis can be placed at right
            ax.spines['right'].set_color((1.0, 0.0, 0.0))  #draw Y2 as red line
            ax.spines['left'].set_color((0.0, 1.0, 0.0))    #draw Y1 as green line
            ax.yaxis.set_ticks_position('right')
            ax.yaxis.set_label_position('right')  #DEV 240217  Places label on the y2 axis right most y-axis
         
        Plot.grid(False)   #Kills default value grid-lines   (True)

        gndspd    = []
        awdacc   = []
        rwdtrc    = []   # The AWD axle speed must be either RWD or FWD 

        msg = "Dev: Arrived above for loop for reading points[] content"
        App.Console.PrintMessage(msg + '...\n')
        msg = "Dev: 240211 self.plotEndRow: " + str(self.plotEndRow)
        App.Console.PrintWarning(msg + '\n')


#        for i in range(len(self.points)):
        for i in range(self.plotEndRow):
            msg = "Dev: 240211 1705  i: " + str(i)
            App.Console.PrintWarning(msg + '\n')
            gndspd.append(self.points[i].gndspd)
            awdacc.append(self.points[i].awdacc)
            rwdtrc.append(self.points[i].rwdtrc)
        
        for i in range(self.plotEndRow):    
            msg = "Cheery picked  Ground Speed: " + str(gndspd[i]) + "     AWD Accel: " + str(awdacc[i])  +  "     AWD:RWD : " + str(rwdtrc[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])
        
        plt.axes = axes[0]
        series = Plot.plot(gndspd, awdacc, r"$\ AWD \; Acceleration \left( g  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('*')
        series.line.set_markersize(13)
        series.line.set_linewidth(2.0)
        series.line.set_color((0.0, 1.0, 0.0))  # green
        # DEV 240212 need to define series.ygridline.set_color((0.0, 1.0, 0.0))
        self.awdacc = series
        Plot.xlabel(r'$Vehicle \; Ground \; Speed \; \left[ \mathrm{mph} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{AWD \;  Acceleration \; g} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((0.0, 1.0, 0.0))  #green


        plt.axes = axes[1]
        series = Plot.plot(gndspd, rwdtrc, r"$\ AWD::RWD \; Traction \left( g  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))   # Red
        self.rwdtrc = series
        Plot.ylabel(r'$ \left[ \mathrm{AWD \; \ \; RWD \; Traction \; g} \right]$')
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((1.0, 0.0, 0.0))  #Red
        Plot.legend(True)
        for ax in self.plt1.axesList:
            msg = "Dev: 240228  Jump to autolim:: "
            App.Console.PrintWarning(msg + '\n')
            autolim(ax)
        #false flag
        #self.awdacc.line.set_data(gndspd, awdacc)
        #self.rwdtrc.line.set_data(gndspd, rwdtrc)
        #plt.update() ## DEV 240210 why here  plt.update()
        return False   ## Indicates no errors

#FWD*****************
    def plotFWD_AccTrc(self):
        """ Graph the Accel - Traction of Vehicle
        @return True if error happens.
        """
        msg = "Dev: Arrived plotAccTrc()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "Ground Speed: FWD Accel-Traction"
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
            ax.yaxis.tick_right()   # Y axis can be placed at right
            ax.spines['right'].set_color((1.0, 0.0, 0.0))  #Y2 as red line
            ax.spines['left'].set_color((0.0, 1.0, 1.0))   #Y1 as light bright blue 
            ax.yaxis.set_ticks_position('right')
            ax.yaxis.set_label_position('right')  #DEV 240217  Places label on the y2 axis right most y-axis
        
        Plot.grid(False)   #DEV 240218   (True)


        gndspd      = []
        fwdacc      = []
        fwdtrc    = []


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
            fwdacc.append((self.points[i].fwdacc))
            fwdtrc.append(self.points[i].fwdtrc)
        #for ax in self.plt2.axesList:
        #    autolim(ax)

            
        
        for i in range(self.plotEndRow):    
            msg = "Cheery picked  Ground Speed: " + str(gndspd[i]) + "     FWD Wheel Power: " + str(fwdacc[i])  +  "   FWD Battery Limit: " + str(fwdtrc[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])
       
        plt.axes = axes[0]
#        series = Plot.plot(gndspd, awdacc, r"$\ AWD \; Acceleration \left( g  \right)$")
        
        series = Plot.plot(gndspd, fwdacc, r"$\ FWD \; Acceleration \left( g  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('D')
        series.line.set_linewidth(2.0)
        series.line.set_color((0.0, 1.0, 1.0))   #bright blue-green
        self.fwdacc = series
        Plot.xlabel(r'$Vehicle \; Ground \; Speed \; \left[ \mathrm{mph} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{FWD \; Acceleration \; g} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((0.0, 1.0, 1.0)) 
        
        
        plt.axes = axes[1]
        series = Plot.plot(gndspd, fwdtrc, r"$\ FWD \; Traction \; Limit \left( g  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))   # Red
        self.fwdtrc = series
        Plot.ylabel(r'$ \left[ \mathrm{FWD \; Traction \; Limit \; g} \right]$')
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
    def plotRWD_AccTrc(self):
        """ Graph the Acceleration - Traction of Vehicle
        @return True if error happens.
        """
        msg = "Dev: Arrived plotAccTrc()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "Ground Speed: RWD Accel - Traction"
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
            ax.spines['right'].set_color((1.0, 0.0, 0.0))
            ax.spines['left'].set_color((1.0, 0.0, 1.0))
            #DEV 240217  
            ax.yaxis.set_ticks_position('right')
            #DEV 240217  Places label on the y2 axis right most y-axis
            ax.yaxis.set_label_position('right')
        
        Plot.grid(False)   #DEV 240228    (True)


        gndspd     = []
        rwdacc      = []
        rwdtrc    = []


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
            rwdacc.append(self.points[i].rwdacc)
            rwdtrc.append(self.points[i].rwdtrc)

        #for ax in self.plt3.axesList:
        #    autolim(ax)
            
        
        for i in range(self.plotEndRow):    
            msg = "Cheery picked  Ground Speed: " + str(gndspd[i]) + "     RWD Accel: " + str(rwdacc[i])  +  "     RWD Traction: " + str(rwdtrc[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])

        plt.axes = axes[0]   # was 4
        series = Plot.plot(gndspd, rwdacc, r"$\ RWD \; Acceleration \left( g  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('P')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 1.0))   # Purplish color
        self.rwdacc = series
        Plot.xlabel(r'$Vehicle \; Ground \; Speed \; \left[ \mathrm{mph} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{RWD \;  Acceleration \; g} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_color((1.0, 0.0, 1.0))   #purplish color


        plt.axes = axes[1]   #  was 5
        series = Plot.plot(gndspd, rwdtrc, r"$\ RWD \; Traction \left( g  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))  # Unknow was yellow
        self.rwdtrc = series
        Plot.ylabel(r'$ \left[ \mathrm{Rear \; Traction \; g} \right]$')
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
                point.awdacc = s.get("E" + str(indx))
                point.fwdacc  = s.get("C" + str(indx))
                point.rwdacc  = s.get("D" + str(indx))
                point.fwdtrc  = s.get("F" + str(indx))   
                point.rwdtrc  = s.get("G" + str(indx))
                msg = "03:: B: mph " + str(point.gndspd) + "   E: awdacc: " +  str(point.awdacc)   + "   C: fwdacc: " + str(point.fwdacc)           
                App.Console.PrintWarning(msg + '\n')
            except ValueError:
                break # exit for loop with filled points
            except AttributeError:    #240211
                break # exit for loop with filled points
            except TypeError:
                msg = "B: mph " + s.get("B" + str(indx)) + "   E: awdacc: " + s.get("E" + str(indx))   + "   C: fwdacc: " + s.get("C" + str(indx))           
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
        self.sheet = App.activeDocument().getObjectsByLabel('06_Accel-Traction')[0]
        #DEV 240209 do not need self.fillSpreadSheet(gm_vehicle)
        self.getDataByRow(gm_vehicle)

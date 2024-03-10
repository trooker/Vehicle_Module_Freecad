#***************************************************************************
#*   Copyright (c) 2023, 2024 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
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

import os
import sys
import math
import FreeCAD as App
import Spreadsheet
from ..gm_vehicleUtils import Paths
from ..gm_vehicleUtils.MathPyPlot import autolim   ## Home of autolim(ax) 
import matplotlib.pyplot as plt  ## 240211 https://stackoverflow.com/questions/60733837/typeerror-unhashable-type-numpy-ndarray-when-attempting-to-make-plot-using-n

def autolim(ax):
    xmin, xmax = sys.float_info.max, -sys.float_info.max
    ymin, ymax = sys.float_info.max, -sys.float_info.max
    for l in ax.get_lines():
        xmin = min(xmin, min(l.get_xdata()))
        xmax = max(xmax, max(l.get_xdata()))
        ymin = min(ymin, min(l.get_ydata()))
        ymax = max(ymax, max(l.get_ydata()))
    try:
        ax.set_xlim(xmin, xmax)
    except TypeError:
        pass
    try:
        ax.set_ylim(ymin, ymax)
    except TypeError:
        pass


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
        self.plotEndRow = 0
        self.spreadSheet(gm_vehicle)  #sub for ship
        self.plotRrMotorDyno() 
        msg = "Dev: Left Plot constructor"
        App.Console.PrintMessage(msg + '...\n')


    def update(self, gm_vehicle):  #240207  , points):   #sub for ship
        #240207 self.points = points[:]
        
        msg = "Dev: Arrived Plot update"
        App.Console.PrintMessage(msg + '...\n')
        '''
        DEV 240212 see content of Ship Hydrostatic update for path to restore content
        '''
        pass
        
    def plotRrMotorDyno(self):
        """ Graph the Dyno CHart for the Rear Motor
        @return True if error happens.
        """
        msg = "Dev: Arrived plotRearMotorDyno()"
        App.Console.PrintMessage(msg + '...\n')
        
        pltTitle = "Rear Motor Dyno Chart"
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
        Plot.grid(True)
        # Sets up the working three axis
        for i in range(0, 3):
            ax = Plot.addNewAxes()
            # Y axis can be placed at right
            ax.yaxis.tick_right()
            ax.spines['right'].set_color((1.0, 0.0, 0.0))
            ax.spines['left'].set_color('none')
            ax.yaxis.set_ticks_position('right')
            ax.yaxis.set_label_position('right')
            # And X axis can be placed at bottom
            #for loc, spine in ax.spines.items():
            #   if loc in ['bottom', 'top']:
            #        spine.set_position(('outward', (i + 1) * 35))
        
        Plot.grid(True)

        rpm = []        
        trq  = []
        pwr = []

        # 240208 xcb = []
        msg = "Dev: Arrived above for loop for reading points[] content"
        App.Console.PrintMessage(msg + '...\n')
        
        msg = "Dev: 240211 self.plotEndRow: " + str(self.plotEndRow)
        App.Console.PrintWarning(msg + '\n')


#        for i in range(len(self.points)):
        for i in range(self.plotEndRow):
            msg = "Dev: 240211 1705  i: " + str(i)
            App.Console.PrintWarning(msg + '\n')
            rpm.append(self.points[i].rpm)
            trq.append(self.points[i].trq)
            pwr.append(self.points[i].pwr)
        
        for i in range(self.plotEndRow):    
            msg = "Dev: 240211 rpm: " + str(rpm[i]) + "     torque: " + str(trq[i])  + "     pwr: " + str(pwr[i])   
            App.Console.PrintWarning(msg + '\n')
          
        axes = Plot.axesList()
        for ax in axes:
            ax.set_position([0.1, 0.35, 0.8, 0.65])

        plt.axes = axes[0]
        
        series = Plot.plot(rpm, trq, r"$\ Torque \left( ftlb  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('D')
        series.line.set_linewidth(2.0)
        series.line.set_color((0.0, 0.0, 0.0))
        # DEV 240212 need to define series.ygridline.set_color((0.0, 1.0, 0.0))
        self.trq = series
        Plot.xlabel(r'$RPM \; \left[ \mathrm{rpm} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{Torque::ftlb} \right]$')
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)
        plt.axes = axes[1]
        series = Plot.plot(rpm, pwr, r"$\ Power \left( kW  \right)$")
        series.line.set_linestyle('-')
        series.line.set_marker('o')
        series.line.set_linewidth(2.0)
        series.line.set_color((1.0, 0.0, 0.0))
        self.pwr = series
        #Plot.xlabel(r'$RPM \;  \; \left[ \mathrm{rpm} \right]$')
        Plot.ylabel(r'$ \left[ \mathrm{Power::kW} \right]$')
        plt.axes.yaxis.label.set_color((1.0, 0.0, 0.0))  #Red
        plt.axes.xaxis.label.set_fontsize(15)
        plt.axes.yaxis.label.set_fontsize(15)

        Plot.legend(True)
        for ax in self.plt1.axesList:
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
                point.rpm  =s.get("A" + str(indx)),
                point.trq   = s.get("B" + str(indx)),
                point.pwr  = s.get("C" + str(indx))
            except ValueError:
                break # exit for loop with filled points
            except AttributeError:    #240211
                break # exit for loop with filled points
            except TypeError:
                msg = "A: rpm: " + s.get("A" + str(indx)) + "   B: torque: " + s.get("B" + str(indx))             
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
        self.sheet = App.activeDocument().getObjectsByLabel('02_Rear_dynoChart')[0]
        #DEV 240209 do not need self.fillSpreadSheet(gm_vehicle)
        self.getDataByRow(gm_vehicle)

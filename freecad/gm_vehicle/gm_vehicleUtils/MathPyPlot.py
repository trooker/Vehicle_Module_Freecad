#***************************************************************************
#*  
#*   Copyright (c) 2024 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
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
240227_tr This module supports the special needs of Plotting multiple axes along
            the left, right and bottom of the gm_vehicle workbench.  The content of
            autolim(ax) was copied from #*   Copyright (c) 2011, 2016 Jose Luis 
            Cercos Pita <jlcercos@gmail.com>   *

"""



import FreeCAD as App
import sys
import math
from FreeCAD import Units
import numpy as np
import matplotlib.pyplot as plt  ## 240211 https://stackoverflow.com/questions/60733837/typeerror-unhashable-type-numpy-ndarray-when-attempting-to-make-plot-using-n


"""
argument ax
return ax modified
where    ax in self.plt1...n.axesList  and n is the number of plots to be executed
 
"""

def autolim(ax):
    xmin, xmax = sys.float_info.max, -sys.float_info.max
    ymin, ymax = sys.float_info.max, -sys.float_info.max
    for l in ax.get_lines():
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

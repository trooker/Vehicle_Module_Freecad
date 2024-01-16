#***************************************************************************
#*
#*   Copyright (c) 2023, 2024 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
#*   
#*   Used general Ship flow for GM_Vehicle.py substituting gm_vehicle content     *

#*                                                                         *
#*   Copyright (c) 2015 Jose Luis Cercos Pita <jlcercos@gmail.com>         *
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
import FreeCADGui as Gui
import FreeCAD as App


__title__="FreeCAD GM_Vehicle module"
__author__ = "Lucca Uzzo"
__url__ = "https://abbottanp.com"

__doc__="The GM_Vehicle (Wheeled) module provides a set of tools for creating a virtual" \
        "  Ground Mobile Wheeled Vehicle"

from .gm_vehicleCreateGM_Vehicle.Tools import createGM_Vehicle
App.Console.PrintMessage("GM_Vehicle.py import createGM_Vehicle\n")
from .gm_vehicleDynoChart.Tools import areas, displacement, wettedArea, moment
from .gm_vehicleDynoChart.Tools import floatingArea, BMT, mainFrameCoeff
App.Console.PrintMessage("GM_Vehicle.py import Dyno Chart")

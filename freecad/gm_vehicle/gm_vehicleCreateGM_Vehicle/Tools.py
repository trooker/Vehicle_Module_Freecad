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
from .. import Instance


def createGM_Vehicle(solids, L, W, H):
    App.Console.PrintMessage("Tools top createGM_Vehicle\n")

    """Create a new object instance

    Position arguments:
    solids -- List of hull solid shapes
    L -- Object length between perpendiculars
    B -- Object Breadth not used for gm_vehicle
    T -- Object design draft
    W-- GM_Vehicle Width
    H -- GM_Vehicle Height

    Returned value:
    The new object

    The solids can be easily extracted from an already existing object. For
    instance, to get the solids from the selected object simply type the
    following command:

    solids = Gui.ActiveDocument.ActiveObject.Object.Shape.Solids

    Regarding the Length, Width, and Height, it is strongly recommended to use
    Units.parseQuantity method, e.g. The following obfuscated code snippet build
    such variables:

    from FreeCAD import Units
    L = Units.parseQuantity("25.5 m")
    B = Units.parseQuantity("3.9 m")
    T = Units.parseQuantity("1.0 m")
    W = Units.parseQuantity("3.9 m")
    H = Units.parseQuantity("1.0 m")
    """
    obj = App.ActiveDocument.addObject("Part::FeaturePython", "GM_Vehicle")
    App.Console.PrintMessage("Tools obj defined\n")

    gm_vehicle = Instance.GM_Vehicle(obj, solids)
    App.Console.PrintMessage("Tools gm_vehicle object created\n")    
    Instance.ViewProviderGM_Vehicle(obj.ViewObject)
    App.Console.PrintMessage("Tools gm_vehicle object veiwable\n")

    obj.Length = L
    obj.Width = W
    obj.Height = H
    App.Console.PrintMessage("Tools obj lenght, width, height set\n")
    App.ActiveDocument.recompute()
    return obj

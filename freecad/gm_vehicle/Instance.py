#***************************************************************************
#*
#*   Copyright (c) 2023 Abbottanp Analytical Products <luzzo@abbottanp.com>   *
#*
#*   Used general GM_Vehicle flow for TaskPanel.y substituting gm_vehicle content     *
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

import time
from math import *
import FreeCAD as App
from FreeCAD import Base, Vector
import Part
from .gm_vehicleUtils import Paths, Math
# from .init_gui import QT_TRANSLATE_NOOP


def add_gm_vehicle_props(obj):
    """This function adds the properties to a gm_vehicle instance, in case they are
    not already created

    Position arguments:
    obj -- Part::FeaturePython object

    Returns:
    The same input object, that now has the properties added
    """
    App.Console.PrintMessage("Instance add GM_Vehicle\n")
    
    try:
        obj.getPropertyByName('IsGM_Vehicle')
    except AttributeError:
        tooltip = "True if it is a valid gm_vehicle instance, False otherwise"
        obj.addProperty("App::PropertyBool",
                        "IsGM_Vehicle",
                        "GM_Vehicle",
                        tooltip).IsGM_Vehicle = True
    try:
        obj.getPropertyByName('Length')
    except AttributeError:
        tooltip = "GM_Vehicle length [m]"
        obj.addProperty("App::PropertyLength",
                        "Length",
                        "GM_Vehicle",
                        tooltip).Length = 0.0
    try:
        obj.getPropertyByName('Width')
    except AttributeError:
        tooltip = "GM_Vehicle with [m]"
        obj.addProperty("App::PropertyLength",
                        "Width",
                        "GM_Vehicle",
                        tooltip).Width = 0.0
    try:
        obj.getPropertyByName('Height')
    except AttributeError:
        tooltip = "GM_Vehicle draft [m]"
        obj.addProperty("App::PropertyLength",
                        "Height",
                        "GM_Vehicle",
                        tooltip).Height = 0.0


    try:
        obj.getPropertyByName('Weights')
    except AttributeError:
        tooltip = "Set of weight instances"
        obj.addProperty("App::PropertyStringList",
                        "Weights",
                        "GM_Vehicle",
                        tooltip).Weights = []
    App.Console.PrintMessage("gm_vehicle object created\n")
                        
    return obj


class GM_Vehicle:
    def __init__(self, obj, solids):
        """ Transform a generic object to a gm_vehicle instance.

        Keyword arguments:
        obj -- Part::FeaturePython created object which should be transformed
        in a gm_vehicle instance.
        solids -- Set of solids which will compound the gm_vehicle hull.
        """
        add_gm_vehicle_props(obj)
        # Add the subshapes
        obj.Shape = Part.makeCompound(solids)
        obj.Proxy = self

    def onChanged(self, fp, prop):
        """Detects the gm_vehicle data changes.

        Keyword arguments:
        fp -- Part::FeaturePython object affected.
        prop -- Modified property name.
        """
        if prop == "Length" or prop == "Width" or prop == "Height":
            pass

    def cleanWeights(self, fp):
        """Reanalyse the weights list looking for duplicated objects, or
        removed ones.
        """
        if not len(fp.Weights):
            return
        # Filter out the duplicated elements
        filtered_list = []
        [filtered_list.append(x) for x in fp.Weights if x not in filtered_list]
        if len(fp.Weights) != len(filtered_list):
            fp.Weights = filtered_list
        # Filter out the removed/non-valid objects
        object_names = []
        for obj in fp.Document.Objects:
            object_names.append(obj.Name)
        filtered_list = []
        for obj_name in fp.Weights:
            if obj_name in object_names:
                for obj in fp.Document.Objects:
                    if obj.Name == obj_name:
                        try:
                            if obj.IsWeight: filtered_list.append(obj_name)
                        except:
                            pass
                        break
        if len(fp.Weights) != len(filtered_list):
            fp.Weights = filtered_list


    def execute(self, fp):
        """Detects the entity recomputations.

        Keyword arguments:
        fp -- Part::FeaturePython object affected.
        """
        fp.Shape = Part.makeCompound(fp.Shape.Solids)


class ViewProviderGM_Vehicle:
    def __init__(self, obj):
        """Add this view provider to the selected object.

        Keyword arguments:
        obj -- Object which must be modified.
        """
        obj.Proxy = self

    def attach(self, obj):
        """Setup the scene sub-graph of the view provider, this method is
        mandatory.
        """
        return

    def updateData(self, fp, prop):
        """If a property of the handled feature has changed we have the chance
        to handle this here.

        Keyword arguments:
        fp -- Part::FeaturePython object affected.
        prop -- Modified property name.
        """
        return

    def getDisplayModes(self, obj):
        """Return a list of display modes.

        Keyword arguments:
        obj -- Object associated with the view provider.
        """
        modes = []
        return modes

    def getDefaultDisplayMode(self):
        """Return the name of the default display mode. It must be defined in
        getDisplayModes."""
        return "Shaded"

    def setDisplayMode(self, mode):
        """Map the display mode defined in attach with those defined in
        getDisplayModes. Since they have the same names nothing needs to be
        done. This method is optional.

        Keyword arguments:
        mode -- Mode to be activated.
        """
        return mode

    def onChanged(self, vp, prop):
        """Detects the gm_vehicle view provider data changes.

        Keyword arguments:
        vp -- View provider object affected.
        prop -- Modified property name.
        """
        pass

    def __getstate__(self):
        """When saving the document this object gets stored using Python's
        cPickle module. Since we have some un-pickable here (the Coin stuff)
        we must define this method to return a tuple of all pickable objects
        or None.
        """
        return None

    def __setstate__(self, state):
        """When restoring the pickled object from document we have the chance
        to set some internals here. Since no data were pickled nothing needs
        to be done here.
        """
        return None

    def claimChildren(self):
        objs = []
        # Locate the owner gm_vehicle object
       # doc_objs = FreeCAD.ActiveDocument.Objects
        doc_objs = App.ActiveDocument.Objects
        obj = None
        for doc_obj in doc_objs:
            try:
                v_provider = doc_obj.ViewObject.Proxy
                if v_provider == self:
                    obj = doc_obj
            except:
                continue
        if obj is None:
            FreeCAD.Console.PrintError("Orphan view provider found...\n")
            FreeCAD.Console.PrintError(self)
            FreeCAD.Console.PrintError('\n')
            return objs

        # Check everything is all right
        add_gm_vehicle_props(obj)


        # Claim the weights
        bad_linked = 0
        for i, w in enumerate(obj.Weights):
            try:
                w_obj = FreeCAD.ActiveDocument.getObject(w)
                objs.append(w_obj)
            except:
                del obj.Weights[i - bad_linked]
                bad_linked += 1
        return objs

    def getIcon(self):
        """Returns the icon for this kind of objects."""
        return ":/icons/GM_Vehicle_Instance.svg"

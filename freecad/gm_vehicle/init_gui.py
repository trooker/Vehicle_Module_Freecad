import os
import FreeCADGui as Gui
import FreeCAD as App
#from freecad.gm_vehicle import ICONPATH
__dirname__ = os.path.dirname(__file__)


class GM_VehicleWorkbench(Gui.Workbench):


    Icon = os.path.join(__dirname__, "resources",  'icons', 'VehicleWorkbench.svg')
    MenuText = "GM Vehicle"
    ToolTip = "Tools for building a virtual ground mobile wheeled vehicle."
#    Icon = os.path.join(ICONPATH, "resources","icons", "VehicleWorkbench.svg")
    toolbox = []
    
    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        else:
            return True
    

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    from . import GM_VehicleGui


    def Initialize(self):
        from freecad.gm_vehicle import my_numpy_function
        App.Console.PrintMessage("switching to workbench_gm_vehicle\n")
        App.Console.PrintMessage("run a numpy function: sqrt(100) = {}\n".format(my_numpy_function.my_foo(100)))


        # ToolBar
        gm_vehiclelist = ["GM_Vehicle_LoadExample",
                           "GM_Vehicle_CreateGM_Vehicle",
                           "GM_Vehicle_DynoChart"]
        App.Console.PrintMessage("init_gui.py: Toolbar gm_vehilcelist \n")
                           

        self.appendToolbar("GM_Vehicle design", gm_vehiclelist)
        App.Console.PrintMessage("init_gui.py: : Below Toolbar \n")
        
        self.appendMenu("GM_Vehicle design", gm_vehiclelist)
        App.Console.PrintMessage("init_gui.py: : Add to Menu \n")


    def Activated(self):
        '''
        code which should be computed when a user switch to this workbench
        '''
        pass

    def Deactivated(self):
        '''
        code which should be computed when this workbench is deactivated
        '''
        pass


Gui.addWorkbench(GM_VehicleWorkbench())

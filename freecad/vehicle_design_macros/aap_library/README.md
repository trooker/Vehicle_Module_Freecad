## aap_library Build Folder

This folder contains the artifact needed to create the aap_lib runtime Python library for the GM_Vehicle Workbench.

To build a new aap_lib if needed:
- Modify the setup.py file as needed
- Insure the modiifed utiliy macros are placed in the aap_library/aap_lib folder
- Run "python setup.py bdist_wheel"
- Copy and paste the contents of the aap_library/dist/aap_lib to the Macro folder of the set for the local FreeCAD session.
- See aap_lib/topoChassisToolbox.py for information about building the aap_lib, distributing, etc.
- When in doubt follow this bolierplate solution:
    https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f 

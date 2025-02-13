## aap_library Build Folder

This folder contains the artifact needed to create the aap_lib runtime Python library for the GM_Vehicle Workbench.

To build a new aap_lib if needed:
- Follow this bolierplate solution to create the proper build structure folder:
    https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f 
- Modify the setup.py file as needed
- Insure the modified utiliy macros are placed in the aap_library/aap_lib folder.  A starter set is provided.
- Run "python setup.py bdist_wheel"
- After running a build, copy and paste the contents of the aap_library/dist/aap_lib to the Macro folder of the set for the local FreeCAD session.
- See aap_lib/topoChassisToolbox.py for information about building the aap_lib, distributing, etc.


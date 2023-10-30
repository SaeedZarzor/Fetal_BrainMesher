# Fetal Brain Mesher

Creates a 3D brain mesh from fetal_mri atlas images using only hexahedral elements.

To create example brain model to be viewed using Paraview, run the following command in the Fetal_BrainMesher directory:

**fetal_brain_creation.py fetal_brain_config_example.ini**


This will create 3 files in a folder with the same name as the mri input image ($FILENAME$).
1. $FILENAME$_log.txt: A log file of what was done and the configuration settings used
2. $FILENAME$_mesh_VTK.vtk: The VTK mesh file to be opened in Paraview
3. mri/$FILENAME$_new.nii: A representation of the mri used after the binary threshold is applied

The configurations used for this model creation are given in **fetal_brain_config_example.ini**

*See requirements.txt for required package installation*
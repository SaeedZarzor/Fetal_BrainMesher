# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 13:47:49 2023

@author: grife
"""

import os
import nibabel as nb
import numpy as np

def create_aseg(fileInPath, filename, fileOutPath, data_new):
          
    # Step 1: Using freesurfer and 'recon-all' create mri outputs. Ensure aseg.mgz is created.
    t1_file = "\\".join([fileInPath, filename])
    t1 = nb.load(t1_file)

    # Now we can save the changed data into a new NIfTI file
    new_img = nb.Nifti1Image(data_new, affine=t1.affine, header=t1.header)
    pathOut = fileOutPath + "/mri"
    file_in_split = filename.split(".")
    file_name_out = file_in_split[0] + "_new"
    if len(file_in_split) == 1:
        file_name_out += '.mgz'
    else:
        file_name_out += "." + file_in_split[1]

    if not os.path.exists(pathOut):
        os.mkdir(pathOut)

    nb.save(new_img, "/".join([pathOut, file_name_out]))

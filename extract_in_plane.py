"""
Execute this script to skip the interactive plane selection 
and extract vel data directly to the specified 3d plane.
"""

import os
import os.path as osp
from glob import glob
import numpy as np
import pyvista as pv
import utils as ut

#-----------------------------------------------------------------------------------------------------------------------
# Options
# path for saving probed .vtp files
outputDir = r'G:\ZhongShan_Data\ZS-ASAD03\pre_MR_processed\try_map' 

# filename of resamples .vtp files
saveName = 'ZS03'   

# directory containing .vtk files of a 4D flow acquisition (processed by dicoms_to_vtk.py)
source_flow_dir = r'G:\ZhongShan_Data\ZS-ASAD03\pre_MR_processed\flow'

# path of the .vtk file containing the binary segmentation mask: it must be aligned with .vtk 4D flow files
source_mask_fn = r'G:\ZhongShan_Data\ZS-ASAD03\ZS03_pre_source_inlet_plane.stl'  
#-----------------------------------------------------------------------------------------------------------------------
#Read data

flowData = [pv.read(fn) for fn in sorted(glob(osp.join(source_flow_dir, '*.vtk')))]
mask = pv.read(source_mask_fn)

os.makedirs(outputDir, exist_ok=True)
probedDir = osp.join(outputDir, 'probed_planes')
for k in range(len(flowData)):
    # ensure point-data exists for sampling; only convert if needed (minimal change)
    if len(flowData[k].point_data) == 0 and len(flowData[k].cell_data) > 0:
        flowData[k] = flowData[k].cell_data_to_point_data()
    # use .sample(...) (works across pyvista versions; same idea as probe)
    probed_plane = mask.sample(flowData[k])
    probed_plane.save(osp.join(outputDir, saveName + '_probed_{:02d}.vtp'.format(k)))
print("Done")
import slicer

import numpy as np

from scipy.ndimage import binary_fill_holes

from vtk.util import numpy_support



#

# Select your segmentation node

#

segmentationNode = slicer.util.getNode("Segmentation")  # change name if needed



#

# Export segmentation to labelmap

#

labelmapNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode")



slicer.modules.segmentations.logic().ExportAllSegmentsToLabelmapNode(

    segmentationNode,

    labelmapNode

)



#

# Get numpy array from labelmap

#

array = slicer.util.arrayFromVolume(labelmapNode)



#

# Fill holes slice-by-slice

#

filledArray = np.zeros_like(array)



for i in range(array.shape[0]):  # axial slices

    sliceMask = array[i] > 0



    # Fill enclosed regions

    filledSlice = binary_fill_holes(sliceMask)



    filledArray[i] = filledSlice.astype(array.dtype)



#

# Write back to volume

#

slicer.util.updateVolumeFromArray(labelmapNode, filledArray)



#

# Import back into segmentation

#

filledSegmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")

filledSegmentationNode.CreateDefaultDisplayNodes()



slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(

    labelmapNode,

    filledSegmentationNode

)



print("Filled segmentation created.")
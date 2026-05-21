import slicer
import numpy as np
from scipy.ndimage import binary_fill_holes

segmentationNode = slicer.util.getNode("Segmentation_3_1") ##IMPORTANT: Change inside the quotes to the name of your segmentation node. You can find it in the Data module. It should be something like "Segmentation_3_1" or "Segmentation_4_1" depending on how many segmentations you have created.
segmentation = segmentationNode.GetSegmentation()

labelmapNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode")

# export
slicer.modules.segmentations.logic().ExportAllSegmentsToLabelmapNode(
    segmentationNode,
    labelmapNode
)

array = slicer.util.arrayFromVolume(labelmapNode)

filledArray = np.zeros_like(array)

for i in range(array.shape[0]):
    filledArray[i] = binary_fill_holes(array[i] > 0)

slicer.util.updateVolumeFromArray(labelmapNode, filledArray)

# IMPORTANT: overwrite SAME segmentation CLEANLY
slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(
    labelmapNode,
    segmentationNode
)

# cleanup
slicer.mrmlScene.RemoveNode(labelmapNode)
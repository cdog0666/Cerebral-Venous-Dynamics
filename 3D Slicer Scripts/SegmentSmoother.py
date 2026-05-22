#
# 3D Slicer smoothing script for segmented structures
# Paste into the Python Interactor in Slicer
#

import slicer

# =========================
# SETTINGS
# =========================

segmentationNodeName = "Segmentation_3_1"   # change if needed
smoothingMethod = "GAUSSIAN"            # GAUSSIAN, MEDIAN, MORPHOLOGICAL_OPENING, MORPHOLOGICAL_CLOSING
kernelSizeMm = 2.0                      # increase for smoother result
applyToAllSegments = True

# =========================
# GET SEGMENTATION NODE
# =========================

segmentationNode = slicer.util.getNode(segmentationNodeName)

if not segmentationNode:
    raise Exception(f"Could not find segmentation node: {segmentationNodeName}")

# =========================
# CREATE SEGMENT EDITOR
# =========================

segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
segmentEditorWidget.setMRMLScene(slicer.mrmlScene)

segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
segmentEditorWidget.setSegmentationNode(segmentationNode)

# =========================
# APPLY SMOOTHING
# =========================

segmentation = segmentationNode.GetSegmentation()

for i in range(segmentation.GetNumberOfSegments()):

    segmentID = segmentation.GetNthSegmentID(i)

    if not applyToAllSegments:
        continue

    print(f"Smoothing segment: {segmentID}")

    segmentEditorWidget.setCurrentSegmentID(segmentID)

    segmentEditorWidget.setActiveEffectByName("Smoothing")
    effect = segmentEditorWidget.activeEffect()

    # Set smoothing type
    effect.setParameter("SmoothingMethod", smoothingMethod)

    # Kernel size in mm
    effect.setParameter("KernelSizeMm", str(kernelSizeMm))

    # Apply smoothing
    effect.self().onApply()

print("Done smoothing segmentation.")

# Cleanup
segmentEditorWidget = None
slicer.mrmlScene.RemoveNode(segmentEditorNode)
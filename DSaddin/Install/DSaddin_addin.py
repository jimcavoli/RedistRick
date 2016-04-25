import os
import sys
import arcpy
import pythonaddins

relPath = os.path.dirname(__file__) 
toolPath = relPath + r"\Redistricting.pyt"  

from arcpy import env
from arcpy import mapping

class DistrictButon(object):
    """Implementation for DSaddin_district.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        # TODO set infc properly based on the selected feature input layer
        # Iterate through all of the layers present in the mxd file
        
        mxd = mapping.MapDocument("CURRENT")
        layers = mapping.ListLayers(mxd)
        selected_lyr = []
        for layer in layers:
            name = layer.name
            desc = arcpy.Describe(name)
            selected_FID = desc.FIDSet
            if len(selected_FID) > 0:
                selected_lyr.append(layer.dataSource)
        
        # If features selected from multiple layers only the first one is addressed by script.
        infc = selected_lyr[0]
        
        # write to temporary file then read as parameter (temp.txt in same directory)
        f = open(r'E:\redistricting_data\RedistRick-development\DSaddin\Install\temp.txt','w')
        f.write(infc)
        #----------------------------------------------------------------------------------
        os.system("python " + os.path.join(os.path.dirname(
                                           os.path.abspath(__file__)),
                                           "result_dialog.py") + " " + infc)
        pythonaddins.GPToolDialog(toolPath,"Add_Integer_Field_Tool")

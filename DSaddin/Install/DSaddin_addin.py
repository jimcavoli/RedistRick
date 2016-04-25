import os
import sys
import arcpy
import pythonaddins

class DistrictButon(object):
    """Implementation for DSaddin_district.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        # TODO set infc properly based on the selected feature input layer
        infc = 'None'
        os.system("python " + os.path.join(os.path.dirname(
                                           os.path.abspath(__file__)),
                                           "result_dialog.py") + " " + infc)
        pythonaddins.GPToolDialog(os.path.join(
                                  os.path.dirname(os.path.abspath(__file__)),
                                  "Redistricting.pyt"),
                                  "Add_Integer_Field_Tool")

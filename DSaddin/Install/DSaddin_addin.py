import arcpy
import pythonaddins

class DistrictButon(object):
    """Implementation for DSaddin_district.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog("c:/Users/n44635/Documents/ArcGIS/Redistricting.pyt",
                                  "Add_Integer_Field_tool")
        
class BuildDistrict(object):
    """Implementation for DSaddin.build_layers (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False
    def onClick(self):
        pythonaddins.GPToolDialog("c:/Users/n44635/Documents/ArcGIS/Redistricting.pyt",
                                  "Build_Districts_tool")

import arcpy
import pythonaddins
import result_dialog


class DistrictButon(object):
    """Implementation for DSaddin_district.button (Button)"""
    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        app = RedistrictingResults()
        app.mainloop()
        pythonaddins.GPToolDialog("Redistricting.pyt",
                                  "Add_Integer_Field_tool")

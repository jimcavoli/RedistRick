# Brian P. Steffes
# April 23, 2016
# The Ohio State University
# Geog5223: GIS Design and Implementation

import os
import sys
import arcpy
from arcpy import env


# Custom Functions:
# ------------------------------------------------------------------------------------


# Custom Function 1: numDistricts(featureclass), returns integer
# returns and integer representing the number of districts
# assigned in a feature class with attribute Dist_ID.
# Districts are numbered 1 to n
def numDistricts(infc, field):
        field_values = []
        rows = arcpy.SearchCursor(infc, fields=field)
        for row in rows:
            instance = row.getValue(field)
            field_values.append(instance)

        value_set = set(field_values)
        present_values = list(value_set)
        return len(present_values)

# --------------------------------------------------------------------------------------


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [Add_Integer_Field_Tool,
                      Split_Layer_Tool,
                      Build_Districts_Tool]


class Add_Integer_Field_Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Add Integer Field"
        self.description = "Populate a new Field with a uniform integer value"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # input TIGER file layer (shp file)
        param0 = arcpy.Parameter(
            displayName="Input Feature Class",
            name="in_feature",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        # Name of Field to be Added
        param1 = arcpy.Parameter(
            displayName="New Field",
            name="new_field",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        # Value to populate the field
        param2 = arcpy.Parameter(
            displayName="Field Integer Value",
            name="field_value",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")

        # list of parameters for tool
        parameters = [param0, param1, param2]
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def execute(self, parameters, messages):
        # Access the parameters: (Returns values as stringtypes)
        infc = parameters[0].valueAsText
        field_name = parameters[1].valueAsText
        field_value = int(parameters[2].valueAsText)

        # -----------------------------------------------------------------
        # Frequently Used Variables
        code_directory = 'E:\\redistricting_data\code'
        infc_dir = os.path.split(arcpy.Describe(infc).catalogPath)[0]
        infc_name = arcpy.Describe(infc).file
        write_file_name = 'temp_output.txt'
        # -----------------------------------------------------------------

        # define the workspace using the path name of the input feature class
        env.workspace = infc_dir

        # Add Field to the Feature Class
        try:
            arcpy.management.AddField(infc_name, field_name, "LONG")
        except arcpy.ExecuteError:
            print arcpy.GetMessages(2)

        # Populate the Field
        mxd = arcpy.mapping.MapDocument("CURRENT")
        layer = arcpy.mapping.ListLayers(mxd)[0]
        desc = arcpy.Describe(layer)
        fids = [int(s) for s in desc.fidSet.split(";")]

        cursor = arcpy.da.UpdateCursor(infc_name, ["FID", field_name])
        mxd = arcpy.mapping.MapDocument("CURRENT")

        for row in cursor:
            if int(row[0]) in fids:
                row[1] = field_value
                cursor.updateRow(row)

# This builds districts based off of an attribute, Dist_ID.
# Returns a field class of joined District Polygons

class Build_Districts_Tool(object):
    def __init__(self):
        """Define the tool"""
        self.label = "Build Districts"
        self.description = "Create District Polygons from Dist_ID attribute"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # Input Feature Class
        param0 = arcpy.Parameter(
            displayName="Input Feature Class",
            name="in_feature",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")

        # only accept Polygon Feature Class
        param0.filter.list = ["Polygon"]

        # Name of Field to be Added
        param1 = arcpy.Parameter(
            displayName="Field Name",
            name="field_name",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        param1.parameterDependencies = [param0.name]
        param1.filter.list = ["LONG", "SHORT"]

        # Outpath
        param2 = arcpy.Parameter(
            displayName="Output Folder",
            name="field_value",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Output")

        # list of parameters for tool
        parameters = [param0, param1, param2]
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def execute(self, parameters, messages):
        infc = parameters[0].valueAsText
        outfc = parameters[2].valueAsText
        env.workspace = os.path.split(infc)[0]

        n = numDistricts(infc, parameters[1].valueAsText)

        # Create Layer from id (default layer name is lyr)
        arcpy.management.MakeFeatureLayer(infc, "lyr")
        # Dissolve layer
        arcpy.management.Dissolve(infc, outfc, parameters[1].valueAsText)
        # add dissolveed layer to district_layers array

        # join all members of district_layers array
        # use copy feature management toool to create a new feature class
        # that is held under outfc.

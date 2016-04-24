Brian P. Steffes
April 23, 2016
The Ohio State University
Geog5223: GIS Design and Implementation


print to E:\redistricting_data\code\temp_output.txt for debugging purposes
"""





import arcpy
from arcpy import env
import os, sys


# Custom Functions:
# ------------------------------------------------------------------------------------


# Custom Function 1: numDistricts(featureclass), returns integer
# returns and integer representing the number of districts assigned in a feature class
# with attribute Dist_ID
# Districts are numbered 1 to n
def numDistricts(infc):
		field_values = []
		rows = arcpy.SearchCursor(infc,fields = "Dist_ID")
		for row in rows:
			instance = row.getValue("Dist_ID")
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
		self.tools = [Tool_1, Tool_2, Tool_3]


class Tool_1(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Add Integer Field"
		self.description = "Populate a new Field with a uniform integer value"
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""
		# input TIGER file layer (shp file)
		param0 = arcpy.Parameter(
			displayName = "Input Feature Class",
			name = "in_feature",
			datatype = "DEFeatureClass",
			parameterType = "Required",
			direction = "Input")
		
		# Name of Field to be Added
		param1 = arcpy.Parameter(
			displayName = "New Field",
			name = "new_field",
			datatype = "GPString",
			parameterType = "Required",
			direction = "Input")
		
		# Value to populate the field
		param2 = arcpy.Parameter(
			displayName = "Field Integer Value",
			name = "field_value",
			datatype = "GPLong",
			parameterType = "Required",
			direction = "Input")
		
		# list of parameters for tool
		parameters = [param0,param1,param2]
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
		infc_directory = os.path.split(arcpy.Describe(infc).catalogPath)[0]
		infc_name = arcpy.Describe(infc).file
		write_file_name = 'temp_output.txt'
		# -----------------------------------------------------------------

		
		# define the workspace using the path name of the input feature class
		env.workspace = infc_directory
		
		# Add Field to the Feature Class 
		try:
			arcpy.management.AddField(infc_name, field_name, "LONG")
		except arcpy.ExecuteError:
			print (arcpy.getMessages(2))
		
		# Populate the Field
		arcpy.management.CalculateField(infc_name, field_name, field_value)

# Tool to Select Features by Attribute and create a new feature class from them
class Tool_2(object):
	def __init__(self):
		"""Define the tool"""
		self.label = "Split Layer"
		self.description = "Creates new Feature Classes based off of instances that share the same value of the input field"
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""
		# Input Feature Class 
		param0 = arcpy.Parameter(
			displayName = "Input Feature Class",
			name = "in_feature",
			datatype = "DEFeatureClass",
			parameterType = "Required",
			direction = "Input")
		
		# only accept Polygon Feature Class
		param0.filter.list = ["Polygon"]
		
		# Field Selection is Based off of
		param1 = arcpy.Parameter(
			displayName = "Field Name",
			name = "field_name",
			datatype = "Field",
			parameterType = "Required",
			direction = "Input")
		param1.parameterDependencies = [param0.name]
		param1.filter.list = ["LONG", "SHORT"]
		
		# Outpath
		param2 = arcpy.Parameter(
			displayName = "Output Folder",
			name = "field_value",
			datatype = "GPFeatureLayer",
			parameterType = "Required",
			direction = "Output")
		
		# list of parameters for tool
		parameters = [param0,param1,param2]
		return parameters
		
	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def execute(self, parameters, messages):

		infc = parameters[0].valueAsText
		field = parameters[1].valueAsText
		infc_directory = arcpy.Describe(infc).catalogPath
		infc_name = arcpy.Describe(infc).file
		
		env.workspace = infc_directory
		# Isolate the range of values in present_values list
		field_values = []
		rows = arcpy.SearchCursor(infc_directory,fields = "Dist_ID")
		for row in rows:
			instance = row.getValue("Dist_ID")
			field_values.append(instance)
	
		value_set = set(field_values)
		present_values = list(value_set)
		
		# Make a Layer from the Feature Class
		arcpy.management.MakeFeatureLayer(infc_name,'lyr')
		
		# Select based off attribute value and make a new feature class that is stored in Results folder.
		for i in present_values:
			arcpy.management.SelectLayerByAttribute('lyr', "NEW_SELECTION", '"Dist_ID" = ' + str(i) + '' )
			arcpy.management.CopyFeatures("lyr", os.path.join(os.path.split(infc_directory)[0],"district_" + str(i)))
		
		return True
		
# This builds districts based off of an attribute, Dist_ID. Returns a field class of joined District Polygons

class Tool_3(object):
	def __init__(self):
		"""Define the tool"""
		self.label = "Build_Districts"
		self.description = "Create District Polygon Feature Class based off Dist_ID attribute"
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""
		# Input Feature Class 
		param0 = arcpy.Parameter(
			displayName = "Input Feature Class",
			name = "in_feature",
			datatype = "DEFeatureClass",
			parameterType = "Required",
			direction = "Input")
		
		# only accept Polygon Feature Class
		param0.filter.list = ["Polygon"]
		
		# Name of Field to be Added
		param1 = arcpy.Parameter(
			displayName = "Field Name",
			name = "field_name",
			datatype = "Field",
			parameterType = "Required",
			direction = "Input")
		param1.parameterDependencies = [param0.name]
		param1.filter.list = ["LONG", "SHORT"]
		
		# Outpath
		param2 = arcpy.Parameter(
			displayName = "Output Folder",
			name = "field_value",
			datatype = "GPFeatureLayer",
			parameterType = "Required",
			direction = "Output")
		
		# list of parameters for tool
		parameters = [param0,param1,param2]
		return parameters
		
	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def execute(self, parameters, messages):
		infc = parameters[0].valueAsText
		outfc = parameters[2].valueAsText
		env.workspace = os.path.split(infc)[0]
		
		n = numDistricts(infc)
		
		
		# Create Layer from id (default layer name is lyr)
		arcpy.management.MakeFeatureLayer(infc, "lyr")
		# Dissolve layer
		arcpy.management.Dissolve(infc,outfc,"Dist_ID")
		# add dissolveed layer to district_layers array
		
		# join all members of district_layers array
		# use copy feature management toool to create a new feature class that is held under outfc.
			
		
		
		

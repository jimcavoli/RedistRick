import _tkinter
import Tkinter as tk
import tkMessageBox
import arcpy
import district_stats
from arcpy import env

class RedistrictingResults(tk.Frame):
    def __init__(self, district_layer, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('Redistricting Results')
        self.grid()
        self.configureGrid()
        if tkMessageBox.askquestion("Redistricting Plan",
                                    "Continue defining districts?") == False:
            self.quit
        self.createWidgets(district_layer)

    def configureGrid(self):
        top = self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)
        top.columnconfigure(2, weight=1)
        top.rowconfigure(0, weight=1)
        top.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

    def createWidgets(self, district_layer):
        self.diretions = tk.Label(self, justify=tk.LEFT,
                                  text=(
                                    "The results of the redistricting plan "
                                    "you designed are summarized here.\n"
                                    "Export will allow you to save a new "
                                    "shapefile with polygons\nof these "
                                    "boundaries.\nReport lets you export "
                                    "a CSV file containing summary "
                                    "statistics\nbased on the fields chosen "
                                    "below in the select boxes."
                                  ))
        self.diretions.grid(columnspan=3, sticky=tk.E+tk.W)
        self.buildFieldSelect(district_layer)
        self.createActionButtons()

    def createActionButtons(self):
        self.actionsFrame = tk.Frame(self)

        self.reportButton = tk.Button(self.actionsFrame, text='Report',
            command=self.report, justify=tk.RIGHT)
        self.exportButton = tk.Button(self.actionsFrame, text='Export',
            command=self.export, justify=tk.RIGHT)
        self.quitButton = tk.Button(self.actionsFrame, text='Finish',
            command=self.quit, justify=tk.RIGHT)

        self.reportButton.grid(column=0, row=0, sticky=tk.E+tk.W)
        self.exportButton.grid(column=1, row=0, sticky=tk.E+tk.W)
        self.quitButton.grid(column=2, row=0, sticky=tk.E+tk.W)

    def buildFieldSelect(self, district_layer):
        self.fieldLabel = tk.Label(self, justify=tk.RIGHT,
                                   text='Field to Summarize:')
        self.fieldLabel.grid(column=1, row=1, sticky=tk.E)

        fieldList = arcpy.ListFields(district_layer)
        self.selectedField = tk.StringVar()
        self.selectedField.set(None)

        self.fieldSelector = tk.OptionMenu(self, self.selectedField,
                                           *fieldList, command=self.fieldChange)
        self.fieldSelector.grid(column=2, row=1, sticky=tk.E+tk.W)

    def fieldChange(self, value):
        tkMessageBox.showinfo("You changed stuff.", "Now you say " + value)

    def export(self):
        tkMessageBox.showinfo("You changed stuff.", 'You clicked Export.')

    def report(self):
        tkMessageBox.showinfo("You changed stuff.", 'You clicked Report.')

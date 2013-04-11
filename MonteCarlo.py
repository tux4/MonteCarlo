#####################################
# Prasanna Suman   
# GNU GPL 3.0
# ------------
# The library for Monte Carlo simulation 
# and visualization
#
####################################
import random
import numpy
from Tkinter import *
import threading

class Basic(object):
    """Basic is the fundamental object that everything else inherits
       For example
       """
    def __init__(self):
        self.properties = {} 
        self.addProperty('_id', numpy.int_)
         
    def addProperty(self, name, data_type=numpy.float_):
        """Add new property to the base object that's 
            kept in the properties dict"""
        self.properties[name] = data_type
         
    def hasProperty(self, name):
        """Returns True if a supplied property exists in the object
        """
        return name in self.properties.keys()

    def getProperty(self, name):
        """Returns the property
        """
        assert self.hasProperty(name)
        return self.properties[name]

    def removeProperty(self, name):
        """Remove the property
        """
        del(self.properties[name])

    def printProperty(self):
        """Print the property dict
        """
        print self.properties

    def getAllProperty(self):
        """Return entire property dict
        """
        return self.properties

    def __repr__(self):
        return self.properties

    def __str__(self):
        return str(self.properties)

class Site(Basic):
    """Contains the values for all the fields at a given time"""
    def __init__(self):
        Basic.__init__(self)

class GenericSite(Basic):
    """Used to define a generic site, which is used only during
       initialization"""
    def __init__(self):
        Basic.__init__(self)

class Grid(Basic):
    """Grid contains all the matrixes and variables of a state 
       in a given shape for the simulation
       For each property in the generic object a numpy array is created.
       Besides the grid can also have separate properties which it inherits
       from Basic object, examples could be total energy of field 
       at a given step of simulation."""

    def __init__(self, shape, generic_site):   
        super(Grid, self).__init__()        
        self.shape = shape
        self.generic_site = generic_site
        self.initializeTables()

    def initializeTables(self):
        """Initialize numpy arrays for all the properties
        """
        all_property = self.generic_site.getAllProperty()
        for prop_name, prop_type in all_property.items():
            self.addProperty(prop_name, numpy.zeros(self.shape, dtype=prop_type))      

    def initializePropertyTable(self, prop_name, init_method):
        """As of now we must override this method for all cases of 
           non-2-dimensional shapes.
           TODO: Implement recursively for n-dimension"""
        assert self.hasProperty(prop_name)
        assert len(self.shape) == 2
        for i in range(0, self.shape[0]):
            for j in range(0, self.shape[1]):
                self.properties[prop_name][i, j] = init_method()
                
                 
    def getSite(self, position):
        """Return the site at a given position on the grid.
        """
        assert len(position) == len(self.shape)
        site = Site()
        for prop_name in self.generic_site.getAllProperty().keys():
            site.addProperty(prop_name, self.getProperty(prop_name)[position])
        return site
             
    
class SimVis(object):
    """The main Simulation and Visualization class
    """
    def __init__(self, grid, width):
        self.visualization = True #If disabled, visualizaion is not updated
        self.refresh = 100 #nth step of simulation in which visualization is updated 
        self.step = 0 #Counter for the number of step in simulation
        self.grid = grid #Main grid object that stores the data of simulation
        self.shape = self.grid.shape #Shape of the grid. E.g 100x100
        width = width#Supplied width of the visualization window 
        height = self.shape[0] * width / self.shape[1]#Height 
        self.size = (width, height)#Store it
        #Tkinter stuff here
        self.master = Tk()
        self.frame = Frame(self.master)
        self.frame.grid(sticky = E+W+N+S)
        self.grid_disp = Canvas(self.frame, width = width, height = height)
        self.grid_disp.grid(row = 1, column = 2, rowspan = 2, columnspan =4, sticky = N)
        self.drawGrid()
        self.frame.update_idletasks()
        self.master.after(2000, self.stepSimulation)

    def stepSimulation(self):
        """Each monte carlo step of the simulation.
           The is where the main code goes."""
        self.step += 1
        if not(self.step % self.refresh):
            if self.visualization: self.drawGrid()
        #To run simulation as part of tkinter event loop
        self.master.after(10, self.stepSimulation)
        
            
    def drawGrid(self):
        """Draws the grid. Works only for 2-d grid
        """  
        for i in range(0, self.shape[0]):
            for j in range(0, self.shape[1]):
                site = self.grid.getSite((i, j))
                self.drawSite(site)
                 

    def drawSite(self, site):  
        """User must define how a custom site will look lile.
           See the example for PiMC
        """
        pass
    
    def startSimulation(self):
        """Simulation and visualization starter
        """
        self.master.mainloop()

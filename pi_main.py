####################################
# Prasanna Suman
# This Monte Carlo simulation calculates 
# the value of Pi = 3.14159...
# 
#
#
#
###################################
import random
import MonteCarlo as mc 
from PiSim import PiMC

#The following methods are grid->site->variable initialization

def init_method_random():
    """Initialize a property as random, e.g. spin of sites
    in case of Ising model"""
    return random.choice([-1, 1])

id_value = -1 
def init_method_id():
    """Id initializes which every grid has"""
    global id_value
    id_value += 1
    return id_value

def init_method_xy(table_x, table_y):
    """Initializes table for co-ordinate of values
    Used in MonteCarlo simulation of PI"""
    for i in range (0, shape[0]):
        for j in range (0, shape[1]):
            table_x[i, j] = j/ float(shape[1] -1)
            table_y[i, j] = i/ float(shape[0] -1)
    return table_x, table_y

#Here begins the simulation for PI
shape = (100, 100) #This is the shape of the grid, higher means slower but better approximations
a = mc.GenericSite() #A generic site stores all the properties associated with a single site on the grid
a.addProperty("x") #property for x-coordinate
a.addProperty("y")
a.addProperty("circle")

g = mc.Grid(shape, a) #Grid for simulation

g.initializePropertyTable("_id", init_method_id) 
init_method_xy(g.getProperty("x"), g.getProperty("y"))

simulation = PiMC(g, 500) #Simulation and Visualization object
simulation.visualization = True #Try changing this to speed up 
simulation.startSimulation()

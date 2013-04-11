################################
# Prasanna Suman
# This is a supporter file for Simulation 
# of Pi. It implements the interface set
# by SimVis class for Pi
##############################
import random
import monteCarlo as mc

class PiMC(mc.SimVis):
    def __init__(self, grid, width):
        self.total_in_circle = 0 #Counter for random sites that fall in the circle
        super(PiMC, self).__init__(grid, width)
         
    def stepSimulation(self):
        """Each step of the Monte Carlo simulation for pi
        """
        shape = self.shape
        #Fetch a random site
        random_position = (random.choice(range(0, shape[0])), random.choice(range(0, shape[1])))
        random_site = self.grid.getSite(random_position)
        x_value = random_site.getProperty("x")
        y_value = random_site.getProperty("y") 
        #Check if it falls in the 1/4th circle
        if (x_value*x_value + y_value*y_value) < 1:
            if not self.grid.getProperty("circle")[random_position]:
                self.grid.getProperty("circle")[random_position] = 1
                self.total_in_circle += 1 
        #pi = 4 * total random boxes in unit circle / total boxes in unit squate
        pi = 4 * self.total_in_circle / float(self.shape[0] * self.shape[1])
        print "After iteration %s steps, on a grid %s, approximated value: %s" %(self.step, self.shape, pi)
        super(PiMC, self).stepSimulation()

    def drawSite(self, site):
        """Draw the sites based on the current state of simulation
        """
        size_x = self.size[0] / float(self.shape[1])
        size_y = self.size[1] / float(self.shape[0])
        site_properties = site.getAllProperty()
        x = (site_properties["x"] * self.shape[0])
        y = (site_properties["y"] * self.shape[1])
        spin = site_properties["circle"]
        if spin == 0:
            color = "green"
        else:
            color = "grey50"
        self.grid_disp.create_rectangle([x*size_x, y*size_y, (x+1)* size_x, (y+1)*size_y], fill=color)  
    

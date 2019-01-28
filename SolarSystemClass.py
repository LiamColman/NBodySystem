from PlanetClass import Particle
import numpy as np
import math

class Solar_System:
    """

    This class initialised all of the planets of the solar system that are inputted through the addPlanet function and then can be used to update each Planets
    acceleration.
    
    Inputted planets need to be an instance of the PlanetClass so that each planet has different properties that can be accessed by further code.

    This class also calculates the total potential and kinetic energy, which is then used in the main class for analysis.

    """

    def __init__(self):
        self.PlanetList = []
        self.TotalKineticEnergy = []
        self.TPE

    def __repr__(self):
        for i in range(len(self.PlanetList)):
            A = self.PlanetList[i]
            return '%s, Mass: %.5e, Position: %s, Velocity: %s, Acceleration: %s' %(A.Name, A.mass, A.position, A.velocity, A.acceleration)

    def acceleration_update(self):
        '''This runs through every planet and calculates the accleration due to each other planet'''
        for i in range(len(self.PlanetList)): 

            self.PlanetList[i].acceleration = [0.,0.,0.] # This ensures that the acceleration is reset, so that the acceleration doesn't just keep adding to the previous value
            
            for j in range(len(self.PlanetList)):

                if j != i: #This ensures that the acceleration calculation does not include the interaction of the planet on itself

                    seperation = self.PlanetList[i].position - self.PlanetList[j].position

                    MagOfSeperation = np.linalg.norm(seperation)
                   
                    UnitVector = seperation/MagOfSeperation
   
                    self.PlanetList[i].acceleration += ((-1.*self.G*self.PlanetList[j].mass)/(MagOfSeperation**2))*UnitVector


    
    def TotalKineticEnergyCalc(self):
        '''This calculates the total kinetic energy of the system, by adding up the kinetic energy of every body from the Particle class'''
        self.TotalKineticEnergy = 0
        for i in range(len(self.PlanetList)):
            self.TotalKineticEnergy += self.PlanetList[i].KineticEnergyCalc()
        return self.TotalKineticEnergy

    def TotalPotentialEnergyCalc(self):
        '''Calculates potential energy of every body by running through each planet, and not including itself '''
        self.TPE = 0  
        for i in range(len(self.PlanetList)): # This runs through each Planet to begin calculating the potential energy due to each other Planet
                   
            for j in range(len(self.PlanetList)):

                if j != i: #This ensures that the acceleration calculation does not include the interaction of the planet on itself

                    seperation = self.PlanetList[i].position - self.PlanetList[j].position
    
                    self.TPE += ((self.G*self.PlanetList[i].mass*self.PlanetList[j].mass)/(np.linalg.norm(seperation)))
        return self.TPE


    def addPlanet(self, aplanet): 
        '''This takes the planets we want to add, and appends a list in this class, which is then used by other methods.'''
        self.PlanetList.append(aplanet)




    G = 6.67408e-11
    PlanetList = []
    TotalKineticEnergy = 0 
    TPE = 0
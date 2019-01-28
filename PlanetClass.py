import numpy as np

class Particle:

    """

    This takes the initial position, velocity, acceleration and mass of the particle and simulates a projectile with constant acceleration through multiple time
    steps using Euler-Cromer method. 

    All initial values will be converted to a numpy array of length 3, not including Name and mass.

    This also calculates the kinetic energy of the instanced object

    Mass - kg
    Velocty - m/s
    Acceleration - m/s^2
    Position - m
    Kinetic Energy - J
    
    """

    def __init__(self, initialPosition, initialVelocity, initialAcceleration, Name, mass, method):
        self.position = np.array(initialPosition)
        self.velocity = np.array(initialVelocity)
        self.acceleration = np.array(initialAcceleration)
        self.Name = Name
        self.mass = mass
        self.setMethod(method)
        self.KineticEnergy = 0
        self.method = method


    def __repr__(self):
        return 'Planet: %10s, Mass: %.5e, Position: %s, Velocity: %s, Acceleration:%s' %(self.Name,self.mass,self.position, self.velocity,self.acceleration)


    def update(self, deltaT):
        '''Updates position and velcoity depending on which approximation user has picked in main file'''
        self.approximation(deltaT)


    def setMethod(self, method):
        '''Takes in a method variable to change what approixmation will be used when we want to update the planet's positions'''
        self.approximation = self.EulerCromer
        if method == 2:
            self.approximation = self.EulerForward


    def EulerCromer(self, deltaT):
        '''Uses Euler-Forward approximation for position and velocity'''
        self.velocity = self.velocity + self.acceleration*deltaT
        self.position = self.position + self.velocity*deltaT
        
 
    def EulerForward(self, deltaT):
        '''Uses Euler-Forward approximation for position and velocity'''
        self.position = self.position + self.velocity*deltaT   
        self.velocity = self.velocity + self.acceleration*deltaT


    def KineticEnergyCalc(self):
        '''Works out kinetic energy of each body'''
        self.KineticEnergy = (1/2)*self.mass*(np.linalg.norm(self.velocity))**2
        return self.KineticEnergy

    
    position = np.array([0.,0.,0.])
    velocity = np.array([0.,0.,0.])
    acceleration = np.array([0.,0.,0.])
    KineticEnergy = 0
    Name = ''
    mass = 1.
    approximation = EulerCromer
#ayyyyyy lmao
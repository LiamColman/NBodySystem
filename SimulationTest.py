from Main import Simulation

'''
To start simulating the solar system, the functions that are needed are already written out in this file. To just simulate the solar system,
comment out the sections underneath the docstring that says Analysis, and uncomment the simulation method. To just analyse the data, comment out 
the simulation method, and uncomment which analysis tests you want to do.
'''


Simulate = Simulation() # DO NOT REMOVE

Simulate.SetupSolarSystem() #DO NOT REMOVE

'''
Simulation method
'''

Simulate.SimulateSolarSystem()

'''
Analysis methods
'''

Simulate.KineticEnergy()
Simulate.PotentialEnergy()
Simulate.PositionGraph()
Simulate.OrbitalPeriod()
Simulate.AngularMomentum()
Simulate.VirialTheorem()
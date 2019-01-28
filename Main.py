from SolarSystemClass import Solar_System
from PlanetClass import Particle
import PlanetDetails
import numpy as np
import matplotlib.pyplot as plt
import PlanetDetails
import time
import copy
import numpy.polynomial.polynomial as poly

class Simulation():
    """
    
    This takes no arguments, and sets up the solar system, which then is simulated by using the Particle and Solar_System classes

    User input is required to set the deltaT, TotalTime and the number of planets that need to be simulated.
    
    Parameters taken in:
    TotalTime: User input required, input in years
    deltaT : User input required, input in seconds
    method : User input required, use either 1 (Euler Forward) or 2 (Euler Cromer)
    Planet : User input required, choose from a set list of planets, appends to Planet list

    Data members:
    DataEng (list) : Appends Energy data to it, and saves to be used in analysis functions
    DataPos (list) : Appends positional data to it, and saves to be used in analysis functions
    ProgressTime (float) : Keeps track of time, used in percent calculation
    StepsForEnergy (float) : Updates every 40 deltaTs and appends to the DataEng or DataPos

    Returns:
    No values returned in methods : SetupSolarSystem(), SimulateSolarSystem()
    Figures returned in methods : PositionGraph(), KineticEnergy(), AngularMomentum(), PotentialEnergy(), TotalEnergy()

    """
    

    def __init__(self):
        self.Planet = []
        self.DataEng = []
        self.DataPos = []
        self.TotalTime = 86400*365*float(input('Please input how many years you want the simulation to run over: ')) #Final number is the number of years you want the simulation to run
        self.deltaT = float(input('Please input the time step you want for the simulation (seconds): ')) #This is the time step that the simulation takes

        if self.TotalTime <= 0 or self.deltaT <= 0: #This is error checking so that the inputted numbers can be used by the simulation
            raise ValueError('Time should not be negative/zero')
        if self.deltaT >= self.TotalTime:
            raise ValueError('Time step should not be larger than total time')

        self.StepsForEnergy = self.deltaT 
        self.ProgressTime = 0 
        self.SolarSystem = Solar_System()
        

    def SetupSolarSystem(self):
        '''Takes user input to change the Total time, deltaT and the method used, and appends all user inputted planets to the list that will be used in simulation'''
        InputPlanets = []
        Loop = True
        while Loop == True:
            #This asks user to input planets to be simulated
            PlanetName = input('Give the name of the planet you want to simulate: ')
            for i in range(len(PlanetDetails.AllPlanetDetails)):
                if PlanetName == 'All':
                    #If All is passed, then all of the planets will be added to the list to simulate
                    InputPlanets = PlanetDetails.AllPlanetDetails
                    Loop = False
                elif PlanetName == PlanetDetails.AllPlanetDetails[i].Name:
                    #This will parse through all planet details to find if the user input is in the list
                    InputPlanets.append(PlanetDetails.AllPlanetDetails[i])

            if Loop == False:
                break

            #This asks if the user would like to contiue adding planets to simulate, if not then the loop breaks, and adds said Planets to a list
            cont = input('Add another planet?: (Y/N)')
            if cont == 'Y':
                continue
            elif cont == 'N':
                break

        

        self.Planet = [[0 for col in range(1)] for row in range(len(InputPlanets))]
        self.SolarSystem.addPlanet(PlanetDetails.Sun)
        self.Planet.append(PlanetDetails.Sun)
        #This part appends all of the inputted planets in a list that is used by all methods in this class
        for i in range(len(InputPlanets)):
            self.Planet[i] = InputPlanets[i]
            print(self.Planet[i])
            self.SolarSystem.addPlanet(self.Planet[i])

        AskForMethod = int(input('Please select which method you want to use: (1/2) '))
        if AskForMethod == 2:
            for i in range(len(self.Planet)):
                self.SolarSystem.PlanetList[i].setMethod(2)

    def SimulateSolarSystem(self):
        '''
        Takes the user defined terms and then loops over the TotalTime with steps of deltaT. This uses the Particle class to update position and velocity, and uses the 
        SolarSystem class to update the acceleration of each body. Percentage is also calculated and displayed to user via terminal. All data is saved every 40 time-steps.
        '''
        Percent = 0
        start = time.time()
        for _ in np.arange(0, self.TotalTime, self.deltaT):
            #Loop over the total time in the steps of deltaT
            self.ProgressTime += self.deltaT

            self.SolarSystem.acceleration_update()
            
            if int((self.ProgressTime*100)/self.TotalTime) > Percent: 
                # This calculates the percentage and then compares against the printed value of percentage, so it doesn't repeat

                Percent = int((self.ProgressTime*100)/self.TotalTime)
                Timenow = time.time()
                Timefromstart = Timenow - start
                Timeremaining = (Timefromstart*(100/Percent))-Timefromstart
                print('Simulation is %s %% complete \nTime remaining: %d seconds'%(Percent, Timeremaining))

            for k in range(len(self.SolarSystem.PlanetList)):
                #This updates for each body in the solar system, and calculates the acceleration, and then the position
                self.SolarSystem.PlanetList[k].update(self.deltaT)
            

            if self.ProgressTime == self.StepsForEnergy:
                #This adds positional and energy data to a list every 40 time steps, which can be used in later analysis
                itemPos = [self.ProgressTime]
                itemEng = [self.ProgressTime]
                self.StepsForEnergy += 40*self.deltaT
                for p in range(len(self.SolarSystem.PlanetList)):
                    KineticEnergy = self.SolarSystem.PlanetList[p].KineticEnergyCalc()
                    itemPos.append(copy.deepcopy(self.SolarSystem.PlanetList[p]))
                    itemEng.append(copy.deepcopy(KineticEnergy))
                TotalKineticEnergy = self.SolarSystem.TotalKineticEnergyCalc()
                TotalPotentialEnergy = self.SolarSystem.TotalPotentialEnergyCalc()
                itemEng.append(TotalKineticEnergy)
                itemEng.append(TotalPotentialEnergy)
                self.DataPos.append(itemPos)
                self.DataEng.append(itemEng)


        end = time.time()

        TimeOfCalculation = end - start
        print('Simulation time: %s'%(TimeOfCalculation))


        np.save('Positional_data_%s_years_%ss_timestep_%s_bodies_%s' %((self.TotalTime/(86400*365)), self.deltaT, len(self.Planet) ,self.SolarSystem.PlanetList[0].method), self.DataPos)
        print('Positional data saved')
        np.save('Energy_data_%s_years_%ss_timestep_%s_bodies_%s' %((self.TotalTime/(86400*365)), self.deltaT, len(self.Planet) , self.SolarSystem.PlanetList[0].method), self.DataEng)
        print('Energy data saved')

    def PositionGraph(self): 
        '''This takes the saved data from the simulation and extracts each planets position, which is then plotted on a graph'''
        LoadData = np.load('Positional_data_%s_years_%ss_timestep_%s_bodies_%s.npy' %((self.TotalTime/(86400*365)), self.deltaT, len(self.Planet) ,self.SolarSystem.PlanetList[0].method))
        xpos = [[0 for col in range(1)] for row in range(len(LoadData[0])-1)] 
        ypos = [[0 for col in range(1)] for row in range(len(LoadData[0])-1)]
        Time = []
        Planets = [[0 for col in range(1)] for row in range(len(LoadData[0])-1)]

        #Extraction of data
        for line in LoadData:  
            Time.append(line[0])

            for i in range(1,len(Planets)+1):
                Planets[i-1].append(line[i])
        for j in range(len(Planets)):
            Planets[j].pop(0)

        for j in range(len(xpos)):
            for k in range(len(Time)):
                xpos[j].append(Planets[j][k].position[0])
                ypos[j].append(Planets[j][k].position[1])
        for i in range(len(Planets)):
            xpos[i].pop(0)
            ypos[i].pop(0)
            plt.plot(xpos[i],ypos[i], '-', label = '%s Position' %(Planets[i][i].Name) )
        plt.xlabel('X position [m]')
        plt.ylabel('Y position [m]')
        plt.legend(loc = 1)
        plt.title('Solar system of %s bodies, \n %s years, time step of %s seconds' %( len(self.Planet), self.TotalTime/(86400*365), self.deltaT))
        plt.savefig('Solar system of %s bodies %s years time step of %s seconds.png' %( len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
        plt.show()


    def KineticEnergy(self):
        '''This method extracts the kinetic energy calculated previously and then plot it over time'''
        LoadDataEng = np.load('Energy_data_%s_years_%ss_timestep_%s_bodies_%s.npy' %((self.TotalTime/(86400*365)), self.deltaT, len(self.Planet) , self.SolarSystem.PlanetList[0].method))
        ChangeinKE = []
        KineticEnergy = []
        Time = []

        #Extraction of data
        for line in LoadDataEng:  
            Time.append(line[0])

        for line in LoadDataEng:
            TotalKinetic = line[len(self.Planet)+1]
            KineticEnergy.append(TotalKinetic)


        ChangeinEnergyCalc = False
        Answer = str(input('Do you want to include Change in Kinetic Energy? (Y/N)'))
        if Answer == 'Y':
            ChangeinEnergyCalc = True

    


        plt.plot(Time,KineticEnergy, '-', label = 'Total kinetic energy')
        plt.xlabel('Time [s]')
        plt.ylabel('Total Kinetic Energy [J]')
        plt.legend(loc = 0)
        plt.title('Total Kinetic Energy of %s bodies,  \n %s years, time step of %s seconds, \n Standard Deviation: %s  Mean: %s \n' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT, '{:0.3e}'.format(np.std(KineticEnergy)), '{:0.3e}'.format(np.average(KineticEnergy))))
        plt.savefig('Total Kinetic Energy of %s bodies %s years time step of %s seconds.png' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
        plt.show()

        if ChangeinEnergyCalc == True:

            for i in range(1, len(LoadDataEng)): 
                ChangeinKE.append(((KineticEnergy[i] - KineticEnergy[0])/KineticEnergy[0])*100)
        
            Time.pop(0)
            plt.plot(Time,ChangeinKE, '-', label = 'Total kinetic energy')
            plt.xlabel('Time [s]')
            plt.ylabel('Total Kinetic Energy [J]')
            plt.legend(loc = 0)
            plt.title('Percentage change in kinetic energy of %s bodies,  \n %s years, time step of %s seconds, \n Standard Deviation: %s  Mean: %s \n' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT, '{:0.3e}'.format(np.std(ChangeinKE)), '{:0.3e}'.format(np.average(ChangeinKE))))
            plt.savefig('Percentage change in kinetic energy of %s bodies %s years time step of %s seconds.png' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
            plt.show()


    def AngularMomentum(self):
        '''This method extracts each planets mass and position, calculates the systems centre of mass, which is then used to find the system's angular momentum'''
        LoadData = np.load('Positional_data_%s_years_%ss_timestep_%s_bodies_%s.npy' %((self.TotalTime/(86400*365)), self.deltaT, len(self.Planet) ,self.SolarSystem.PlanetList[0].method))
        Time = []
        AngularMomentumList = []
        ChangeinAngularMomentum = []
        Planets = [[0 for col in range(1)] for row in range(len(LoadData[0])-1)]

        #Extraction of data
        for line in LoadData:  
            Time.append(line[0])

            for i in range(1,len(Planets)+1):
                Planets[i-1].append(line[i])
        for j in range(len(Planets)):
            Planets[j].pop(0)


        for k in range(len(Time)):
            AngularMomentum = 0
            massposition = 0
            totalmass = 0 
            for n in range(len(Planets)):
                massposition += Planets[n][k].mass*Planets[n][k].position
                totalmass += Planets[n][k].mass
                centreofmass = massposition/totalmass #Calculate centre of mass of the whole system depending on each bodies mass and the distance from the origin
                LinearMomentum = Planets[n][k].velocity*Planets[n][k].mass
                AngularMomentum += np.linalg.norm(np.cross(Planets[n][k].position - centreofmass, LinearMomentum))
            AngularMomentumList.append(AngularMomentum)

        ChangeinMomentumCalc = False
        Answer = str(input('Do you want to include Change in Angular Momentum? (Y/N)'))
        if Answer == 'Y':
            ChangeinMomentumCalc = True

        
        plt.plot(Time, AngularMomentumList, '-', label = 'Angular momentum')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.xlabel('Time [s]')
        plt.ylabel('Angular momentum [m^2kgs^-2]')
        plt.legend(loc = 1)
        plt.title('Angular momentum of %s bodies,  \n %s years, time step of %s seconds, \n Standard Deviation: %s  Mean: %s \n' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT, '{:0.3e}'.format(np.std(AngularMomentumList)), '{:0.3e}'.format(np.average(AngularMomentumList))))
        plt.savefig('Angular momentum of %s bodies %s years time step of %s seconds.png' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
        plt.show()

        if ChangeinMomentumCalc == True:

            for i in range(1, len(LoadData)): 
                ChangeinAngularMomentum.append(((AngularMomentumList[i] - AngularMomentumList[0])/AngularMomentumList[0])*100)

            Time.pop(0)

            plt.plot(Time, ChangeinAngularMomentum, '-', label = 'Percentage Change in angular momentum')
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            plt.xlabel('Time [s]')
            plt.ylabel('Percentage change in angular momentum')
            plt.legend(loc = 1)
            plt.title('Percentage change of angular momentum of %s bodies,  \n %s years, time step of %s seconds, \n Standard Deviation: %s  Mean: %s \n' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT, '{:0.3e}'.format(np.std(ChangeinAngularMomentum)), '{:0.3e}'.format(np.average(ChangeinAngularMomentum))))
            plt.savefig('Percentage change of angular momentum of %s bodies %s years time step of %s seconds.png' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
            plt.show()

    def OrbitalPeriod(self):
        '''This method calculates the orbital period of each planet, and sees how much it varies over time'''
        LoadData = np.load('Positional_data_%s_years_%ss_timestep_%s_bodies_%s.npy' %((self.TotalTime/(86400*365)), self.deltaT, len(self.Planet) ,self.SolarSystem.PlanetList[0].method))
        PositionsfromSun = []
        Time = []
        PositionsofPlanets = []
        OrbitalPeriod = []
        ChangeinOrbitalPeriod = []
        Planets = [[0 for col in range(1)] for row in range(len(LoadData[0])-1)]

        for line in LoadData:  
            Time.append(line[0])
            for i in range(1,len(Planets)+1):
                Planets[i-1].append(line[i])
        for j in range(len(Planets)):
            Planets[j].pop(0)

        for l in range(len(Planets)):
            PositionsofPlanets.append([])
            for j in range(len(LoadData)):
                Position = Planets[l][j].position
                PositionsofPlanets[l].append(Position)

        for l in range(len(Planets)):
            PositionsfromSun.append([])
            OrbitalPeriod.append([])
            for j in range(len(LoadData)):
                RadialDist = np.linalg.norm(PositionsofPlanets[l][j]-PositionsofPlanets[0][j])
                OrbitalPeriod[l].append((RadialDist/1.496e11)**(3/2)) #Uses Kepler's Law to calculate the orbital period
            print('Orbital period of %s :%s' %(Planets[l][l].Name, np.average(OrbitalPeriod[l])))    

        StabilityOfOrbit = False #User input needed to as if the user if they want an additional graph
        Answer = str(input('WARNING: Graph is very messy\nDo you REALLY want to include the Stability of the Orbital Period? (Y/N) '))
        if Answer == 'Y':
            StabilityOfOrbit = True
        
        
        for k in range(1, len(PositionsfromSun)): #This gets rid of the sun, as that value is just 0, so the log graph doesn't display it
            plt.plot(Time, OrbitalPeriod[k], '-', label = '%s Orbital Period' %(Planets[k][k].Name))
        plt.xlabel('Time [s]')
        plt.ylabel('Log of Orbital Period [yr]')
        ax = plt.subplot(111)
        chartbox = ax.get_position() #Used to put the legend outside of the graph
        ax.set_position([chartbox.x0, chartbox.y0, chartbox.width*0.6, chartbox.height])
        ax.legend(loc = 'upper center', bbox_to_anchor=(1.45,0.8), shadow = True, ncol = 1) #Sets the legend to be outside of the plot 
        plt.yscale('log')
        plt.title('Log of Orbital Period over time of %s bodies, \n %s years, time step of %s seconds' %( len(self.Planet), self.TotalTime/(86400*365), self.deltaT))
        plt.savefig('Log of Orbial Period over time of %s bodies %s years time step of %s seconds.png' %( len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
        plt.show()

        if StabilityOfOrbit == True:
            OrbitalPeriod.pop(0)
            for m in range(len(OrbitalPeriod)):
                ChangeinOrbitalPeriod.append([])
                for k in range(len(LoadData)):
                    ChangeinOrbitalPeriodCalc = ((OrbitalPeriod[m][k]-OrbitalPeriod[m][0])/OrbitalPeriod[m][0])*100
                    ChangeinOrbitalPeriod[m].append(ChangeinOrbitalPeriodCalc)
            
            for j in range(len(ChangeinOrbitalPeriod)):
                plt.plot(Time, ChangeinOrbitalPeriod[j], '-', label = 'Stability of Orbital Period of %s' %(Planets[j+1][j].Name))
            plt.xlabel('Time [s]')
            plt.ylabel('Percentage change of Orbital Period')
            plt.legend(loc = 1)
            plt.title('Percentage change in Orbital Period over time of %s bodies, \n %s years, time step of %s seconds' %( len(self.Planet), self.TotalTime/(86400*365), self.deltaT))
            plt.savefig('Percentage change in Orbial Period over timeof %s bodies %s years time step of %s seconds.png' %( len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
            plt.show()


    
    def PotentialEnergy(self):
        '''This method extracts the potential energy worked out earlier, and then plots the change in potential over time'''
        LoadDataEng = np.load('Energy_data_%s_years_%ss_timestep_%s_bodies_%s.npy' %((self.TotalTime/(86400*365)), self.deltaT, len(self.Planet) , self.SolarSystem.PlanetList[0].method))
        ChangeinPE = []
        PotentialEnergy = []
        Time = []

        #Extraction of data
        for line in LoadDataEng:  
            Time.append(line[0])

        

        ChangeinEnergyCalc = False
        Answer = str(input('Do you want to include Change in Potential Energy? (Y/N)'))
        if Answer == 'Y':
            ChangeinEnergyCalc = True

        for line in LoadDataEng:
            TotalPotential = line[len(self.Planet)+2]
            PotentialEnergy.append(-1*TotalPotential)

        plt.plot(Time, PotentialEnergy, '-', label = 'Change in total potential energy')
        plt.xlabel('Time [s]')
        plt.ylabel('Total Potential Energy [J]')
        plt.legend(loc = 1)
        plt.title('Total Potential Energy of %s bodies,  \n %s years, time step of %s seconds, \n Standard Deviation: %s  Mean: %s \n' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT, '{:0.3e}'.format(np.std(PotentialEnergy)), '{:0.3e}'.format(np.average(PotentialEnergy))))
        plt.savefig('Total Potential Energy of %s bodies %s years time step of %s seconds.png' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
        plt.show()

        if ChangeinEnergyCalc == True:

            for i in range(1, len(LoadDataEng)): 
                ChangeinPE.append(((PotentialEnergy[i] - PotentialEnergy[0])/PotentialEnergy[0])*100)

            Time.pop(0)
            plt.plot(Time,ChangeinPE, '-', label = 'Change in total potential energy')
            plt.xlabel('Time [s]')
            plt.ylabel('Percentage change in Total Potential Energy')
            plt.legend(loc = 1)
            plt.title('Percentage change of total Potential Energy of %s bodies,  \n %s years, time step of %s seconds, \n Standard Deviation: %s  Mean: %s \n' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT, '{:0.3e}'.format(np.std(ChangeinPE)), '{:0.3e}'.format(np.average(ChangeinPE))))
            plt.savefig('Percentage change of total Potential Energy of %s bodies %s years time step of %s seconds.png' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
            plt.show()

    
    def VirialTheorem(self):
        '''This method extracts the kinetic and potential energy, and, using Virial theorem, calculates the value of this theorem, which is then plotted over time'''
        LoadDataEng = np.load('Energy_data_%s_years_%ss_timestep_%s_bodies_%s.npy' %((self.TotalTime/(86400*365)), self.deltaT, len(self.Planet) , self.SolarSystem.PlanetList[0].method))
        ChangeinTotalEnergy = []
        PotentialEnergy = []
        KineticEnergy = []
        TotalEnergy = []
        Time = []
        Timeplot = []
        TotalEnergyplot = []
        ChangeinTotalEnergyplot = []
      

        #Extraction of data
        for line in LoadDataEng:  
            Time.append(line[0])


        for line in LoadDataEng:
            TotalKinetic = line[len(self.Planet)+1]
            TotalPotential = line[len(self.Planet)+2]
            PotentialEnergy.append(TotalPotential)
            KineticEnergy.append(TotalKinetic)


        #This is using the Virial theorem to calculation total energy
        for i in range(len(KineticEnergy)):
            TotalEnergy.append(2*KineticEnergy[i] - PotentialEnergy[i])

        ChangeinTotalEnergyCalc = False
        Answer = str(input('Do you want to include Change in Virial Theorem? (Y/N)'))
        if Answer == 'Y':
            ChangeinTotalEnergyCalc = True

        #This fits a line of best fit 
        Time_new = np.linspace(Time[0], Time[-1], num=len(Time)*10)
        coefficients = poly.polyfit(Time, TotalEnergy, 10)
        fit = poly.polyval(Time_new, coefficients)
        plt.plot(Time_new, fit, label = 'Best fit')
        
        for l in range(0,len(Time),int(len(Time)/200)):
            Timeplot.append(Time[l])
            TotalEnergyplot.append(TotalEnergy[l])


        plt.plot(Timeplot,TotalEnergyplot, 'o', markersize = 2, label = 'Value of Virial\'s Theorem')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.xlabel('Time [s]')
        plt.ylabel('Value of Virial\'s Theorem')
        plt.legend(loc = 1)
        plt.title('Value of Virial\'s Theorem of %s bodies,  \n %s years, time step of %s seconds, \n Standard Deviation: %s  Mean: %s \n' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT, '{:0.3e}'.format(np.std(TotalEnergy)), '{:0.3e}'.format(np.average(TotalEnergy))))
        plt.savefig('Value of Virial\'s Theorem of %s bodies %s years time step of %s seconds.png' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
        plt.show()

        if ChangeinTotalEnergyCalc == True:

            for j in range(1, len(LoadDataEng)):
                ChangeinTotalEnergy.append(((TotalEnergy[j] - TotalEnergy[0])/TotalEnergy[0])*100)
            Time.pop(0)
            Time_new = np.linspace(Time[0], Time[-1], num=len(Time)*10)
            coefficients = poly.polyfit(Time, ChangeinTotalEnergy, 10)
            fit = poly.polyval(Time_new, coefficients)
            plt.plot(Time_new, fit, label = 'Best fit')
        
            for l in range(0,len(Time),int(len(Time)/200)):
                ChangeinTotalEnergyplot.append(ChangeinTotalEnergy[l])
            
            plt.plot(Timeplot,ChangeinTotalEnergyplot, 'o', markersize = 3, label = 'Percentage change in the value of Virial\'s theorem')
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
            plt.xlabel('Time [s]')
            plt.ylabel('Percentage change in value of Virial\'s Theorem')
            plt.legend(loc = 1)
            plt.title('Percentage change in the value of Virial\'s Theorem of %s bodies,  \n %s years, time step of %s seconds, \n Standard Deviation: %s  Mean: %s \n' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT, '{:0.3e}'.format(np.std(ChangeinTotalEnergy)), '{:0.3e}'.format(np.average(ChangeinTotalEnergy))))
            plt.savefig('Percentage change in the value of Virial\'s Theorem of %s bodies %s years time step of %s seconds.png' %(len(self.Planet), self.TotalTime/(86400*365), self.deltaT), bbox_inches = 'tight')
            plt.show()
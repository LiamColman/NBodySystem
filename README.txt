Files included in this simulation and what they do:

PlanetClass.py:

This class creates objects that are used for the Planets, using a class called Particle. These are point-like objects so they don't have a size associated with them. The update method in this class 
updates the position and velocity of each instance of objects when they have been created in the Main file, which is iterated over every single time-step. Every 40 time-steps
the kinetic energy of every single object instanced is calculated and then fed back for the Solar System Class to sum up each kinetic energy.


SolarSystemClass.py:

This class creates the solar system that each instance created by the Particle Class is placed. The main function in this class is the acceleration update method, which 
calculates each planet's acceleration due to every other body, and then assigns it to be used by PlanetClass. Like the PlanetClass, this class contains 2 functions that
calculate the Total kinetic energy of the system, and the Total potential energy of the system. 


Main.py:

This class takes in user input to change the values for deltaT, TotalTime, method used, and what planets they want to use. When they input the desired planets, the corresponding
planets are then initialised through using the Particle class. When the user want to simulate the system, they will use the SimulateSolarSystem method. This method loops
over the total time for the simulation in steps defined by what deltaT the user inputted, and updates the acceleration (using the SolarSystemClass), velocities and positions
(using the Particle Class) for each planet. This also includes a print function to print the percentage elapsed and the time remaining to the terminal for the user to see.
This also saves the data every 40 time-steps to a seperate file that can be used in the analysis methods in the class. The analysis methods can be externally called and 
can be in any combination, using the SimulationTest. The methods are to find: Position of planets, Kinetic Energy, Angular Momentum, Orbital Period, Potential energy and Virial
theorem.


SimulationTest:

This contains the functions that call the Main file. There are functions that need to be there, which are commented as so. The user can comment out what they want to do
and what they don't want to do.


PlanetDetails.py

This file contains all of the data for the planets that can be simulated. The user input used in the simulation method in the Main file calls the data from this file,
and then appends it to its own list.



How to use the simulation:

To use the simulation, open up the file "SimulationTest.py". Here there is a short file that contains the functions that will begin the simulation of the solar system
using the planets of your choice. In this file there are 2 functions that are required to be there for the simulation to begin, and for the other functions to work, for
example, the "Simulation.SetupSolarSystem()" is needed even if you just want to do data analysis, as you can input the data you want to analyse in the user prompt.

When you run the simulation, the terminal will prompt you to input information that will change how the simulation will work. The questions and answers are below:

"Please input how many years you want the simulation to run over" 

Input any positive number to be the number of years that you want the simulation to run over, otherwise an error will be thrown. If the number is too large, then the
simulation will take a long time to run.

"Please input the time step you want for the simulation (seconds)"

Input any positive number to be the time step for the simulation, otherwise an error will be thrown. If the number for your time step is too large, the solar system will
run into problems, for example, planets escaping their orbit and being shot off into "space". Too small of a time step will mean that the simulation may take too long if
the amount of years inputted is also large.

"Give the name of the planet you want to simulate"

This gives the user options to input what planets they want. There is a select pool of planets to choose from, but the Sun is in every simulation. The selection
of planets are:
Mercury
Venus
Earth
Moon
Mars
Jupiter
Saturn
Saturn
Uranus
Neptune

If anything other than these options are inputted, then they will not be in the simulation

Using "All" inputs all of the Planets in one go

If you input a planet at a time, you will be given a choice of:

"Add another planet?: (Y/N)"

Input Y or N exactly to give your choice otherwise the loop just starts over again, until a correct input is made


After running simulation:

After the simulation has been run, the data will be saved in the form of "Energy/Positional_data_for_*_bodies_*_years_*_timestep_*" using, Number of bodies,
Total time (in years), deltaT (in seconds) and the method used (1 or 2)

This can then be accessed by the analysis methods in the class. If the functions are not commented out in the test file, then the analysis will be run straight after
the simulation has completed. If they have been commented out, then, providing SetupSolarSystem() is still able to run, you can run each analysis file individually after
simulation, and can access the data through inputting the required numbers for the data you would like.

For example, if you want to run analysis for 10 bodies, with 20 years total time, timestep of 1000s and using the Euler-Cromer approximation, you would input 
Totaltime = 20, deltaT = 1000, Planets = "All", method = 1.

Each analysis function will ask the user whether they would want to calculate the percentage change in the total amount, by either inputting Y or N exactly.

Each analysis function will output either 1 or 2 graphs, depending on what choice the user made for the previous question, and all of these figures will be saved
using the same method as is used for saving the files.
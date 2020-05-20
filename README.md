# simulating-woc
A Simulation-Based Approach to Understanding the Wisdom of Crowds Phenomenon in Aggregating Expert Judgment

The folder **Analysis** contains all scenarios, input data, and experiment setups for the scientific publication in Business & Information Systems Engineering. The results of the experiments are gathered in **Plots** and **Data**.

If you want to use the code base for your own simulation of WOC scenarios, all necessary classes (Experts, Events, Models, as well as data containers) are contained in the folder **Code**. First, have a look at Scenarios.py. This is the main class that creates a WOC scenario by reading from a pre-designed excel file, creating the necessary expert and event objects, and running the simulation.

Other starting points for a deeper understanding are:
* Event.py: A representation of events that can be forecasted
* Expert.py: A representation of experts that can forecast the abovementioned events
* Algorithm.py: An implementation of WOC aggregation algorithms

The use of all other classes can be derived from there.

For further information, help on setting up the simulation, or collaboration ideas please feel free to contact the author via christopher.vandun@fim-rc.de 

# SD-Refactoring-Assessment

This repository contains the submitted code, test and output files for Software Development Ractoring and Reflection Assessment.

The report has been submitted separately through Turnitin, together with the zipped code files.

The program is a Python-based command line implementation of the Ant Colonization method to solve small instances of the Travelling Salesman Problem.

The program is run through the command line using the following command:
python tspmain.py <number of cities to visit> <number of ants> <number of iterations> <number of repetitions> < alpha factor > <beta factor> <state transition probability> < pheromone evaporation coefficient > <city data file> <output file>

An example is given below:
python tspmain.py 12 20 20 1 0.1 1.0 0.5 0.99 citiesAndDistances.pickled output.pickled

import random
import sys


from tspworkingant import TSPWorkingAnt


class TSPColony:
    """
    #this class is the group of ants that will travel through the network
    #the colony is constantly being updated with the best path and its cost
    """


    def __init__(self, graph, num_ants, num_iterations, alpha, q0, rho, beta):
        """
        #the constructor
        """
        self.graph = graph                      #the network
        self.num_ants = num_ants                #number of ants in the colony
        self.num_iterations = num_iterations    #the maximum number of times all the ants work through the network
        self.Alpha = alpha                      #alpha controls the influence of pheromone level on choice of next node
        self.reset()
        self.q0 = q0
        self.rho = rho
        self.beta = beta


    def reset(self):
        """
        #to reset best path statistics
        """
        self.minimum_cost = sys.maxint      #re-initialize cost of best path        
        self.best_path = None               #resets best path to empty
        self.best_path_matrix = None        #resets best path matrix to empty
        self.best_iter_counter = 0          #keeps track of the number of iterations of best path 


    def start(self):
        """
        #creates the working ants,
        #controls the number of iteration and
        #update the network after each itertaion
        """
        self.ants = self.create_working_ants()
        self.iter_counter = 0

        while self.iter_counter < self.num_iterations:
            self.iteration()
            # Note that this will help refine the results future iterations.
            self.global_updating_rule()


    def iteration(self):
        """
        #in each itertaion, runs all the ants through the network
        """
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iter_counter += 1
        for ant in self.ants:
            ant.run()


    def num_ants(self):
        #gets number of ants in the colony
        return len(self.ants)


    def num_iterations(self):
        #gets maximum number of iterations
        return self.num_iterations


    def iteration_counter(self):
        #gets number of iterations so far
        return self.iter_counter


    def update(self, ant):
        """
        #if an ant finds better path statistics, it updates the colony
        """
        print "Update called by %s" % (ant.ID,)
        self.ant_counter += 1
        self.avg_path_cost += ant.path_cost
        if ant.path_cost < self.minimum_cost:
            self.minimum_cost = ant.path_cost
            self.best_path_matrix = ant.path_mat
            self.best_path = ant.path_vec
            self.best_iter_counter = self.iter_counter

        #if this is the last ant in the cony, calculate the average path cost
        #and display the current network best path statistics
        if self.ant_counter == len(self.ants):
            self.avg_path_cost /= len(self.ants)
            print "Best: %s, %s, %s, %s" % (
                self.best_path, self.minimum_cost, self.iter_counter, self.avg_path_cost,)


    def done(self):
        """
        returns true is the maximum numbe rof iterations has been reached
        """
        return self.iter_counter == self.num_iterations


    def create_working_ants(self):    
        """
        #creates and returns a list of working ants
        """
        self.reset()
        ants = []
        for i in range(0, self.num_ants):
            #each ant can start from any node in the network
            ant = TSPWorkingAnt(i, random.randint(0, self.graph.num_nodes - 1), self, self.q0, self.rho, self.beta)
            ants.append(ant)

        return ants
 

    def global_updating_rule(self):
        """
        #this updates the pheromone trails of all edges in the network
        #after each iteration, deposition happens on used paths and evaporation on ununsed paths
        """
        evaporation = 0
        deposition = 0
        for r in range(0, self.graph.num_nodes):
            for s in range(0, self.graph.num_nodes):
                if r != s:
                    delt_tau = self.best_path_matrix[r][s] / self.minimum_cost
                    evaporation = (1 - self.Alpha) * self.graph.tau(r, s)
                    deposition = self.Alpha * delt_tau
                    self.graph.update_tau(r, s, evaporation + deposition)


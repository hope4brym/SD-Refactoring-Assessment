import math
import random

class TSPWorkingAnt():  
    """
    #this class is the working ant which travels through the network.
    #the ant choses the next node based on the strength of the pheromone
    """

    def __init__(self, ID, start_node, colony, q0, rho, beta):
        """
        #this is the construcctor to initialize the important variables
        """
        self.ID = ID                    #the working ant needs an identity
        self.start_node = start_node    #the working ant needs node to start from
        self.colony = colony            
        self.curr_node = self.start_node
        self.graph = self.colony.graph
        self.path_vec = []              #the sequence of nodes chosen by the ant
        self.path_vec.append(self.start_node)
        self.path_cost = 0              #initialize the cost of path
        self.Beta = beta                #beta controls the influence of distance on choice of next node
        self.Q0 = q0                    #determines the state transition probability
        self.Rho = rho                  #to control how fast the deposited pheromone evaporates
        self.unvisited_nodes = {}       #to store unvisited nodes

        #store all the nodes as unvisited except the first 
        for i in range(0, self.graph.num_nodes):
            if i != self.start_node:
                self.unvisited_nodes[i] = i

        # a square path matrix of 0s and 1s (1 means a node is visited)
        self.path_mat = []

        # the matrix is initialized with all 0s
        for i in range(0, self.graph.num_nodes):
            self.path_mat.append([0] * self.graph.num_nodes)

    
    def run(self):
        """
        #the ants use this function to traverse the network
        #the colony and pheromone are updated in the journey
        """
        graph = self.colony.graph
        while not self.end():
            new_node = self.state_transition_rule(self.curr_node)       

            #update the forward cost based on selected node
            self.path_cost += graph.delta(self.curr_node, new_node)     

            #store the new node in the sequence of chosen nodes
            self.path_vec.append(new_node)                              

            #add a 1 to the path matrix to note that the node is visited
            self.path_mat[self.curr_node][new_node] = 1                 
            self.pheromone_updating_rule(self.curr_node, new_node)          

            #the new node becomes the current node
            self.curr_node = new_node                                   

        #update the backward cost from the selected node
        self.path_cost += graph.delta(self.path_vec[-1], self.path_vec[0])  

        #update the colony of the findings
        self.colony.update(self)                                          

        self.__init__(self.ID, self.start_node, self.colony, self.Q0, self.Rho, self.Beta)


    
    def end(self):
        """
        #checks if all the nodes have been visisted
        #if all nodes have been visted, this should be empty and true
        """
        return not self.unvisited_nodes


    def state_transition_rule(self, curr_node):
        """
        #the next node to visit is determined by this state transition rule
        """
        graph = self.colony.graph
        q = random.random()
        max_node = -1

        #so we use either Exploitation or Exploration method
        #depending on the state transition probability
        if q < self.Q0:
            print "Exploitation"
            max_val = -1
            val = None

            for node in self.unvisited_nodes.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")

                val = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)

                if val > max_val:
                    max_val = val
                    max_node = node
                    
        else:           
            print "Exploration"
            sum = 0
            node = -1

            for node in self.unvisited_nodes.values():
                if graph.tau(curr_node, node) == 0:
                    raise Exception("tau = 0")

                sum += graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)

            if sum == 0:
                raise Exception("sum = 0")

            avg = sum / len(self.unvisited_nodes)

            print "avg = %s" % (avg,)
            for node in self.unvisited_nodes.values():
                p = graph.tau(curr_node, node) * math.pow(graph.etha(curr_node, node), self.Beta)
                if p > avg:
                    print "p = %s" % (p,)
                    max_node = node
                    
            if max_node == -1:
                max_node = node
                
        if max_node < 0:
            raise Exception("max_node < 0")
        
        del self.unvisited_nodes[max_node]
        return max_node

    def pheromone_updating_rule(self, curr_node, next_node):    
        #Update the pheromones on the tau matrix to represent transitions of the ants
        graph = self.colony.graph
        val = (1 - self.Rho) * graph.tau(curr_node, next_node) + (self.Rho * graph.tau0)
        graph.update_tau(curr_node, next_node, val)

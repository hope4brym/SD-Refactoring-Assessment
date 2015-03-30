class TSPNetwork:
    """
    this is the network to be solved
    it's a square matrix o fthe cities and their distances/costs
    """


    def __init__(self, num_nodes, delta_mat, tau_mat=None):
        """
        #this is the constructor
        """
        print len(delta_mat)

        #the number of node distances must match the number of nodes
        if len(delta_mat) != num_nodes:
            raise Exception("len(delta) != num_nodes")

        self.num_nodes = num_nodes
        #stores the node distances
        self.delta_mat = delta_mat 

        #initialize all pheromone levels to 0
        if tau_mat is None:
            self.tau_mat = []
            for i in range(0, num_nodes):
                self.tau_mat.append([0] * num_nodes)


    def delta(self, r, s):
        """
        #returns costs between two nodes
        """
        return self.delta_mat[r][s]


    def tau(self, r, s):
        """
        #returns pheromone level of the edge between two nodes
        """
        return self.tau_mat[r][s]


    def etha(self, r, s):
        """
        #returns the inverse of delta
        """
        return 1.0 / self.delta(r, s)
    

    def update_tau(self, r, s, val):
        """
        #updates the phermone level on an edge
        """
        self.tau_mat[r][s] = val


    def reset_tau(self):
        """
        #resets tau
        """
        avg = self.average_delta()
        self.tau0 = 1.0 / (self.num_nodes * 0.5 * avg)
        print "Average = %s" % (avg,)
        print "Tau0 = %s" % (self.tau0)
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                self.tau_mat[r][s] = self.tau0


    def average_delta(self):
        """
        #returns the overall average edge distance
        """
        return self.average(self.delta_mat)


    def average_tau(self):
        """
        #returns the overall average tau
        """
        return self.average(self.tau_mat)


    def average(self, matrix):
        """
        #returns an overall average for the square matrix of either distances or tau
        """
        sum = 0
        for r in range(0, self.num_nodes):
            for s in range(0, self.num_nodes):
                sum += matrix[r][s]

        avg = sum / (self.num_nodes * self.num_nodes)
        return avg

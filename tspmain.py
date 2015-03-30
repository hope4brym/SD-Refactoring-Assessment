import pickle
import sys
import traceback


from tspnetwork import TSPNetwork
from tspcolony import TSPColony


def main(argv):
    """
    this is the starting point of the program
    """

   #this is not necessary 
   #number_of_nodes = 10     

    if len(argv) >= 3 and argv[0]:
        number_of_nodes = int(argv[0])   #picks number of nodes from file

    number_of_ants = int(argv[1])     
    iterations = int(argv[2])     
    repetitions = int(argv[3])
    alpha = float(argv[4])
    beta = float(argv[5])
    q0 = float(argv[6])
    rho = float(argv[7])

    #these hardcoded values have been parameterised
    """
    if number_of_nodes <= 10:
        number_of_ants = 20     
        iterations = 12     
        repetitions = 1      
    else:
        number_of_ants = 20
        iterations = 12
        repetitions = 1
    """

    stuff = pickle.load(open(argv[8], "r"))
    cities = stuff[0]
    distances = stuff[1]   

    #why are we doing this?
    """
    #if the number of nodes is less than the dimension of the distances matrix
    #then the program should only use the distances of dimension up to the number of nodes.
    #that means, the program assumes that the problem size is the number of nodes
    """
    if number_of_nodes < len(distances):
        distances = distances[0:number_of_nodes]
        for i in range(0, number_of_nodes):
            distances[i] = distances[i][0:number_of_nodes]



    try:
        graph = TSPNetwork(number_of_nodes, distances)
        bpv = None
        bpc = sys.maxint
        for i in range(0, repetitions):
            print "Repetition %s" % i
            graph.reset_tau()
            workers = TSPColony(graph, number_of_ants, iterations, alpha, q0, rho, beta)
            print "Colony Started"
            workers.start()
            if workers.minimum_cost < bpc:
                print "Colony Path"
                bpv = workers.best_path
                bpc = workers.minimum_cost

        print "\n------------------------------------------------------------"
        print "                     Results                                "
        print "------------------------------------------------------------"
        print "\nBest path = %s" % (bpv,)
        city_vec = []
        for node in bpv:
            print cities[node] + " ",
            city_vec.append(cities[node])

        print "\nBest path cost = %s\n" % (bpc,)
        results = [bpv, city_vec, bpc]
        pickle.dump(results, open(argv[9], 'w+'))

    except Exception, e:
        print "exception: " + str(e)
        traceback.print_exc()


if __name__ == "__main__":
    main(sys.argv[1:])

""""
This data derives from a study on the diffusion of micro-finance
in rural India. This was published in Science in "The Diffusion of
Micro-finance" article in 2013, by Banerjee et al.

Adjacency matrix returns 1 in position ij if nodes i and j are connected
and 0 if ij are not connected. The network is undirected, so ij = ji

This code reads in the adjacency matrix for the data of social networks for two different villages in rural India, then provides basic information about the networks, including numbers of nodes, edges, and average degree of nodes. It also produces a figure of each network.
""""
import numpy as np
import networkx as nx

A1 = np.loadtxt("adj_allVillageRelationships_vilno_1.csv", delimiter = ",")
A2 = np.loadtxt("adj_allVillageRelationships_vilno_2.csv", delimiter = ",")

def basic_net_stats(G):
    print("Number of nodes: %d" % G.number_of_nodes())
    print("Number of edges: %d" % G.number_of_edges())
    degree_sequence = [d for n, d in G.degree()]
    print("Average degree: %.2f" % np.mean(degree_sequence))

""""
Return the number of edges, nodes, and average degree for the two networks:
""""

basic_net_stats(G1)
basic_net_stats(G2)

"""" Plot a histogram of the degree distribution""""

plot_degree_distribution(G1)
plot_degree_distribution(G2)


"""" Draw figures of the networks""""

plt.figure()
nx.draw(G1_LCC, node_color = "red", edge_color = "gray", node_size = 20)
plt.savefige("village1.pdf")

plt.figure()
nx.draw(G2_LCC, node_color = "green", edge_color = "gray", node_size = 20)
plt.savefige("village2.pdf")

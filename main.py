from utils import *


def read_data():
    g = nx.read_gml('real/karate/karate.gml', label='id')
    dict = {}
    i = 0
    for node in g.nodes:
        dict[node] = i
        i += 1
    mat = [[0 for _ in range(len(dict))] for _ in range(len(dict))]

    for pair in g.edges:
        mat[dict[pair[0]]][dict[pair[1]]] = 1
        mat[dict[pair[1]]][dict[pair[0]]] = 1

    degree = []
    for el in g.degree:
        degree.append(el[1])

    net = {'noNodes': len(g.nodes), 'mat': mat, 'noEdges': len(g.edges), 'degrees': degree}
    return net


def modularity(communities, param):
    noNodes = param['noNodes']
    mat = param['mat']
    degrees = param['degrees']
    noEdges = param['noEdges']
    M = 2 * noEdges
    Q = 0.0
    for i in range(0, noNodes):
        for j in range(0, noNodes):
            if communities[i] == communities[j]:
                Q += (mat[i][j] - degrees[i] * degrees[j] / M)
    return Q * 1 / M


def communitiesNmb(bestChr):
    nrCom = []
    for gene in bestChr.repres:
        if gene not in nrCom:
            nrCom.append(gene)
    return len(nrCom)


def community_app(bestChr):
    for i in range(0, len(bestChr.repres)):
        print(i, " : ", bestChr.repres[i])


def solution(ga, problemParams, bestChrFitness, nrCom):
    for i in range(problemParams['numberOfIterations']):
        ga.oneGenerationElitism()
        bestChr = ga.bestChromosome()
        bestChrFitness.append(bestChr.fitness)
        nrCom.append(communitiesNmb(bestChr))


def show_solution(bestChr, bestChrFitness, nr_com):
    print("Number of communities: ", communitiesNmb(bestChr))
    print('Node appartenance to each community: ')
    community_app(bestChr)
    print('Best chromosome fitness evolution throughout generations: ')
    for x in bestChrFitness:
        print(x)
    print('Number of communities throughout generations: ')
    for x in nr_com:
        print(x)


def main():
    problemParams = read_data()
    problemParams['numberOfChromosomes'] = 100
    problemParams['numberOfIterations'] = 1000
    problemParams['function'] = modularity;

    bestChrFitness = []
    nr_com = []
    ga = GA(problemParams)

    # show_graph(problemParams)

    solution(ga, problemParams, bestChrFitness, nr_com)

    bestChr = ga.bestChromosome()

    show_solution(bestChr, bestChrFitness, nr_com)

    # show_communities(problemParams, bestChr)


if __name__ == '__main__':
    main()

import argparse
import sys
from AdaptivePELE.atomset import atomset, SymmetryContactMapEvaluator
from AdaptivePELE.utilities import utilities
import numpy as np
import networkx as nx
import itertools


def parseArguments():
    desc = "Create a network of residues that share contacts with the same ligand atom over a trajectory, either as pdb files or from a clustering\n"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("resname", type=str, help="Ligand resname in pdb")
    parser.add_argument("contactThreshold", type=int, help="Contact threshold to calculate contactMap")
    parser.add_argument("-trajectory", type=str, nargs='+', help="Path to the trajectory or pdbs to analyse")
    parser.add_argument("-clustering", help="Path to the clustering object to analyse")
    parser.add_argument("-nRes", type=int, default=10, help="Number of top residues to display")
    args = parser.parse_args()
    return args.trajectory, args.clustering, args.nRes, args.resname, args.contactThreshold


def generateConformations(resname, clAcc, trajectory):
    if clAcc is None:
        for traj in trajectory:
            snapshots = utilities.getSnapshots(traj)
            for snapshot in snapshots:
                PDBobj = atomset.PDB()
                PDBobj.initialise(snapshot, resname)
                yield PDBobj
    else:
        for cluster in clAcc.clusters.clusters:
            yield cluster.pdb


if __name__ == "__main__":
    trajectory, clustering, nRes, resname, contactThreshold = parseArguments()

    if clustering is None:
        clAcc = None
    else:
        clAcc = utilities.readClusteringObject(clustering)

    symEval = SymmetryContactMapEvaluator.SymmetryContactMapEvaluator()
    refPDB = None
    network = nx.Graph()
    sys.stderr.write("Creating network...\n")

    for pdb in generateConformations(resname, clAcc, trajectory):
        contactMap, foo = symEval.createContactMap(pdb, resname, contactThreshold)
        if refPDB is None:
            refPDB = pdb
            proteinList = symEval.proteinList
        for row in contactMap:
            nodes = np.where(row)[0]
            for pair in itertools.combinations(nodes, 2):
                atom1 = refPDB.atoms[proteinList[pair[0]]]
                atom2 = refPDB.atoms[proteinList[pair[1]]]
                res1, res2 = int(atom1.resnum), int(atom2.resnum)
                if abs(res1-res2) > 5:
                    if network.has_edge(res1, res2):
                        network[res1][res2]['weight'] += 1
                    else:
                        network.add_edge(res1, res2, weight=1)

    numAtoms = min(nRes, network.order())
    deg = network.degree()
    print "Residue\tDegree"
    for node in sorted(network.nodes(), key=lambda x: deg[x], reverse=True)[:nRes]:
        print "%d\t%d" % (node, deg[node])
    nx.write_weighted_edgelist(network, "newtorkCM.edgelist")
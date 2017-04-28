import os
import sys
import argparse
from AdaptivePELE.utilities import utilities
import matplotlib.pyplot as plt


def parseArguments():
    desc = "Write the information related to the conformation network to file\n"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("clusteringObject", type=str, help="Path to the clustering object")
    parser.add_argument("suffix", type=str, help="Suffix to append to file names")
    parser.add_argument("metricCol", type=int, help="Column of the metric of interest")
    parser.add_argument("-o", type=str, default=None, help="Output path where to write the files")
    args = parser.parse_args()
    return args.clusteringObject, args.suffix, args.metricCol, args.o


if __name__ == "__main__":
    clusteringObject, suffix, metricCol, outputPath = parseArguments()
    if outputPath is not None:
        outputPath = os.path.join(outputPath, "")
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
    else:
        outputPath = ""
    sys.stderr.write("Reading clustering object...\n")
    cl = utilities.readClusteringObject(clusteringObject)
    optimalCluster = cl.getOptimalMetric(4)
    pathway = cl.createPathwayToCluster(optimalCluster)
    metInd = cl.calculateMetastabilityIndex()
    if not os.path.exists(outputPath+"conformationNetwork%s.edgelist" % suffix):
        sys.stderr.write("Writing conformation network...\n")
        cl.writeConformationNetwork(outputPath+"conformationNetwork%s.edgelist" % suffix)
    if not os.path.exists(outputPath+"FDT%s.edgelist" % suffix):
        sys.stderr.write("Writing FDT...\n")
        cl.writeFDT(outputPath+"FDT%s.edgelist" % suffix)
    if not os.path.exists(outputPath+"pathwayFDT%s.pdb" % suffix):
        sys.stderr.write("Writing pathway to optimal cluster...\n")
        # cl.writePathwayOptimalCluster(outputPath+"pathwayFDT%s.pdb" % suffix)
        cl.writePathwayTrajectory(pathway, outputPath+"pathwayFDT%s.pdb" % suffix)
    if not os.path.exists(outputPath+"nodesPopulation%s.txt" % suffix):
        sys.stderr.write("Writing nodes population...\n")
        cl.writeConformationNodePopulation(outputPath+"nodesPopulation%s.txt" % suffix)
    if not os.path.exists(outputPath+"nodesMetric%s.txt" % suffix):
        sys.stderr.write("Writing nodes metrics...\n")
        cl.writeConformationNodeMetric(outputPath+"nodesMetric%s.txt" % suffix, metricCol)
    if not os.path.exists(outputPath+"nodesMetIndex%s.txt" % suffix):
        sys.stderr.write("Writing metastability indeces...\n")
        cl.writeMetastabilityIndex(outputPath+"nodesMetIndex%s.txt" % suffix)
    plt.figure()
    plt.plot(pathway, [cl.clusters.clusters[i].getMetricFromColumn(5) for i in pathway])
    plt.xlabel("Cluster number")
    plt.ylabel("Binding energy(kcal/mol)")
    plt.savefig(outputPath+"bindingEnergy_%s.png" % suffix)
    plt.figure()
    plt.plot(pathway, [cl.clusters.clusters[i].contacts for i in pathway])
    plt.xlabel("Cluster number")
    plt.ylabel("Contacts ratio")
    plt.savefig(outputPath+"contacts_%s.png" % suffix)
    plt.figure()
    plt.plot(pathway, [cl.clusters.clusters[i].getMetricFromColumn(3) for i in pathway])
    plt.xlabel("Cluster number")
    plt.ylabel("Energy(kcal/mol)")
    plt.savefig(outputPath+"totalEnergy_%s.png" % suffix)
    plt.figure()
    plt.plot(pathway, [metInd[i] for i in pathway])
    plt.xlabel("Cluster number")
    plt.ylabel("Metastability index")
    plt.savefig(outputPath+"metIndex_%s.png" % suffix)
    plt.show()
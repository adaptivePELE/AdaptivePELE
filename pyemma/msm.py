import pyemma.msm as msm
import pyemma.plots as mplt

def calculateITS(trajectories, lagtimes, errors = None):
    """ Calulate the implied time-scales at the given lagtimes"""
    its_object = msm.its(trajectories, lags=lagtimes, errors=errors)
    return its_object

def plotITS(its_object, its_plot_file=None, nits=-1):
    its_plot = mplt.plot_implied_timescales(its_object, outfile=its_plot_file, nits=nits)
    return its_plot

def estimateMSM(trajectories,lagtime):
    """ Estimate a MSM from the trajectories using a provided lagtime that
    should be big enough so that the relevant processes have converged.
    Return a MaximumLikelihoodMSM object"""
    MSM_object = msm.estimate_markov_model(trajectories, lagtime)
    return MSM_object

def calculatePCCA(MSM_object, numPCCA):
    """ Coarse-cluster the MSM usin numPCCA clusters. 
    Return a PCCA object"""
    MSM_object.pcca(numPCCA)
    return MSM_object

def is_connected(MSM_object):
    """ Check if the MSM created is connected"""
    return msm.analysis.is_connected(MSM_object.transition_matrix)

def ChapmanKolmogorovTest(MSM_object, nsets,memberships=None, error_estimation=False):
    """ Perform the ChapmanKolmogorov test to validate the MSM"""
    return MSM_object.cktest(nsets,memberships=memberships,err_est=error_estimation)

def plotChapmanKolmogorovTest(CKObject, layout=None, padding_between=0.1,
                              padding_top=0.075):
    """ Plot the results of the Chapman-Kolgomorov tests"""
    mplt.plot_cktest(CKObject,layout=layout, padding_between=padding_between,
                     padding_top=padding_top)
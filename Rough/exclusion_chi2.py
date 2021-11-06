import numpy as np
from scipy import stats
from matplotlib import pyplot as plt

def modelResult(x):
    mu = 5e1
    sig = 1e1
    #artificial model I created 
    return 1e14*np.exp(-(x-mu)**2/sig**2*0.5)

def chiSquare(model,data,axis=-1):
    return np.sum((model-data)**2/data**2,axis=axis) #we always sum over the data points so I need to specify which axis this corresponds to

def chiSqToProb(chiSq,df):
    return stats.chi2.sf(chiSq,df)


y0 = 1e-10
alpha = -1.5
CL = 0.05

x = np.logspace(1,2,num=20)
data = y0*x**alpha #simple power-law as artificial data

sigV = np.logspace(-2,5,num=1000)*1e-26 #trial values of sigV 
model = np.tensordot(modelResult(x),sigV,axes=0) #here I build an array where each element is a value of model*sigV (every combination will be considered)
data = np.tensordot(data,np.ones_like(sigV),axes=0) #I am generating N identical copies of the data, one for each trial sigV value

plt.yscale("log");plt.xscale("log")
plt.plot(x,data)
plt.plot(x,modelResult(x)*sigV[-1])
plt.plot(x,modelResult(x)*sigV[0])
plt.show()

chi2 = chiSquare(model,data,axis=0) #note I specify the data axis which is the first due to the order of the tensordot in the model line
chiDiff = chi2 - min(chi2) #I want to find out how far each sigV value is from the best-fit value
pVals = chiSqToProb(chiDiff,1) #convert from chi^2 to probability of explaining the data with sigV*model

"""
Now is the tricky bit:
I need to find the parts of the chi^2 distribution that integrate to less than 0.05
The p value corresponds to the area under the distribution chi(x) where x < - x0/2  or x > x0/2 (imagine the tails of a normal distribution as analogy)
The easiest way to find our need parts is to do the following:
Ask the opposite question -> which sigV's have p > 0.5*0.05, this we can do via sigV[pVals>0.5*CL]
Since larger sigV indicates larger model*sigV, we can conclude that any sigV > max(sigV[pVals>0.5*CL]) has a p value outside the 0.05 contour
"""
upperLim = max(sigV[pVals>0.5*CL]) 
print("The cross-section {} cm^3 s^-1 was excluded at 95% probability".format(upperLim))

"""
Here I plot the value*model to confirm it narrowly exceeds data*2, which is a rough idea of what a 95% exclusion corresponds to
"""
plt.yscale("log");plt.xscale("log")
plt.plot(x,2*data)
plt.plot(x,modelResult(x)*upperLim)
plt.show()



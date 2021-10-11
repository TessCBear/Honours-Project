import classes
import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
from astropy.io import fits

def chiSquare(model,data,axis=-1):
    return np.sum((model-data)**2/data**2,axis=axis)

def chiSqToProb(chiSq,df):
    return stats.chi2.sf(chiSq,df)

# just 75 GeV for now

coma_data = {
    "M_vir": 1.24e15, #solar mass 
    "R_vir": 3, # Mpc
    "D_L" : 99, # Mpc 
    "density_type" : "NFW",
    "c_vir" : 9.0
    }

coma = classes.Astrophysical(coma_data)
coma.mass = 75
coma.data = np.loadtxt("madala_22_spin0_AtProduction_gammas.dat")

data_m = coma.data[np.where(coma.data[:,0]==coma.mass)]
E_list = []
for item in data_m:
    E = item[1]
    E_list.append(E)

flux_GeV = []
for energy in E_list:
    if energy >= 0.2 and energy < 1:
        fluxes = [1.98, 2.28, 2.36, 2.38, 2.73, 2.18]
    elif energy >= 1 and energy < 10:
        fluxes = [0.77, 0.76, 0.82, 0.82, 0.74, 1.11]
    elif energy >=10 and energy < 100:
        fluxes = [2.01, 3.03, 3.08, 4.97, 4.88, 2.92]
    else:
        fluxes = 0
    flux = np.average(fluxes)
    flux *= 6.2415e-10 #conversion from 1e-12 erg to GeV and x by scaling factor of sigma
    flux_GeV.append(flux)



sigV = np.logspace(-2,5,num=1000)  
model = np.tensordot(coma.SE(E_list),sigV,axes=0) 
data = np.tensordot(flux_GeV,np.ones_like(sigV),axes=0) 

plt.yscale("log");plt.xscale("log")
plt.plot(E_list,data)
plt.plot(E_list,coma.SE(E_list)*sigV[-1])
plt.plot(E_list,coma.SE(E_list)*sigV[0])
plt.show()

chi2 = chiSquare(model,data,axis=0) #note I specify the data axis which is the first due to the order of the tensordot in the model line
chiDiff = chi2 - min(chi2) #I want to find out how far each sigV value is from the best-fit value
pVals = chiSqToProb(chiDiff,1) #convert from chi^2 to probability of explaining the data with sigV*model

CL = 0.05

upperLim = max(sigV[pVals>0.5*CL]) 
print("The cross-section {} cm^3 s^-1 was excluded at 95% probability".format(upperLim))


plt.yscale("log");plt.xscale("log")
plt.plot(E_list,2*data)
plt.plot(E_list,coma.SE(E_list)*upperLim)
plt.show()
import numpy as np
import scipy.integrate
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.constants as const
from scipy import stats
from astropy.io import fits

class Astrophysical:
    def __init__(self, galaxy):
        self.M_vir = galaxy["M_vir"]
        self.R_vir = galaxy["R_vir"]
        self.c_vir = galaxy["c_vir"]
        self.r_s = self.R_vir/self.c_vir
        self.density_type = galaxy["density_type"]
        self.D_L = galaxy["D_L"]
        self.name = galaxy["name"]
    
        self.mass = 0
        self.data = []

    def NFW_profile(self, r):
            
            def nfw(x):
                return 1.0/x/(1+x)**2

            z = 0.0231
            
            nfwInt = scipy.integrate.quad(lambda x: x**2*nfw(x),0,self.c_vir)[0]*4*np.pi*self.r_s**3 
            rhos = self.M_vir/nfwInt
        
            
            return rhos*nfw(r/self.r_s)
                

    def J_spherical(self, D, theta):
        if self.density_type == 'NFW':
            density = self.NFW_profile
        else:
            print("No density profile as given")
        return scipy.integrate.quad(lambda r: (1/D**2) *density**2 * r**2, 0, D*theta)
    solar_to_GeV = (((1*u.M_sun).to('kg')*const.c**2).to('GeV')).to_value()
    Mpc_to_cm = ((1*u.Mpc).to('cm')).to_value()

    def J_cylindrical(self, D, theta):
                
                
                if self.density_type == 'NFW':
                    density = self.NFW_profile
                else:
                    print("No density profile as given")
                
                if self.name == 'virgo':
                    func = lambda R, z: ((2 * np.pi) / D**2 + R**2 + z**2) * R * density(np.sqrt(R**2 + z**2))**2
                    theta = 3* np.pi/180

                else:
                    func = lambda R, z: ((2 * np.pi) / D**2) * R * density(np.sqrt(R**2 + z**2))**2
                
                a = np.NINF
                b = np.inf
                gfun = lambda R: 0
                hfun = lambda R: D*theta
                return scipy.integrate.dblquad(func, a, b, gfun, hfun)[0]*self.solar_to_GeV**2 *self.Mpc_to_cm**-5
               
    def SE(self, E_list):
        mass = self.mass
        data = self.data

        sigma = 2.2e-26 

        data_m = data[data["#mdm(GeV)"]==mass]

        phi_list = []

        for index, row in data_m.iterrows():
            #phi = 1/2 * item[2]* 1/(item[0]**2) * sigma/(4*np.pi) 
            phi = 1/2 * row["dN/dE(GeV^-1)"] * 1/(row["#mdm(GeV)"]**2) * sigma/(4*np.pi)
            phi_list.append(phi)

        def S(phi, J):
            return phi*J

        S_list = []
        for phi in phi_list:
            S_point = S(phi, self.J_cylindrical(self.D_L, 0.5*np.pi/180))
            S_list.append(S_point)

        
        return np.multiply(E_list, S_list)

    def plot(self):
        mass = self.mass
        data = self.data

        #data_m = data[np.where(data[:,0]==mass)]
        data_m = data[data["#mdm(GeV)"]==mass]
        freq_list = []
        E_list = []
    
            
        for index, row in data_m.iterrows():
            E = row["E(GeV"]
            freq = (E/4.135667696e-24)*10**-6 # Planck's constant in GeV/Hz, so that freq is in Hz, then converted to MHz
            freq_list.append(freq)
            E_list.append(E)

        SE_list = self.SE(E_list)

        plotting_data = pd.DataFrame()
        plotting_data['freq'] = freq_list
        plotting_data['SE'] = SE_list

        sb.lineplot(data=plotting_data, x='freq', y= 'SE')
        plt.yscale("log")
        plt.xscale("log")

        plt.rcParams['text.usetex'] = True
        plt.ylabel(r"$S(\nu) E(\nu)$ (GeV cm$^{-2}$ s$^{-1}$)")
        plt.xlabel(r"$\nu$ (MHz)")
        plt.show()

    def chi_square_lim(self):
        
        def chiSquare(model,data,axis=-1):
            return np.sum((model-data)**2/data**2,axis=axis)

        def chiSqToProb(chiSq,df):
            return stats.chi2.sf(chiSq,df)
        
        #data_m = self.data[np.where(self.data[:,0]==self.mass)]
        data_m = self.data[self.data["#mdm(GeV)"]==self.mass]

        E_list = []
        for index, row in data_m.iterrows():
            E = row["E(GeV)"]
            E_list.append(E)

        flux_GeV = []
        if self.name == "coma":
            for energy in E_list:
                if energy >= 0.2 and energy < 1:
                    fluxes = [1.98, 2.28, 2.36, 2.38, 2.73, 2.18]
                elif energy >= 1 and energy < 10:
                    fluxes = [0.77, 0.76, 0.82, 0.82, 0.74, 1.11]
                elif energy >=10 and energy < 100:
                    fluxes = [2.01, 3.03, 3.08, 4.97, 4.88, 2.92]
                else:
                    pass
        elif self.name == "virgo":
            for energy in E_list:
                if energy >= 0.2 and energy < 1:
                    fluxes = [4.97, 4.93, 5.26, 5.62, 5.62, 5.71, 5.62, 5.24]
                elif energy >= 1 and energy < 10:
                    fluxes = [4.13, 4.65, 4.72, 4.72, 4.59, 4.72, 4.33, 3.89]
                elif energy >=10 and energy < 100:
                    fluxes = [4.35, 5.13, 4.48, 4.48, 4.35, 4.48, 5.26, 2.67]
                else:
                    pass
        else:
            print("No data for this galaxy")

        flux = np.average(fluxes)
        flux *= 6.2415e-10 #conversion from 1e-12 erg to GeV
        flux_GeV.append(flux)

        sigV = np.logspace(-2,10,num=1000)  
        model = np.tensordot(self.SE(E_list),sigV,axes=0) 
        data = np.tensordot(flux_GeV,np.ones_like(sigV),axes=0) 
        
        chi2 = chiSquare(model,data,axis=0)         
        chiDiff = chi2 - min(chi2) 
        pVals = chiSqToProb(chiDiff,1) 
        CL = 0.05

        upperLim = max(sigV[pVals>0.5*CL]) 
        return upperLim

import numpy as np
import scipy.integrate
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.constants as const

class Astrophysical:
    def __init__(self, galaxy):
        self.M_vir = galaxy["M_vir"]
        self.R_vir = galaxy["R_vir"]
        self.c_vir = galaxy["c_vir"]
        self.r_s = self.R_vir/self.c_vir
        self.density_type = galaxy["density_type"]
        self.D_L = galaxy["D_L"]
    
        self.mass = 0
        self.data = []

    def NFW_profile(self, r):
            
            def nfw(x):
                return 1.0/x/(1+x)**2

            z = 0.0231
            
            nfwInt = scipy.integrate.quad(lambda x: x**2*nfw(x),0,self.c_vir)[0]*4*np.pi*self.r_s**3 
            rhos = self.M_vir/nfwInt
        
            
            return rhos*nfw(r/self.r_s)
                

    # def J_spherical(self, D, theta):
    #     if self.density_type == 'NFW':
    #         density = NFW_profile
    #     else:
    #         density = lambda r: 1
    #     return scipy.integrate.quad(lambda r: (1/D**2) *density**2 * r**2, 0, D*theta)
    solar_to_GeV = (((1*u.M_sun).to('kg')*const.c**2).to('GeV')).to_value()
    Mpc_to_cm = ((1*u.Mpc).to('cm')).to_value()

    def J_cylindrical(self, D, theta):
                
                
                if self.density_type == 'NFW':
                    density = self.NFW_profile
                else:
                    density = lambda r: 1
                
                func = lambda R, z: ((2 * np.pi) / D**2) * R * density(np.sqrt(R**2 + z**2))**2
                a = np.NINF
                b = np.inf
                gfun = lambda R: 0
                hfun = lambda R: D*theta
                return scipy.integrate.dblquad(func, a, b, gfun, hfun)[0]*self.solar_to_GeV**2 *self.Mpc_to_cm**-5
                #return J *(self.solar_to_kg)**2 *(1/3.086e22*(10**2)**5) #* (1/5.39e-44)**4 #unit conversion to cm^-1 kg^2
               
    def SE(self, E_list):
        mass = self.mass
        data = self.data

        sigma = 2.2e-26 

        data_m = data[np.where(data[:,0]==mass)]

        phi_list = []

        for item in data_m:
            phi = 1/2 * item[2]* 1/(item[0]**2) * sigma/(4*np.pi) 
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

        data_m = data[np.where(data[:,0]==mass)]
        freq_list = []
        E_list = []
    
            
        for item in data_m:
            E = item[1]
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

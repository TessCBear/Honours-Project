import numpy as np
import scipy.integrate
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.constants as const
from scipy import stats
from astropy.io import fits


galaxy = {
    "M_vir": 6.3e14, #solar mass
    "R_vir": 1.7, # Mpc
    "D_L": 16.5, # Mpc
    "density_type": "NFW",
    "c_vir": 1.7/1.24,
    "name" : "virgo" 
}

M_vir = galaxy["M_vir"]
R_vir = galaxy["R_vir"]
c_vir = galaxy["c_vir"]
r_s = R_vir/c_vir
density_type = galaxy["density_type"]
D_L = galaxy["D_L"]
name = galaxy["name"]



def NFW_profile(r):
        
        def nfw(x):
            return 1.0/x/(1+x)**2

        z = 0.0231
        
        nfwInt = scipy.integrate.quad(lambda x: x**2*nfw(x),0,c_vir)[0]*4*np.pi*r_s**3 
        rhos = M_vir/nfwInt
    
        
        return rhos*nfw(r/r_s)
            

# def J_spherical( D, theta):
#     if density_type == 'NFW':
#         density = NFW_profile
#     else:
#         print("No density profile as given")
#     return scipy.integrate.quad(lambda r: (1/D**2) *density**2 * r**2, 0, D*theta)
solar_to_GeV = (((1*u.M_sun).to('kg')*const.c**2).to('GeV')).to_value()
Mpc_to_cm = ((1*u.Mpc).to('cm')).to_value()

def J_cylindrical(D, theta):
            
            
            if density_type == 'NFW':
                density = NFW_profile
            else:
                print("No density profile as given")
            
            if name == 'virgo':
                func = lambda R, z: ((2 * np.pi) / D**2 + R**2 + z**2) * R * density(np.sqrt(R**2 + z**2))**2
                theta = 3* np.pi/180

            else:
                func = lambda R, z: ((2 * np.pi) / D**2) * R * density(np.sqrt(R**2 + z**2))**2
            
            a = np.NINF
            b = np.inf
            gfun = lambda R: 0
            hfun = lambda R: D*theta
            return scipy.integrate.dblquad(func, a, b, gfun, hfun)[0]*solar_to_GeV**2 *Mpc_to_cm**-5
            
def SE(E_list, mass, data):
    

    #sigma = 2.2e-26 
    sigma = 1e-25

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
        S_point = S(phi, J_cylindrical(D_L, 0.5*np.pi/180))
        S_list.append(S_point)

    
    return np.multiply(E_list, S_list)

def plot_data(mass, data):
    
    #data_m = data[np.where(data[:,0]==mass)]
    data_m = data[data["#mdm(GeV)"]==mass]
    freq_list = []
    E_list = []

        
    for index, row in data_m.iterrows():
        E = row["E(GeV)"]
        freq = (E/4.135667696e-24)*10**-6 # Planck's constant in GeV/Hz, so that freq is in Hz, then converted to MHz
        freq_list.append(freq)
        E_list.append(E)

    SE_list = SE(E_list, mass, data)

    plotting_data = pd.DataFrame()
    plotting_data['freq'] = freq_list
    plotting_data['SE'] = SE_list

    return plotting_data

data = pd.read_csv("madala_23_spin0_AtProduction_gammas.dat", sep=' ')
m75 = plot_data(200, data)
m200 = plot_data(400, data)

sb.lineplot(data=m75, x='freq', y= 'SE', label = f"Mass of 200 GeV")
sb.lineplot(data=m200, x='freq', y= 'SE', label = f"Mass of 400 GeV")
plt.title("Virgo")
plt.yscale("log")
plt.xscale("log")

plt.rcParams['text.usetex'] = True
plt.ylabel(r"$S(\nu) E(\nu)$ (GeV cm$^{-2}$ s$^{-1}$)")
plt.xlabel(r"$\nu$ (MHz)")
plt.show()



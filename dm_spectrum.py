import numpy as np
from astrophysical_class import Astrophysical
import matplotlib.pyplot as plt
import pandas as pd

coma_data = {
    "M_vir": 1.24e15, #solar mass 
    "R_vir": 3, # Mpc
    "D_L" : 99, # Mpc 
    "density_type" : "NFW",
    "c_vir" : 9.0, # virial concentration (rvir/rs)
    "name": "coma"
    }

virgo_data = {
    "M_vir": 6.3e14, #solar mass
    "R_vir": 1.7, # Mpc
    "D_L": 16.5, # Mpc
    "density_type": "NFW",
    "c_vir": 1.7/1.24,
    "name" : "virgo" 
}


coma = Astrophysical(coma_data)
virgo = Astrophysical(virgo_data)


spectral_type = ["22", "23"]
clusters = [coma, virgo]

for cluster in clusters:
    for type in spectral_type:
        if type == "22":
            dm_masses = [75, 200]
        elif type == "23":
            dm_masses = [200, 400]
        data = pd.read_csv("madala_{}_spin0_AtProduction_gammas.dat".format(type), sep=' ')
        cluster.data = data
    
        for mass in dm_masses:
            cluster.mass = mass
            cluster.plot()
            plt.legend()
        plt.show()
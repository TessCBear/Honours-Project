from astrophysical_class import Astrophysical
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

data = pd.read_csv("madala_22_spin0_AtProduction_gammas.dat", sep=' ')
#data = np.loadtxt("madala_22_spin0_AtProduction_gammas.dat")


coma_data = {
    "M_vir": 1.24e15, #solar mass 
    "R_vir": 3, # Mpc
    "D_L" : 99, # Mpc 
    "density_type" : "NFW",
    "c_vir" : 9.0
    }



coma = Astrophysical(coma_data)
coma.mass = 75
coma.data = data


masses = [75, ]

chis = []
for index, row in data.iterrows():
    if row['#mdm(GeV)'] == coma.mass:
        pass
    else: 
        coma.mass = row["#mdm(GeV)"]
        masses.append(coma.mass)

print(masses)

for mass in masses:
    coma.mass = mass
    chi = coma.chi_square_lim()
    chis.append(chi)
    print(chi)

print(chis)

# #-----Results from dat22-------#
# masses22 = [75, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]
# chis22 = [6438.857427240413, 12276.910479883603, 39865.810735804385, 85100.07247122246, 100000.0, 100000.0, 100000.0, 100000.0, 100000.0, 100000.0, 100000.0]

# #----Results from dat23------#
# masses23 = [200, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]
# chis23 = [18675.45842761074, 37982.15306190736, 62632.07452198692, 93750.1501514529, 100000.0, 100000.0, 100000.0, 100000.0, 100000.0]

# chis_scaled = []
# for chi in chis22:
#     chi*= 1e-26
#     chis_scaled.append(chi)

# for chi in chis23:
#     chi*= 1e-26
#     chis_scaled.append(chi)

# masses = masses22+masses23

# sb.lineplot(x=masses, y=chis_scaled)
# plt.yscale("log")
# plt.xscale("log")
# plt.rcParams['text.usetex'] = True
# plt.ylabel(r"SE (GeV cm$^{-2}$ s$^{-1}$)")
# plt.xlabel(r"Mass (GeV)")
# plt.show()

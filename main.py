from astrophysical_class import Astrophysical
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib as plt

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
chis = coma.chi_square_lim()

masses = [75, ]

chis = []
for index, row in data.iterrows():
    if row['#mdm(GeV)'] == coma.mass:
        pass
    else: 
        coma.mass = row["#mdm(GeV)"]
        masses.append(coma.mass)

    chi = coma.chi_square_lim()
    chis.append(chi)
    print(chi)

print(chis)

sb.lineplot(x=masses, y=chis)
plt.ylabel("Upperlim")
plt.xlabel("Mass (GeV)")
plt.show()

import classes
import numpy as np

data = np.loadtxt("madala_22_spin0_AtProduction_gammas.dat")


coma_data = {
    "M_vir": 1.24e15, #solar mass 
    "R_vir": 3, # Mpc
    "D_L" : 99, # Mpc 
    "density_type" : "NFW",
    "c_vir" : 9.0
    }



coma = classes.Astrophysical(coma_data)
coma.mass = 75
coma.data = data
coma.plot() 


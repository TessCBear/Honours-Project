from astrophysical_class import Astrophysical
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

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


spec_type = [ "22", "23"]
for type in spec_type:
    data = pd.read_csv(".\model_data\madala_{}_spin0_AtProduction_gammas.dat".format(type), sep=' ')

    first_row = data.iloc[0]
    mass = first_row["#mdm(GeV)"]

    coma = Astrophysical(coma_data)
    virgo = Astrophysical(virgo_data)

    clusters = [coma, virgo ]
    for cluster in clusters:
        print(cluster.name)
        cluster.mass = mass
        cluster.data = data
        
        J = cluster.J_cylindrical(D = cluster.D_L, theta = 0.5)
        print(f"The J-factor for {cluster.name} = {J} GeV^2 cm^-5")

        masses = [mass, ]
    
        chis = []
        for index, row in data.iterrows():
            if row['#mdm(GeV)'] == cluster.mass:
                pass
            else: 
                cluster.mass = row["#mdm(GeV)"]
                masses.append(cluster.mass)
        
        print(masses)
        

        for mass in masses:
            cluster.mass = mass
            chi = cluster.chi_square_lim()
            chis.append(chi)
            print(chi)
        
        
        chis_scaled = []
        chis_nosubs = []
        #chis22_scaled = []
        for chi in chis:
            chi_nosubs = chi*1e-26
            chi*= 1e-26 *1/35
            chis_scaled.append(chi)
            chis_nosubs.append(chi_nosubs)
            # chis22_scaled.append(chi)
        


        plt.plot(masses, chis_scaled, label = r"$\chi^2$ exclusion boosted")
        plt.plot(masses, chis_nosubs, label = r"$\chi^2$ exclusion")
        #plt.plot(masses23, chis23_scaled)
        #sb.lineplot(x=masses, y=chis_scaled)
        plt.yscale("log")
        plt.xscale("log")
        plt.ylabel(r"$\langle \sigma_V \rangle$ (cm$^3$ s$^{-1}$")
        plt.xlabel(r"Mass (GeV)")


        def fill(file, label_name):
            posData = np.loadtxt(file)
            plt.fill_between(posData[0],posData[1]*1e-26,posData[2]*1e-26,alpha=0.4,label=label_name)
            
            


        fill(".\parameter_space\\ams2_positrons_{}_bestfit_3sigma_{}_{}_addBaKG.data".format("med","nfw",type), r"$e^{+}$ $3 \sigma$")
        fill(".\parameter_space\\ams2_antiproton_{}_{}_{}_uncorrelated_bestfit_3sigma.data".format(type, "nfw", "med"), r"$\bar{p}$ $3 \sigma$")
        fill(".\parameter_space\\fermi_gc10_{}_{}_bestfit_3sigma.data".format("nfw", type), r"Fermi gc10 $3 \sigma$")
        plt.legend(loc = "upper left")
        plt.title(r"{}: Spectral type {} $\chi^2$ exclusion at 95% CL".format(cluster.name, type))
        plt.show()





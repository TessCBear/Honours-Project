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


spec_type = ["22", "23"]
for type in spec_type:
    data = pd.read_csv("madala_{}_spin0_AtProduction_gammas.dat".format(type), sep=' ')

    first_row = data.iloc[0]
    mass = first_row["#mdm(GeV)"]

    coma = Astrophysical(coma_data)
    # coma.mass = mass
    # coma.data = data

    virgo = Astrophysical(virgo_data)
    # virgo.mass = mass
    # virgo.data = data

    clusters = [virgo, ]
    for cluster in clusters:
        print(cluster.name)
        cluster.mass = mass
        cluster.data = data
        
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
        #chis22_scaled = []
        for chi in chis:
            chi*= 1e-26 *1/35
            chis_scaled.append(chi)
            # chis22_scaled.append(chi)
        # chis23_scaled = []
        # for chi in chis23:
        #     chi*= 1e-26 *1/35
        #     chis_scaled.append(chi)
        #     chis23_scaled.append(chi)


        plt.plot(masses, chis_scaled, label = r"$\chi^2$ exclusion")
        #plt.plot(masses23, chis23_scaled)
        #sb.lineplot(x=masses, y=chis_scaled)
        plt.yscale("log")
        plt.xscale("log")
        plt.ylabel(r"$\langle \sigma_V \rangle$")
        plt.xlabel(r"Mass (GeV)")


        def fill(file, label_name):
            posData = np.loadtxt(file)
            plt.fill_between(posData[0],posData[1]*1e-26,posData[2]*1e-26,alpha=0.4,label=label_name)
            
            


        fill("ams2_positrons_{}_bestfit_3sigma_{}_{}_addBaKG.data".format("med","nfw",spec_type), r"$e^{+}$ $3 \sigma$")
        fill("ams2_antiproton_{}_{}_{}_uncorrelated_bestfit_3sigma.data".format(spec_type, "nfw", "med"), r"$\bar{p}$ $3 \sigma$")
        fill("fermi_gc10_{}_{}_bestfit_3sigma.data".format("nfw", spec_type), r"Fermi gc10 $3 \sigma$")
        plt.legend(loc="lower right")
        plt.title("{}: Spectral type {} (substructure accounted for)".format(cluster.name, spec_type))
        plt.show()





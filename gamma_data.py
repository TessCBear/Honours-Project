import numpy as np
import matplotlib.pyplot as plt


clusters = ["coma", "virgo"]
E_list = np.linspace(0.2, 100)
flux_GeV = []
for cluster in clusters:

    if cluster == "coma":
        for energy in E_list:
            if energy >= 0.2 and energy < 1:
                fluxes = [1.98, 2.28, 2.36, 2.38, 2.73, 2.18]
            elif energy >= 1 and energy < 10:
                fluxes = [0.77, 0.76, 0.82, 0.82, 0.74, 1.11]
            elif energy >=10 and energy < 100:
                fluxes = [2.01, 3.03, 3.08, 4.97, 4.88, 2.92]
            else:
                pass
            flux = np.average(fluxes)
            flux *= 6.2415e-10 #conversion from 1e-12 erg to GeV
            flux_GeV.append(flux)
    elif cluster == "virgo":
        flux_GeV = []
        for energy in E_list:
            if energy >= 0.2 and energy < 1:
                fluxes = [4.97, 4.93, 5.26, 5.62, 5.62, 5.71, 5.62, 5.24]
            elif energy >= 1 and energy < 10:
                fluxes = [4.13, 4.65, 4.72, 4.72, 4.59, 4.72, 4.33, 3.89]
            elif energy >=10 and energy < 100:
                fluxes = [4.35, 5.13, 4.48, 4.48, 4.35, 4.48, 5.26, 2.67]
            else:
                pass
            flux = np.average(fluxes)
            flux *= 6.2415e-10 #conversion from 1e-12 erg to GeV
            flux_GeV.append(flux)

    plt.plot(E_list, flux_GeV, )
    plt.xlabel("Energy (GeV)")
    plt.xscale('log')
    plt.ylabel(r"Flux Upper Limit (GeV cm$^{-2}$ s$^{-1}$)")
    plt.title(f"Fermi-LAT Upper Limit Data for {cluster}")
    plt.show()
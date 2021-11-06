masses22 = [75.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]
masses23 = [200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1000.0]

#------Coma data-----#
cchis22 =[6335.804992658254, 12305.240043592616, 39318.2875570577, 85296.44499741016, 148310.25143361028, 237342.42500238662, 349577.55743632716, 487178.0218794631, 660419.3962330305, 847086.8266557403, 1247659.5526308685]
cchis23 = [18632.4631193156, 37202.36681413066, 62921.461096103376, 92675.93301146883, 132777.08293554292, 175082.70317357234, 224569.79955397718, 870843.1497690724, 349577.55743632716]

#-----Virgo data----#
vchis22 = [637.9766808606282, 1239.0621569479156, 5220.567527846975, 11969.557023590429, 20812.215699863373, 32397.426295281955, 46415.88833612782, 62921.461096103376, 80706.20141149507, 100693.86314760271, 140328.9084785873]
vchis23 = [1679.6748720926532, 4301.6357581067905, 7904.92762269642, 12650.337203959038, 18124.175473742358, 25258.200269627847, 32397.426295281955, 122204.46866314887, 50431.59487171359]


chis = vchis23
masses = masses23
type = "23"

chis_scaled = []
chis_nosubs = []
#chis22_scaled = []
for chi in chis:
    chi_nosubs = chi*1e-26
    chi*= 1e-26 *1/35
    chis_scaled.append(chi)
    chis_nosubs.append(chi_nosubs)
    # chis22_scaled.append(chi)

import matplotlib.pyplot as plt
import numpy as np


plt.plot(masses, chis_scaled, label = r"$\chi^2$ exclusion boosted")
plt.plot(masses, chis_nosubs, label = r"$\chi^2$ exclusion")
#plt.plot(masses23, chis23_scaled)
#sb.lineplot(x=masses, y=chis_scaled)
plt.yscale("log")
plt.xscale("log")
plt.ylabel(r"$\langle \sigma_V \rangle$ (cm$^3$ s$^{-1}$)")
plt.xlabel(r"Mass (GeV)")


def fill(file, label_name):
    posData = np.loadtxt(file)
    plt.fill_between(posData[0],posData[1]*1e-26,posData[2]*1e-26,alpha=0.4,label=label_name)
    
    


fill(".\parameter_space\\ams2_positrons_{}_bestfit_3sigma_{}_{}_addBaKG.data".format("med","nfw",type), r"$e^{+}$ $3 \sigma$")
fill(".\parameter_space\\ams2_antiproton_{}_{}_{}_uncorrelated_bestfit_3sigma.data".format(type, "nfw", "med"), r"$\bar{p}$ $3 \sigma$")
fill(".\parameter_space\\fermi_gc10_{}_{}_bestfit_3sigma.data".format("nfw", type), r"Fermi gc10 $3 \sigma$")
plt.legend(loc = "upper left")
plt.title(r"{}: Spectral type {} $\chi^2$ exclusion at 95% CL".format("Virgo", type))
plt.show()



import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

#zmienne
pogoda = np.arange(-10,10,1)
pompadzialanie = np.arange(-0.001,0.0003,0.001)
#funkcje przynaleznosci
pog_snieg = fuzz.trimf(pogoda,[8,10,10])
pog_deszcz = fuzz.trimf(pogoda,[1,8,10])
pog_slonce = fuzz.trapmf(pogoda,[-10,-10,1,8])

pom_działa = fuzz.trimf(pompadzialanie,[-0.001,-0.001,0])
pom_doplyw = fuzz.trimf(pompadzialanie,[0.0001,0.0002,0.0003])
pom_off = fuzz.trimf(pompadzialanie,[-0.001,0,0.0001])

fig, [ax1, ax2] = plt.subplots(nrows=2,ncols=1)

ax1.plot(pogoda,pog_slonce,"r",pogoda,pog_deszcz,"m",pogoda,pog_snieg,"b")
ax1.set_ylabel('Przynaleznosc')
ax1.set_xlabel('Pogoda')
ax1.set_ylim(-0.1,1.1)

ax2.plot(pompadzialanie,pom_działa,'c',pompadzialanie,pom_doplyw,'m',pompadzialanie,pom_off,'ForestGreen')
ax2.set_ylabel("Przynależność")
ax2.set_xlabel("Działąnie pompy")
ax2.set_ylim(-0.1,1.1)

R1 = fuzz.relation_product(pog_deszcz,pom_doplyw)
R2=fuzz.relation_product(pog_snieg,pom_off)
R3=fuzz.relation_product(pog_slonce,pom_działa)
R_combined = np.fmax(R1, np.fmax(R2,R3))

plt.figure(2)
plt.imshow(R_combined)
cbar = plt.colorbar()
cbar.set_label('Przynależność')
plt.yticks([i*10 for i in range(6)]),[str(i*10 -10) for i in range(6)]
plt.ylabel('Pogoda')
plt.xlabel('Pompa')

plt.show()
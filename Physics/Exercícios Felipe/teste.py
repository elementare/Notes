import numpy as np
import math
import matplotlib.pyplot as plt

# Parâmetros "típicos":
N_A = 1e18  # Concentração de aceitadores (cm^-3)
Tmin, Tmax = 100, 1000  # Faixa de temperatura (K)
Eg = 1.0    # Gap do semicondutor (eV)
kB_eV = 8.617e-5  # Constante de Boltzmann em eV/K

# Função "intrínseca" aproximada:
# n_i(T) ~ 2.5e19 * exp(-Eg / 2kB T)  (ordem de grandeza)
# Este 2.5e19 cm^-3 é um valor típico dependendo de (m_e*, m_h*) etc.
def n_intrinsic(T):
    return 2.5e19 * np.exp(-Eg/(2*kB_eV*T))

# Montar array de temperaturas e calcular p(T) de forma piecewise
npoints = 500
T_array = np.linspace(Tmin, Tmax, npoints)
p_array = np.zeros(npoints)

for i, T in enumerate(T_array):
    if T < 200:
        # Freeze-out aproximado:
        # Aqui só faço uma transição suave de p(100 K) até p(200 K)
        # p(100K) ~ 1e16 cm^-3, p(200K) ~ N_A = 1e18 cm^-3, só p/ ilustrar
        # (ISSO É BEM ARTIFICIAL, apenas para ficar "com cara" de freeze-out)
        T1, T2 = 100, 200
        p1, p2 = 1e16, N_A
        # Interpolação exponencial:
        alpha = (T - T1)/(T2 - T1)
        p = p1 * (p2/p1)**alpha
    elif T < 600:
        # Região extrínseca: p ~ N_A (aceitadores totalmente ionizados)
        p = N_A
    else:
        # Região intrínseca significativa: p ~ doping + n_i(T)
        # Quando n_i(T) >> N_A, isso domina
        ni = n_intrinsic(T)
        p = max(N_A, ni)  # Só p/ ficar suave, ou p = N_A + ni
    p_array[i] = p

# Agora geramos ln(p) e 1/T
lnp_array = np.log(p_array)
invT_array = 1.0 / T_array

# Plotar ln(p) vs. 1/T
plt.figure()
plt.plot(invT_array, lnp_array, linewidth=2)
plt.xlabel('1/T (K⁻¹)')
plt.ylabel('ln(p) [p em cm⁻³]')
plt.title('Gráfico qualitativo: ln(p) vs. 1/T (100 K a 1000 K)')
plt.grid(True)

plt.show()


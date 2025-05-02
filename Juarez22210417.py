""" Practica 5: Sistema Cardiovascular


Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México


Nombre del alumno:  Juarez Salazar Angel Eduardo
Número de control: 22210417
Correo institucional: l2221017@tectijuana.edu.mx


Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tend, dt, w, h = 0, 0, 10, 1E-3, 10, 5
N = round((tend - t0) / dt) + 1
t = np.linspace(t0, tend, N)
u = np.sin (2*m.pi*95/60*t) + 0.8

# Función de transferencia sistema cardiovascular
def cardio(Z, C, R, L):
    num = [L * R, R * Z]
    den = [C * L * R * Z, L * (R + Z), R * Z]
    sys = ctrl.tf(num, den)
    return sys

# Casos
Z, C, R, L =  0.020, 0.250, 0.600, 0.005
sysHipotenso = cardio(Z, C, R, L)

Z, C, R, L =0.033, 1.500, 0.950, 0.010
sysNormotenso = cardio(Z, C, R, L)

Z, C, R, L = 0.050, 2.500, 1.400, 0.020
sysHipertenso = cardio(Z, C, R, L)

# Colores
rosa = [255 / 255, 32 / 255, 78 / 255]
rosafuerte= [160 / 255, 21 / 255, 62 / 255]
morado = [93 / 255, 14 / 255, 65 / 255]
azul = [0 / 255, 34 / 255, 77 / 255]

#GRAFICA 1: Todas las señales sin tratamiento 
fig1 = plt.figure()
_, respHipotenso = ctrl.forced_response(sysHipotenso, t, u, x0)
plt.plot(t, respHipotenso, '--', color=rosa, label='Pp(t): Hipotenso')
_, respNormotenso = ctrl.forced_response(sysNormotenso, t, u, x0)
plt.plot(t, respNormotenso, '-', color=morado, label='Pp(t): Normotenso')

_, respHipertenso = ctrl.forced_response(sysHipertenso, t, u, x0)
plt.plot(t, respHipertenso, ':', linewidth=2, color=azul, label='Pp(t): Hipertenso')

plt.xlim(0, 10)
plt.xticks(np.arange(0, 11, 1))
plt.ylim(-0.5, 2)
plt.yticks(np.arange(-0.5, 2.5, 0.5))
plt.xlabel('t [s]', fontsize=12)
plt.ylabel('V(t) [V]', fontsize=12)
plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=3,
fontsize=9, frameon=False)
plt.title('Señales sin tratamiento')
plt.show()

#CONTROLADOR PI 
Cr = 10E-6
Kp = 0.0020645
kI = 44.6377
Re = 1/(kI*Cr); print ('Re = ', Re)


def tratamiento_I(sysCaso, Re, Cr):
    num = [1]
    den = [Re * Cr, 0]
    controlador_I = ctrl.tf(num, den)
    lazo = ctrl.series(controlador_I, sysCaso)
    sistema_controlado = ctrl.feedback(lazo, 1, sign=-1)
    return sistema_controlado

# GRAFICA 2: Normotenso, Hipertenso, Hipertenso 
sysHipertensoTratado = tratamiento_I(sysHipertenso, Re, Cr)

fig2 = plt.figure()
_, respNormotenso = ctrl.forced_response(sysNormotenso, t, u, x0)
plt.plot(t, respNormotenso, '-', color=morado, label='Normotenso')

_, respHipertenso = ctrl.forced_response(sysHipertenso, t, u, x0)
plt.plot(t, respHipertenso, '-', color=rosa, label='Hipertenso')

_, respTratado = ctrl.forced_response(sysHipertensoTratado, t, u, x0)
plt.plot(t, respTratado, ':', linewidth=2, color=azul, label='Tratamiento (Hipertenso)')
plt.xlim(0, 10)

plt.ylim(-0.5, 2)
plt.xlabel('t [s]')
plt.ylabel('V(t) [V]')
plt.xticks(np.arange(0, 11, 1))
plt.yticks(np.arange(-0.5, 2.5, 0.5))
plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=3,
fontsize=9, frameon=False)
plt.title('Tratamiento del Hipertenso')
plt.show()

#GRAFICA 3: Normotenso, Hipotenso, Hipotenso 
sysHipotensoTratado = tratamiento_I(sysHipotenso, Re, Cr)

fig3 = plt.figure()
_, respNormotenso = ctrl.forced_response(sysNormotenso, t, u, x0)
plt.plot(t, respNormotenso, '-', color=morado, label='Normotenso')

_, respHipotenso = ctrl.forced_response(sysHipotenso, t, u, x0)
plt.plot(t, respHipotenso, '-', color=rosa, label='Hipotenso')

_, respTratado = ctrl.forced_response(sysHipotensoTratado, t, u, x0)
plt.plot(t, respTratado, ':', linewidth=2, color=azul, label='Tratamiento (Hipotenso)')
plt.xlim(0, 10)

plt.ylim(-0.5, 2)
plt.xlabel('t [s]')
plt.ylabel('V(t) [V]')
plt.xticks(np.arange(0, 11, 1))
plt.yticks(np.arange(-0.5, 2.5, 0.5))
plt.legend(bbox_to_anchor=(0.5, -0.2), loc='center', ncol=3,
fontsize=9, frameon=False)
plt.title('Tratamiento del Hipotenso')
plt.show()

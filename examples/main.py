from __future__ import print_function

from edibles.fit.models.create_model import *
from edibles.functions.atomic_line_tool import AtomicLines
from edibles.functions.edibles_spectrum import EdiblesSpectrum
from edibles.fit.models.models import Sightline
from edibles.fit.fit import fit
import matplotlib.pyplot as plt

# ======================================
# ======================================

star_name = 'HD170740'
file = '/HD170740/RED_860/HD170740_w860_redl_20140916_O12.fits'
xmin = 7661.
xmax = 7670.
sp = EdiblesSpectrum(file)
data = sp.getSpectrum(xmin, xmax)
wave, flux = data

# Cont parameters
n_points = 4
cont = createCont(data, n_points)

slightline = Sightline(star_name=star_name, cont=cont)

slightline.addCloud(cloud_name='Telluric', b=1.07, d=0.046)
slightline.addLine(name='tell_1', lam_0=7664.8, tau_0=0.75)
slightline.addLine(name='tell_2', lam_0=7666, tau_0=0.75)

slightline.addCloud(cloud_name='Interstellar', b=1.0, d=0.001)
slightline.addLine(name='KI_1', lam_0=7665.3, tau_0=0.1)
slightline.addLine(name='KI_2', lam_0=7665.35, tau_0=0.05)


# fit_model = fit(star_name, data, cloud.model)
fit_model = fit(star_name, data, slightline.model)
# print(fit_model)

# ======================================
# ======================================

# using dupCloud
file = '/HD148937/BLUE_346/HD148937_w346_blue_20150817_O11.fits'
star = 'HD148937'
wave, flux = EdiblesSpectrum(file).getSpectrum(3301.5, 3304)
plt.plot(wave, flux)
plt.title(file)
plt.show()

cont = createCont((wave, flux), 3)
slightline = Sightline(star_name=star, cont=cont)
slightline.addCloud('Cloud 1', 1.42631e-07, 0.036356)
slightline.addLine('NaI_1', lam_0=3302.46, tau_0=0.06)
slightline.addLine('NaI_2', lam_0=3303.1, tau_0=0.03)

slightline.dupCloud('Cloud 1', 'Cloud 2', 1.00005)
slightline.dupCloud('Cloud 1', 'Cloud 3', 0.99995)

fit_model = fit(star, (wave, flux), slightline.model, breakdown=True)

# star_name = 'HD170740'
# file = '/HD170740/BLUE_346/HD170740_w346_n20_20140916_B.fits'
# xmin = 3301.
# xmax = 3305.
# ion0 = 'Na I'
# wave0 = 3302.3
# ion1 = 'Na I'
# wave1 = 3302.9

# sp = EdiblesSpectrum(file)
# data = sp.getSpectrum(xmin,xmax)
# wave, flux = data

# # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# # Continuum
# n_points = 3
# cont = createCont(data, n_points)

# # ==========
# model = cont

# # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# # ion0 = 'Na I'
# # wave0 = wave[peaks[0]]
# # ion1 = 'Na I'
# # wave1 = wave[peaks[1]]

# # AtomicLineList = AtomicLines()
# # f0 = AtomicLineList.get_f_known(ion0, wave0)
# # f1 = AtomicLineList.get_f_known(ion1, wave1)

# # name    = ['line0', 'line1']
# # lam_0   = [wave[peaks[0]], wave[peaks[1]]]
# # b       = [2.0, 2.0]
# # d       = [0.005, 0.005]
# # N       = [0.14, 0.14]
# # f_known = [f0, f1]

# # cloud = createKnownCloud(name=name, num_lines=2, lam_0=lam_0, b=b, d=d, N=N, f_known=f_known)
# # model *= cloud

# # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# AtomicLineList = AtomicLines()
# f0 = AtomicLineList.get_f_known(ion0, wave0)
# f1 = AtomicLineList.get_f_known(ion1, wave1)

# lab_wave0 = AtomicLineList.getLabWavelength(ion0, wave0)
# lab_wave1 = AtomicLineList.getLabWavelength(ion1, wave1)
# lab_list = [lab_wave0, lab_wave1]

# name    = ['line0', 'line1']
# v_cloud = 18
# b       = 2
# d       = 0.005
# N       = 6.61966e+13
# f_known = [f0, f1]

# cloud = createKnownVelocityCloud(name=name, num_lines=2, v_cloud=v_cloud, b=b, d=d, N=N, f_known=f_known, lab_lam_0=lab_list)

# for line in cloud:
#     model *= line

# # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# fit_model = fit(star_name, data, model)

# for line in model:
#     print(line)
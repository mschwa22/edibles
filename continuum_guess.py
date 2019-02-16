import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from astropy.modeling.models import Voigt1D
from astropy import constants as cst


import sys
import os
path = os.getcwd()
os.chdir('..')
sys.path.append(os.getcwd())
os.chdir(path)

# from edibles.voigtMathematical import voigt_math
from edibles.fit.make_grid import make_grid


def generateContinuum(x, y, n_piece=2, move_x=False, move_y=True):
	'''
	This function fits a continuum to data separated into n sections
	where the x and y-values are the median of each section	using a cubic spline

	INPUT:
	x: [ndarray] wavelength grid
	y: [ndarray] flux values
	n_piece: [int, default=4] evenly split data into n sections
	move_x: [bool, default=False] change x values of points to fit
	move_y: [bool, default=True] change y values of points to fit

	OUTPUT:
	x_cont: [ndarray] wavelength grid points for fit continuum
	y_cont: [ndarray] flux value points for fit continuum
	'''

	# # resolving power of 0.1 km/s
	# R = cst.c.to('cm/s').value * 1.0e-5 / 0.1

	# make resolving power 1 m/s
	R = cst.c.to('m/s').value

	# print('Resolotion: ', R)


	# delta_lambda = lambda_peak / R
	# xmin = min(x)
	# xmax = max(x)
	# x_nonbroad = np.arange(xmin, xmax, delta_lambda)
	# # using this method for making grid increase fitting time so much
	# # x_nonbroad = mg.make_grid(xmin, xmax, resolution=R)

	x_nonbroad = make_grid(np.min(x), np.max(x), resolution=R)
	x_spline = np.array(x_nonbroad)

	x_sections = np.array_split(x, n_piece)
	y_sections = np.array_split(y, n_piece)

	x_value_array = []
	y_value_array = []
	for i in range(len(x_sections)):
		x_value = np.median(x_sections[i])
		y_value = np.median(y_sections[i])
		x_value_array.append(x_value)
		y_value_array.append(y_value)

	spline = CubicSpline(x_value_array, y_value_array)
	# x_spline = np.linspace(np.min(x), np.max(x), (len(x)))
	y_spline = spline(x_spline)

	# # plot median points of each section
	# plt.plot(x_value_array, y_value_array, 'ko')

	return x_spline, y_spline


# Example

alpha, gamma = 0.1, 0.1

wave = np.linspace(7666, 7668, 1000)
# flux = -voigt_math(wave, alpha, gamma)
voigt_func = Voigt1D(x_0=7667, amplitude_L=10, fwhm_L=0.1, fwhm_G=0.2)
flux = -1 * voigt_func(wave)

# Generate the spline curve
x_spline, y_spline = generateContinuum(wave, flux)


plt.plot(wave, flux, marker='o', markersize='3', label='Data')
plt.plot(x_spline, y_spline, label='Spline fit')
plt.legend()
plt.show()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 12:31:34 2020

@author: amelielaurens

Source : A simple model for nanofiber formation by rotary jet-spinning
by mellado et al.

Goal : Prediction of the final radius for various reservoir radius.

Select the machine and the polymer for which we want to run the code and ajust values
in deck.yaml file.

Polymer parameters : the density, the viscosity, the surface tension
Machine parameters  : the collector radius, the orifice radius,
                      the angular viscosity of the spinneret.
Discretisation number

All data are in SI units.

"""

from deck import Deck
from machine import RJSMachine
from polymer import Polymer
from models_rjs import *
import numpy
import matplotlib.pyplot as plt

deck = Deck("deck.yaml")
machine = RJSMachine(deck)
polymer = Polymer(deck)

discretisation = int(deck.doc['Discretisation'])
# The higher the discretisation number is, the finer the discretisation will be,
# there will be more points on the graphic.

# Reach machine parameters
name_machine = machine.name
Rc = machine.collector_radius
omega = machine.omega
orifice_radius = machine.orifice_radius

# Reach polymer parameters
name_polymer = polymer.name
rho = polymer.density
mu = polymer.viscosity
surface_tension = polymer.surface_tension

s0 = numpy.linspace(0.01, 0.1, discretisation)

omega_th = []
initial_velocity = []
for l in range(discretisation):
    omega_th.append(critical_rotational_velocity_threshold(surface_tension,
                                                           orifice_radius, s0[l], rho))
    initial_velocity.append(Initial_velocity(omega_th[l], s0[l]))
omega_th = numpy.array(omega_th)
initial_velocity = numpy.array(initial_velocity)

nu = kinematic_viscosity(mu, rho)


final_radius = []
for k in range(discretisation):
    final_radius.append(final_radius_approx(orifice_radius, initial_velocity[k],
                                            nu, Rc, omega))
final_radius = numpy.array(final_radius)

fig = plt.figure()
axes = fig.add_subplot(1, 1, 1)

for i in range(discretisation):
    axes.plot(s0[i], final_radius[i], 'ro')
axes.grid()
axes.set_xlabel("Radius of the reservoir (m)", fontsize=16)
axes.set_ylabel("Final radius (m)", fontsize=16)
axes.set_title(" %s / %s " % (name_machine, name_polymer), fontsize=16, y=1.)

# Plot a zoomed graphic on the small radius below 0.00002 m
fig2 = plt.figure()
axes = fig2.add_subplot(1, 1, 1)

for i in range(discretisation-1):
    if final_radius[i] <= 0.00002:
        axes.plot(s0[i], final_radius[i], 'bo')
axes.grid()
axes.set_xlabel("Radius of the reservoir (m)", fontsize=16)
axes.set_ylabel("Final radius  (m)", fontsize=16)
axes.set_title("ZOOM %s / %s " % (name_machine, name_polymer), fontsize=16, y=1.05)

plt.show()

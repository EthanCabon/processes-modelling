#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 13:10:31 2020

@author: amelielaurens

Source : A simple model for nanofiber formation by rotary jet-spinning
by mellado et al.

Goal : Prediction of the radius of the jet in steady state as a function of
the axial coordinate x.

Select the machine and the polymer for which we want to run the code and ajust values
in deck.yaml file.

Polymer parameters : the density, the viscosity, the surface tension
Machine parameters  : the reservoir radius, the collector radius,
                      the orifice radius, the angular viscosity of the spinneret.
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
s0 = machine.reservoir_radius
Rc = machine.collector_radius
omega = machine.omega
orifice_radius = machine.orifice_radius

# Reach polymer parameters
name_polymer = polymer.name
rho = polymer.density
mu = polymer.viscosity
surface_tension = polymer.surface_tension

x_position = numpy.linspace(0, Rc-s0, discretisation)

omega_th = critical_rotational_velocity_threshold(surface_tension,
                                                  orifice_radius, s0, rho)
initial_velocity = Initial_velocity(omega_th, s0)
Sigma = []
for l in range(discretisation):
    Sigma.append(sigma(surface_tension, x_position[l], orifice_radius,
                       initial_velocity))
Sigma = numpy.array(Sigma)

radius = []
for k in range(1, discretisation):
    radius.append(Radius(orifice_radius, rho, initial_velocity, x_position[k],
                         mu, Sigma[k], omega))
radius = numpy.array(radius)

fig = plt.figure()
axes = fig.add_subplot(1, 1, 1)

for i in range(discretisation-1):
    axes.plot(x_position[i], radius[i], 'ro')
axes.grid()
axes.set_xlabel("Axial coordinate x (m)", fontsize=16)
axes.set_ylabel("Radius (m)", fontsize=16)
axes.set_title(" %s / %s " % (name_machine, name_polymer), fontsize=16, y=1.)

# tracer un graphe zoomé sur les petits rayons inférieurs à 0.00010 m
fig2 = plt.figure()
axes = fig2.add_subplot(1, 1, 1)

for i in range(discretisation-1):
    if radius[i] <= 0.00010:
        axes.plot(x_position[i], radius[i], 'bo')
axes.grid()
axes.set_xlabel("Axial coordinate x (m)", fontsize=16)
axes.set_ylabel("Radius (m)", fontsize=16)
axes.set_title("ZOOM %s / %s " % (name_machine, name_polymer), fontsize=16, y=1.05)

plt.show()

import openmc
import openmc.lib
import numpy as np
from matplotlib import pyplot as plt

import os
import sys
script_dir = os.path.dirname(__file__)
sys.path.append(script_dir)
import common as specs

# This is a simplified OpenMC model of a CEFR fuel subassembly; for this multiphysics
# tutorial, we focus only on the active region, with a height of 45 cm
# (just out of simplicity and to make the training more tractable for the time allotted).

model = openmc.Model()

# create materials

# UO2 for Fuel
UO2 = openmc.Material()
UO2.set_density('sum')
UO2.add_nuclide('U235',1.49981E-02,'ao')
UO2.add_nuclide('U238',8.26381E-03,'ao')
UO2.add_nuclide('O16', 4.69512E-02,'ao')

# 15-15Ti Stainless Steel
SS = openmc.Material()
SS.set_density('atom/b-cm',density=8.49843E-02)
SS.add_nuclide('Fe54' ,3.18736E-03 )
SS.add_nuclide('Fe56' ,5.00347E-02 )
SS.add_nuclide('Fe57' ,1.15552E-03 )
SS.add_nuclide('Fe58' ,1.53779E-04 )
SS.add_nuclide('Cr50' ,6.43727E-04 )
SS.add_nuclide('Cr52' ,1.24136E-02 )
SS.add_nuclide('Cr53' ,1.40761E-03 )
SS.add_nuclide('Cr54' ,3.50383E-04 )
SS.add_nuclide('Ni58' ,8.11014E-03 )
SS.add_nuclide('Ni60' ,3.12399E-03 )
SS.add_nuclide('Ni61' ,1.35798E-04 )
SS.add_nuclide('Ni62' ,4.32997E-04 )
SS.add_nuclide('Ni64' ,1.10257E-04 )
SS.add_nuclide('Mo92' ,1.57916E-04 )
SS.add_nuclide('Mo94' ,9.94445E-05 )
SS.add_nuclide('Mo95' ,1.72153E-04 )
SS.add_nuclide('Mo96' ,1.81174E-04 )
SS.add_nuclide('Mo97' ,1.04335E-04 )
SS.add_nuclide('Mo98' ,2.65077E-04 )
SS.add_nuclide('Mo100',1.06726E-04 )
SS.add_nuclide('Mn55' ,1.29433E-03 )
SS.add_nuclide('C0'   ,2.37026E-04 )
SS.add_nuclide('Ti46' ,2.85966E-05 )
SS.add_nuclide('Ti47' ,2.57889E-05 )
SS.add_nuclide('Ti48' ,2.55532E-04 )
SS.add_nuclide('Ti49' ,1.87524E-05 )
SS.add_nuclide('Ti50' ,1.79552E-05 )
SS.add_nuclide('Si28' ,7.00451E-04 )
SS.add_nuclide('Si29' ,3.55834E-05 )
SS.add_nuclide('Si30' ,2.34843E-05 )

# Ti316 Stainless Steel
Ti316 = openmc.Material()
Ti316.set_density('atom/b-cm',density=8.54309E-02)
Ti316.add_nuclide('Fe54' ,3.23855E-03)
Ti316.add_nuclide('Fe56' ,5.08384E-02)
Ti316.add_nuclide('Fe57' ,1.17408E-03)
Ti316.add_nuclide('Fe58' ,1.56248E-04)
Ti316.add_nuclide('Cr50' ,6.74283E-04)
Ti316.add_nuclide('Cr52' ,1.30029E-02)
Ti316.add_nuclide('Cr53' ,1.47442E-03)
Ti316.add_nuclide('Cr54' ,3.67015E-04)
Ti316.add_nuclide('Ni58' ,6.88162E-03)
Ti316.add_nuclide('Ni60' ,2.65077E-03)
Ti316.add_nuclide('Ni61' ,1.15228E-04)
Ti316.add_nuclide('Ni62' ,3.67407E-04)
Ti316.add_nuclide('Ni64' ,9.35550E-05)
Ti316.add_nuclide('Mo92' ,1.79675E-04)
Ti316.add_nuclide('Mo94' ,1.13147E-04)
Ti316.add_nuclide('Mo95' ,1.95874E-04)
Ti316.add_nuclide('Mo96' ,2.06138E-04)
Ti316.add_nuclide('Mo97' ,1.18712E-04)
Ti316.add_nuclide('Mo98' ,3.01602E-04)
Ti316.add_nuclide('Mo100',1.21432E-04)
Ti316.add_nuclide('Mn55' ,1.51194E-03)
Ti316.add_nuclide('C0'   ,2.37324E-04)
Ti316.add_nuclide('Ti46' ,3.27229E-05)
Ti316.add_nuclide('Ti47' ,2.95101E-05)
Ti316.add_nuclide('Ti48' ,2.92403E-04)
Ti316.add_nuclide('Ti49' ,2.14583E-05)
Ti316.add_nuclide('Ti50' ,2.05460E-05)
Ti316.add_nuclide('Si28' ,9.35106E-04)
Ti316.add_nuclide('Si29' ,4.75041E-05)
Ti316.add_nuclide('Si30' ,3.13517E-05)

# sodium
sodium = openmc.Material()
sodium.set_density('sum')
sodium.add_nuclide('Na23',2.33599E-02)

# helium
He = openmc.Material()
He.set_density('sum')
He.add_nuclide('He4',1.00000E-11)

model.materials = openmc.Materials([UO2, SS, Ti316, He, sodium])

# Define the surfaces needed for a fuel pin
helium_hole_surface = openmc.ZCylinder(x0=0, y0=0, r=specs.hole_diameter/2.0)
fuel_surface        = openmc.ZCylinder(x0=0, y0=0, r=specs.pellet_diameter/2.0)
clad_inner_surface  = openmc.ZCylinder(x0=0, y0=0, r=specs.inner_clad_diameter/2.0)
clad_outer_surface  = openmc.ZCylinder(x0=0, y0=0, r=specs.outer_clad_diameter/2.0)

# Define the surfaces needed for the various hexagons enclosing the assembly,
# defining the duct, etc.
hex_WR_IN    = openmc.model.hexagonal_prism(orientation='y', origin=(0.0, 0.0), edge_length= 3.281335614) # pitch=2.84172, Wrapper tube inner flat-to-flat/2 (cm)
hex_WR_OU    = openmc.model.hexagonal_prism(orientation='y', origin=(0.0, 0.0), edge_length= 3.420465482) # pitch=2.96221, Wrapper tube outer flat-to-flat/2 (cm)
hex_SA_PITCH = openmc.model.hexagonal_prism(orientation='y', origin=(0.0, 0.0), edge_length= 3.536385869, boundary_type='reflective') # pitch=3.06260, S/A Pitch          flat-to-flat/2 (cm)
hexcore = openmc.model.hexagonal_prism(orientation='x', origin=(0.0, 0.0),edge_length= 3.536385869, boundary_type='reflective')

# define axial surfaces which will bound the active fissile region
lower = openmc.ZPlane(z0=0.0, boundary_type='vacuum')
upper = openmc.ZPlane(z0=specs.height, boundary_type='vacuum')

# create the cells in a fuel pin
helium_hole    = openmc.Cell(fill=He,     region=-helium_hole_surface)
fuel_annulus   = openmc.Cell(fill=UO2,    region=+helium_hole_surface & -fuel_surface)
helium_gap     = openmc.Cell(fill=He,     region=+fuel_surface & -clad_inner_surface)
ss_clad        = openmc.Cell(fill=SS,     region=+clad_inner_surface & -clad_outer_surface)
sodium_annulus = openmc.Cell(fill=sodium, region=+clad_outer_surface)

fuel_pin_universe = openmc.Universe(cells=[helium_hole, fuel_annulus, helium_gap, ss_clad, sodium_annulus])

# pure sodium universe
sodium_universe = openmc.Universe(cells=[openmc.Cell(fill=sodium)])

# create a lattice for a fuel assembly, consisting of 61 fuel pins
fuel_pin_lattice = openmc.HexLattice()
fuel_pin_lattice.center = [0., 0.]
fuel_pin_lattice.pitch  = [specs.pin_pitch]
fuel_pin_lattice.universes = [[sodium_universe]*30, [fuel_pin_universe]*24, [fuel_pin_universe]*18, [fuel_pin_universe]*12, [fuel_pin_universe]*6, [fuel_pin_universe]]

# put that fuel pin lattice inside a hexagon boundary, then add additional hexagons
# to represent the duct. For each, place inside the axial extents
layer = +lower & -upper
fuel_hex_cell = openmc.Cell(region=hex_WR_IN & layer, fill=fuel_pin_lattice)
duct_cell = openmc.Cell(region=hex_WR_OU & ~hex_WR_IN & layer, fill=Ti316)
sodium_cell = openmc.Cell(region=~hex_WR_OU & hex_SA_PITCH & layer, fill=sodium)

root = openmc.Universe(cells=[fuel_hex_cell, duct_cell, sodium_cell])
model.geometry = openmc.Geometry(root)

###############################################################################
#                   Exporting to OpenMC settings.xml file
###############################################################################

# Instantiate a Settings object, set all runtime parameters, and export to XML
model.settings.batches   = 120  #1050   # sum of active & inactive cycles
model.settings.inactive  = 20   #50
model.settings.particles = 1000 #100000
model.settings.ptables   = True
model.settings.temperature['method']='interpolation'

# Create an initial uniform spatial source distribution over fissionable zones
bounds = [-5.0, -5.0, 0.0, 5.0, 5.0, specs.height]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True )
model.settings.source = openmc.source.IndependentSource(space=uniform_dist)

# Create some plots for visualization
plot1          = openmc.Plot()
plot1.filename = 'plot1'
plot1.width    = (8, 8)
plot1.basis    = 'xy'
plot1.origin   = (0.0, 0.0, 0.5*specs.height)
plot1.pixels   = (2000, 2000)
plot1.color_by = 'material'

model.plots = openmc.Plots([plot1])

model.export_to_xml()


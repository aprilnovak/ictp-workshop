import openmc
import openmc.lib
import numpy as np
from matplotlib import pyplot as plt

# create materials

# UO2 for Fuel
UOF = openmc.Material( name='UOF')
UOF.set_density('sum')
UOF.add_nuclide('U235',1.49981E-02,'ao')
UOF.add_nuclide('U238',8.26381E-03,'ao')
UOF.add_nuclide('O16', 4.69512E-02,'ao')

# UO2 for Blanket
# --- UOB at T=250.0 deg-C
UOB = openmc.Material( name='UOB')
UOB.set_density('sum')
UOB.add_nuclide('U235',1.04432E-04,'ao')
UOB.add_nuclide('U238',2.30457E-02,'ao')
UOB.add_nuclide('O16', 4.69594E-02,'ao')

# 15-15Ti Stainless Steel
# --- SS at T=250.0 deg-C
SS = openmc.Material( name='SS')
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
# --- 316Ti at T=250.0 deg-C
Ti316 = openmc.Material( name='Ti316')
Ti316.set_density('atom/b-cm',density=8.54309E-02)
Ti316.add_nuclide('Fe54' ,3.23855E-03 ) 
Ti316.add_nuclide('Fe56' ,5.08384E-02 ) 
Ti316.add_nuclide('Fe57' ,1.17408E-03 ) 
Ti316.add_nuclide('Fe58' ,1.56248E-04 ) 
Ti316.add_nuclide('Cr50' ,6.74283E-04 ) 
Ti316.add_nuclide('Cr52' ,1.30029E-02 ) 
Ti316.add_nuclide('Cr53' ,1.47442E-03 ) 
Ti316.add_nuclide('Cr54' ,3.67015E-04 ) 
Ti316.add_nuclide('Ni58' ,6.88162E-03 ) 
Ti316.add_nuclide('Ni60' ,2.65077E-03 ) 
Ti316.add_nuclide('Ni61' ,1.15228E-04 ) 
Ti316.add_nuclide('Ni62' ,3.67407E-04 ) 
Ti316.add_nuclide('Ni64' ,9.35550E-05 ) 
Ti316.add_nuclide('Mo92' ,1.79675E-04 ) 
Ti316.add_nuclide('Mo94' ,1.13147E-04 ) 
Ti316.add_nuclide('Mo95' ,1.95874E-04 ) 
Ti316.add_nuclide('Mo96' ,2.06138E-04 ) 
Ti316.add_nuclide('Mo97' ,1.18712E-04 ) 
Ti316.add_nuclide('Mo98' ,3.01602E-04 ) 
Ti316.add_nuclide('Mo100',1.21432E-04 ) 
Ti316.add_nuclide('Mn55' ,1.51194E-03 ) 
Ti316.add_nuclide('C0'   ,2.37324E-04 ) 
Ti316.add_nuclide('Ti46' ,3.27229E-05 ) 
Ti316.add_nuclide('Ti47' ,2.95101E-05 ) 
Ti316.add_nuclide('Ti48' ,2.92403E-04 ) 
Ti316.add_nuclide('Ti49' ,2.14583E-05 ) 
Ti316.add_nuclide('Ti50' ,2.05460E-05 ) 
Ti316.add_nuclide('Si28' ,9.35106E-04 ) 
Ti316.add_nuclide('Si29' ,4.75041E-05 ) 
Ti316.add_nuclide('Si30' ,3.13517E-05 ) 

# -------------------------------------------------------
# --- Sodium for all regions
# -------------------------------------------------------
Na_FU = openmc.Material( name='Na_FU')
Na_FU.set_density('sum')
Na_FU.add_nuclide('Na23',2.33599E-02)

# -------------------------------------------------------
# --- He in different locations
# -------------------------------------------------------
He = openmc.Material( name='He')
He.set_density('sum')
He.add_nuclide('He4',1.00000E-11)

vacuum = openmc.Material( name='vacuum')
vacuum.set_density('sum')
vacuum.add_nuclide('He4',1.00000E-23)

# -------------------------------------------------------
# --- Homogeneous mixtures
# -------------------------------------------------------
# ---    OpenMC format
# ---    <matname> = openmc.Material.mix_materials ([<mat1>,<mat2>, ...], [<frac1>,<frac2>, ...], 'xx')
# ---    'xx': Mass fractions are entered with 'wo', and volume fractions with 'vo'.
#
# --- Homogeneous spring-NA
HOMOG_SPR_FU = openmc.Material.mix_materials([Ti316,He], [0.173,0.827], 'vo', name='HOMOG_SPR_FU')

materials_file = openmc.Materials([
UOF,
UOB,
SS,
Ti316,
He,
vacuum,
Na_FU,
HOMOG_SPR_FU
])

materials_file.export_to_xml()


#-----------------------------------------------------------------------------------
# --- Pin surfaces - fuel
#-----------------------------------------------------------------------------------
# --- 61 pin lattices (same inner/outer clad)
#
# ---  Fuel fissile
cyl_FI_hole = openmc.ZCylinder( x0=0, y0=0, r=0.08020, name='cyl_FI_hole') # Fissile fuel pellet inner hole radius (cm)
cyl_FI_fuel = openmc.ZCylinder( x0=0, y0=0, r=0.25565, name='cyl_FI_fuel') # Fissile fuel pellet radius (cm)
# ---  Fuel fertile
cyl_FE_fuel = openmc.ZCylinder( x0=0, y0=0, r=0.25559, name='cyl_FE_fuel') # Fertile fuel pellet radius (cm)
# --- Cladding
cyl_Clad61_IN = openmc.ZCylinder( x0=0, y0=0, r=0.27112, name='cyl_Clad61_IN') # Inner clad radius (cm)
cyl_Clad61_OU = openmc.ZCylinder( x0=0, y0=0, r=0.30499, name='cyl_Clad61_OU') # Outer clad radius (cm)

#-----------------------------------------------------------------------------------
# --- Radial surfaces - Fuel assembly
#-----------------------------------------------------------------------------------
hex_HEA_IN   = openmc.model.hexagonal_prism(orientation='y', origin=(0.0, 0.0),edge_length= 2.909856904) # pitch = 2.52001, Head inner flat-to-flat/2 (cm)
cyl_USH_hole = openmc.ZCylinder( x0=0, y0=0, r=1.60662, name='cyl_USH_hole')                       #                  Upper shield inner hole radius (cm)
hex_UCN_IN   = openmc.model.hexagonal_prism(orientation='y', origin=(0.0, 0.0),edge_length= 3.234720353) # pitch = 2.80135, Upper connector inner flat-to-flat/2 (cm)
hex_LCN_IN   = openmc.model.hexagonal_prism(orientation='y', origin=(0.0, 0.0),edge_length= 3.310260862) # pitch = 2.86677, Lower connector inner flat-to-flat/2 (cm)

# --- SA wrapper hexagons
hex_WR_IN    = openmc.model.hexagonal_prism(orientation='y', origin=(0.0, 0.0),edge_length= 3.281335614) # pitch=2.84172, Wrapper tube inner flat-to-flat/2 (cm)
hex_WR_OU    = openmc.model.hexagonal_prism(orientation='y', origin=(0.0, 0.0),edge_length= 3.420465482) # pitch=2.96221, Wrapper tube outer flat-to-flat/2 (cm)
hex_SA_PITCH = openmc.model.hexagonal_prism(orientation='y', origin=(0.0, 0.0),edge_length= 3.536385869) # pitch=3.06260, S/A Pitch          flat-to-flat/2 (cm)


#-----------------------------------------------------------------------------------
# --- Axial surfaces - Fuel assembly
#-----------------------------------------------------------------------------------
# --- fuel - axial s/a regions - upper boundary
pz_FUEL_HEA = openmc.ZPlane( z0= 220.473 ,name='pz_FUEL_HEA') # 01 - Head
pz_FUEL_USH = openmc.ZPlane( z0= 197.377 ,name='pz_FUEL_USH') # 02 - Upper shield
pz_FUEL_UCN = openmc.ZPlane( z0= 150.183 ,name='pz_FUEL_UCN') # 03 - Upper connector
pz_FUEL_TEP = openmc.ZPlane( z0= 144.158 ,name='pz_FUEL_TEP') # 04 - Top end plug
pz_FUEL_SPR = openmc.ZPlane( z0= 143.154 ,name='pz_FUEL_SPR') # 05 - Spring
pz_FUEL_UBL = openmc.ZPlane( z0= 137.631 ,name='pz_FUEL_UBL') # 06 - Upper blanket
pz_FUEL_FIS = openmc.ZPlane( z0= 127.608 ,name='pz_FUEL_FIS') # 07 - Fissile
pz_FUEL_LBL = openmc.ZPlane( z0= 82.494  ,name='pz_FUEL_LBL') # 08 - Lower blanket
pz_FUEL_LGP = openmc.ZPlane( z0= 57.437  ,name='pz_FUEL_LGP') # 09 - Lower gas plenum
pz_FUEL_BEP = openmc.ZPlane( z0= 12.251  ,name='pz_FUEL_BEP') # 10 - Bottom end plug
pz_FUEL_LCN = openmc.ZPlane( z0= 8.736   ,name='pz_FUEL_LCN') # 11 - Lower connector


#-----------------------------------------------------------------------------------
# --- Core surfaces
#-----------------------------------------------------------------------------------
pz_BOT   = openmc.ZPlane( z0= 0.00    ,name='pz_BOT', boundary_type='vacuum')
pz_TOP   = openmc.ZPlane( z0= 221.778 ,name='pz_TOP', boundary_type='vacuum') # 221.778

# Surface define for CORE
hexcore = openmc.model.hexagonal_prism(orientation='x', origin=(0.0, 0.0),edge_length= 3.536385869, boundary_type='reflective')


# -------------------------------------------------------
# --- Pins - Fuel assemblies
# -------------------------------------------------------

# --- Void
# a_OU
c_VOID = openmc.Cell( name='c_VOID')
c_VOID.fill = None
a_OU = openmc.Universe()
a_OU.add_cells([c_VOID])

# --- Top end plug (TEP)
c_FU_TEP1 = openmc.Cell( name='c_FU_TEP1')
c_FU_TEP2 = openmc.Cell( name='c_FU_TEP2')

c_FU_TEP1.region = -cyl_Clad61_OU
c_FU_TEP2.region = +cyl_Clad61_OU

c_FU_TEP1.fill = SS
c_FU_TEP2.fill = Na_FU

p_FU_TEP = openmc.Universe()
p_FU_TEP.add_cells([
c_FU_TEP1,
c_FU_TEP2
])

# --- Spring (SPR)
c_FU_SPR1 = openmc.Cell( name='c_FU_SPR1')
c_FU_SPR2 = openmc.Cell( name='c_FU_SPR2')
c_FU_SPR3 = openmc.Cell( name='c_FU_SPR3')

c_FU_SPR1.region = -cyl_Clad61_IN
c_FU_SPR2.region = +cyl_Clad61_IN & -cyl_Clad61_OU
c_FU_SPR3.region = +cyl_Clad61_OU

c_FU_SPR1.fill = HOMOG_SPR_FU
c_FU_SPR2.fill = SS
c_FU_SPR3.fill = Na_FU

p_FU_SPR = openmc.Universe()
p_FU_SPR.add_cells([
c_FU_SPR1,
c_FU_SPR2,
c_FU_SPR3
])

# --- Upper fuel fertile/blanket (UBL)
c_FU_UBL_1 = openmc.Cell( name='c_FU_UBL_1')
c_FU_UBL_2 = openmc.Cell( name='c_FU_UBL_2')
c_FU_UBL_3 = openmc.Cell( name='c_FU_UBL_3')
c_FU_UBL_4 = openmc.Cell( name='c_FU_UBL_4')

c_FU_UBL_1.region = -cyl_FE_fuel
c_FU_UBL_2.region = +cyl_FE_fuel   & -cyl_Clad61_IN
c_FU_UBL_3.region = +cyl_Clad61_IN & -cyl_Clad61_OU
c_FU_UBL_4.region = +cyl_Clad61_OU

c_FU_UBL_1.fill = UOB
c_FU_UBL_2.fill = He
c_FU_UBL_3.fill = SS
c_FU_UBL_4.fill = Na_FU

p_FU_UBL = openmc.Universe()
p_FU_UBL.add_cells([c_FU_UBL_1, c_FU_UBL_2, c_FU_UBL_3, c_FU_UBL_4])

# --- Fuel fissile (FIS)
c_FU_FIS_0 = openmc.Cell( name='c_FU_FIS_0')
c_FU_FIS_1 = openmc.Cell( name='c_FU_FIS_1')
c_FU_FIS_2 = openmc.Cell( name='c_FU_FIS_2')
c_FU_FIS_3 = openmc.Cell( name='c_FU_FIS_3')
c_FU_FIS_4 = openmc.Cell( name='c_FU_FIS_4')

c_FU_FIS_0.region = -cyl_FI_hole
c_FU_FIS_1.region = +cyl_FI_hole   & -cyl_FI_fuel
c_FU_FIS_2.region = +cyl_FI_fuel   & -cyl_Clad61_IN
c_FU_FIS_3.region = +cyl_Clad61_IN & -cyl_Clad61_OU
c_FU_FIS_4.region = +cyl_Clad61_OU

c_FU_FIS_0.fill = He
c_FU_FIS_1.fill = UOF
c_FU_FIS_2.fill = He
c_FU_FIS_3.fill = SS
c_FU_FIS_4.fill = Na_FU

p_FU_FIS = openmc.Universe()
p_FU_FIS.add_cells([
c_FU_FIS_0,
c_FU_FIS_1,
c_FU_FIS_2,
c_FU_FIS_3,
c_FU_FIS_4
])

# --- Lower fuel fertile/blanket (LBL)
c_FU_LBL_1 = openmc.Cell( name='c_FU_LBL_1')
c_FU_LBL_2 = openmc.Cell( name='c_FU_LBL_2')
c_FU_LBL_3 = openmc.Cell( name='c_FU_LBL_3')
c_FU_LBL_4 = openmc.Cell( name='c_FU_LBL_4')

c_FU_LBL_1.region = -cyl_FE_fuel
c_FU_LBL_2.region = +cyl_FE_fuel   & -cyl_Clad61_IN
c_FU_LBL_3.region = +cyl_Clad61_IN & -cyl_Clad61_OU
c_FU_LBL_4.region = +cyl_Clad61_OU

c_FU_LBL_1.fill = UOB
c_FU_LBL_2.fill = He
c_FU_LBL_3.fill = SS
c_FU_LBL_4.fill = Na_FU

p_FU_LBL = openmc.Universe()
p_FU_LBL.add_cells([
c_FU_LBL_1,
c_FU_LBL_2,
c_FU_LBL_3,
c_FU_LBL_4
])

# --- Lower gas plenum (LGP)
c_FU_LGP1 = openmc.Cell( name='c_FU_LGP1')
c_FU_LGP2 = openmc.Cell( name='c_FU_LGP2')
c_FU_LGP3 = openmc.Cell( name='c_FU_LGP3')

c_FU_LGP1.region = -cyl_Clad61_IN
c_FU_LGP2.region = +cyl_Clad61_IN & -cyl_Clad61_OU
c_FU_LGP3.region = +cyl_Clad61_OU

c_FU_LGP1.fill = He
c_FU_LGP2.fill = SS
c_FU_LGP3.fill = Na_FU

p_FU_LGP = openmc.Universe()
p_FU_LGP.add_cells([
c_FU_LGP1,
c_FU_LGP2,
c_FU_LGP3
])

# --- Bottop end plug (BEP)
c_FU_BEP1 = openmc.Cell( name='c_FU_BEP1')
c_FU_BEP2 = openmc.Cell( name='c_FU_BEP2')

c_FU_BEP1.region = -cyl_Clad61_OU
c_FU_BEP2.region = +cyl_Clad61_OU

c_FU_BEP1.fill = SS
c_FU_BEP2.fill = Na_FU

p_FU_BEP = openmc.Universe()
p_FU_BEP.add_cells([
c_FU_BEP1,
c_FU_BEP2
])

# --- Na pins
# Outlet Na
c_FU_NOU = openmc.Cell( name='c_FU_NOU')
c_FU_NOU.fill = Na_FU
p_FU_NOU = openmc.Universe()
p_FU_NOU.add_cells([c_FU_NOU])

# Na in  fissile
c_FU_NFI = openmc.Cell( name='c_FU_NFI')
c_FU_NFI.fill = Na_FU
p_FU_NFI = openmc.Universe()
p_FU_NFI.add_cells([c_FU_NFI])

# Na in  fertile
c_FU_NFE = openmc.Cell( name='c_FU_NFE')
c_FU_NFE.fill = Na_FU
p_FU_NFE = openmc.Universe()
p_FU_NFE.add_cells([c_FU_NFE])

# Inlet Na
c_FU_NIN = openmc.Cell( name='c_FU_NIN')
c_FU_NIN.fill = Na_FU
p_FU_NIN = openmc.Universe()
p_FU_NIN.add_cells([c_FU_NIN])


# --- FUEL ASSEMBLY LATTICES
#
# 11. Head                26.00 cm
# 10. Upper shield        44.00 cm
#  9. Upper connector      6.00 cm
# ------ Fuel pin top ------------
#  8. Top end plug         2.00 cm
#  7. Spring               4.50 cm
#  6. Upper blanket       10.00 cm
#  5. Fissile             45.00 cm
#  4. Lower blanket       25.00 cm
#  3. Lower gas plenum    45.00 cm
#  2. Bottom end plug      3.50 cm
# ------ Fuel pin bottom ---------
#  1. Lower connector     10.00 cm


# -------------------------------------------------------
# --- HEAD
# -------------------------------------------------------
c_l_FU_HEA_01 = openmc.Cell( name='c_l_FU_HEA_01')
c_l_FU_HEA_02 = openmc.Cell( name='c_l_FU_HEA_02')
c_l_FU_HEA_03 = openmc.Cell( name='c_l_FU_HEA_03')

c_l_FU_HEA_01.region =  hex_HEA_IN
c_l_FU_HEA_02.region = ~hex_HEA_IN & hex_WR_OU
c_l_FU_HEA_03.region = ~hex_WR_OU

c_l_FU_HEA_01.fill = Na_FU
c_l_FU_HEA_02.fill = Ti316
c_l_FU_HEA_03.fill = Na_FU

u_FU_HEA = openmc.Universe()
u_FU_HEA.add_cells([c_l_FU_HEA_01, c_l_FU_HEA_02, c_l_FU_HEA_03])

# -------------------------------------------------------
# --- Upper shield (USH)
# -------------------------------------------------------
c_l_FU_USH_01 = openmc.Cell( name='c_l_FU_USH_01')
c_l_FU_USH_02 = openmc.Cell( name='c_l_FU_USH_02')
c_l_FU_USH_03 = openmc.Cell( name='c_l_FU_USH_03')

c_l_FU_USH_01.region = -cyl_USH_hole
c_l_FU_USH_02.region =  hex_WR_OU & +cyl_USH_hole
c_l_FU_USH_03.region = ~hex_WR_OU

c_l_FU_USH_01.fill = Na_FU
c_l_FU_USH_02.fill = Ti316
c_l_FU_USH_03.fill = Na_FU

u_FU_USH = openmc.Universe()
u_FU_USH.add_cells([c_l_FU_USH_01, c_l_FU_USH_02, c_l_FU_USH_03])

# -------------------------------------------------------
# --- Upper connector (UCN)
# -------------------------------------------------------
c_l_FU_UCN_01 = openmc.Cell( name='c_l_FU_UCN_01')
c_l_FU_UCN_02 = openmc.Cell( name='c_l_FU_UCN_02')
c_l_FU_UCN_03 = openmc.Cell( name='c_l_FU_UCN_03')

c_l_FU_UCN_01.region =  hex_UCN_IN
c_l_FU_UCN_02.region =  hex_WR_OU & ~hex_UCN_IN
c_l_FU_UCN_03.region = ~hex_WR_OU

c_l_FU_UCN_01.fill = Na_FU
c_l_FU_UCN_02.fill = Ti316
c_l_FU_UCN_03.fill = Na_FU

u_FU_UCN = openmc.Universe()
u_FU_UCN.add_cells([c_l_FU_UCN_01, c_l_FU_UCN_02, c_l_FU_UCN_03])

# -------------------------------------------------------
# --- Top end plug (TEP)
# -------------------------------------------------------
l_FU_TEP = openmc.HexLattice()
l_FU_TEP.center = [0., 0.]
l_FU_TEP.pitch  = [ 0.695]
l_FU_TEP.universes = \
       [ [p_FU_TEP]*24, [p_FU_TEP]*18, [p_FU_TEP]*12, [p_FU_TEP]*6, [p_FU_TEP] ]
l_FU_TEP.outer  = p_FU_NOU

c_l_FU_TEP_01 = openmc.Cell( name='c_l_FU_TEP_01')
c_l_FU_TEP_02 = openmc.Cell( name='c_l_FU_TEP_02')
c_l_FU_TEP_03 = openmc.Cell( name='c_l_FU_TEP_03')

c_l_FU_TEP_01.region =  hex_WR_IN
c_l_FU_TEP_02.region =  hex_WR_OU & ~hex_WR_IN
c_l_FU_TEP_03.region = ~hex_WR_OU

c_l_FU_TEP_01.fill = l_FU_TEP
c_l_FU_TEP_02.fill = Ti316
c_l_FU_TEP_03.fill = Na_FU

u_FU_TEP = openmc.Universe()
u_FU_TEP.add_cells([c_l_FU_TEP_01, c_l_FU_TEP_02, c_l_FU_TEP_03])

# -------------------------------------------------------
# --- Spring (SPR)
# -------------------------------------------------------
l_FU_SPR = openmc.HexLattice()
l_FU_SPR.center = [0., 0.]
l_FU_SPR.pitch  = [ 0.695]
l_FU_SPR.universes = \
       [ [p_FU_SPR]*24, [p_FU_SPR]*18, [p_FU_SPR]*12, [p_FU_SPR]*6, [p_FU_SPR] ]
l_FU_SPR.outer  = p_FU_NOU

c_l_FU_SPR_01 = openmc.Cell( name='c_l_FU_SPR_01')
c_l_FU_SPR_02 = openmc.Cell( name='c_l_FU_SPR_02')
c_l_FU_SPR_03 = openmc.Cell( name='c_l_FU_SPR_03')

c_l_FU_SPR_01.region =  hex_WR_IN
c_l_FU_SPR_02.region =  hex_WR_OU & ~hex_WR_IN
c_l_FU_SPR_03.region = ~hex_WR_OU

c_l_FU_SPR_01.fill = l_FU_SPR
c_l_FU_SPR_02.fill = Ti316
c_l_FU_SPR_03.fill = Na_FU

u_FU_SPR = openmc.Universe()
u_FU_SPR.add_cells([c_l_FU_SPR_01, c_l_FU_SPR_02, c_l_FU_SPR_03])

# -------------------------------------------------------
# --- Upper fuel fertile/blanket (UBL)
# -------------------------------------------------------
l_FU_UBL = openmc.HexLattice()
l_FU_UBL.center = [0., 0.]
l_FU_UBL.pitch  = [ 0.695]
l_FU_UBL.universes = \
       [ [p_FU_UBL]*24, [p_FU_UBL]*18, [p_FU_UBL]*12, [p_FU_UBL]*6, [p_FU_UBL] ]
l_FU_UBL.outer  = p_FU_NFE

c_l_FU_UBL_01 = openmc.Cell( name='c_l_FU_UBL_01')
c_l_FU_UBL_02 = openmc.Cell( name='c_l_FU_UBL_02')
c_l_FU_UBL_03 = openmc.Cell( name='c_l_FU_UBL_03')

c_l_FU_UBL_01.region =  hex_WR_IN
c_l_FU_UBL_02.region =  hex_WR_OU & ~hex_WR_IN
c_l_FU_UBL_03.region = ~hex_WR_OU

c_l_FU_UBL_01.fill = l_FU_UBL
c_l_FU_UBL_02.fill = Ti316
c_l_FU_UBL_03.fill = Na_FU

u_FU_UBL = openmc.Universe()
u_FU_UBL.add_cells([c_l_FU_UBL_01, c_l_FU_UBL_02, c_l_FU_UBL_03])

# -------------------------------------------------------
# --- Fuel fissile (FIS)
# -------------------------------------------------------
l_FU_FIS = openmc.HexLattice()
l_FU_FIS.center = [0., 0.]
l_FU_FIS.pitch  = [ 0.695]
l_FU_FIS.universes = \
       [ [p_FU_FIS]*24, [p_FU_FIS]*18, [p_FU_FIS]*12, [p_FU_FIS]*6, [p_FU_FIS] ]
l_FU_FIS.outer  = p_FU_NFI

c_l_FU_FIS_01 = openmc.Cell( name='c_l_FU_FIS_01')
c_l_FU_FIS_02 = openmc.Cell( name='c_l_FU_FIS_02')
c_l_FU_FIS_03 = openmc.Cell( name='c_l_FU_FIS_03')

c_l_FU_FIS_01.region =  hex_WR_IN
c_l_FU_FIS_02.region =  hex_WR_OU & ~hex_WR_IN
c_l_FU_FIS_03.region = ~hex_WR_OU

c_l_FU_FIS_01.fill = l_FU_FIS
c_l_FU_FIS_02.fill = Ti316
c_l_FU_FIS_03.fill = Na_FU

u_FU_FIS = openmc.Universe()
u_FU_FIS.add_cells([c_l_FU_FIS_01, c_l_FU_FIS_02, c_l_FU_FIS_03])

# -------------------------------------------------------
# --- Lower fuel fertile/blanket (LBL)
# -------------------------------------------------------
l_FU_LBL = openmc.HexLattice()
l_FU_LBL.center = [0., 0.]
l_FU_LBL.pitch  = [ 0.695]
l_FU_LBL.universes = \
       [ [p_FU_LBL]*24, [p_FU_LBL]*18, [p_FU_LBL]*12, [p_FU_LBL]*6, [p_FU_LBL] ]
l_FU_LBL.outer  = p_FU_NFE

c_l_FU_LBL_01 = openmc.Cell( name='c_l_FU_LBL_01')
c_l_FU_LBL_02 = openmc.Cell( name='c_l_FU_LBL_02')
c_l_FU_LBL_03 = openmc.Cell( name='c_l_FU_LBL_03')

c_l_FU_LBL_01.region =  hex_WR_IN
c_l_FU_LBL_02.region =  hex_WR_OU & ~hex_WR_IN
c_l_FU_LBL_03.region = ~hex_WR_OU

c_l_FU_LBL_01.fill = l_FU_LBL
c_l_FU_LBL_02.fill = Ti316
c_l_FU_LBL_03.fill = Na_FU

u_FU_LBL = openmc.Universe()
u_FU_LBL.add_cells([c_l_FU_LBL_01, c_l_FU_LBL_02, c_l_FU_LBL_03])

# -------------------------------------------------------
# --- Lower gas plenum (LGP)
# -------------------------------------------------------
l_FU_LGP = openmc.HexLattice()
l_FU_LGP.center = [0., 0.]
l_FU_LGP.pitch  = [ 0.695]
l_FU_LGP.universes = \
       [ [p_FU_LGP]*24, [p_FU_LGP]*18, [p_FU_LGP]*12, [p_FU_LGP]*6, [p_FU_LGP] ]
l_FU_LGP.outer  = p_FU_NIN

c_l_FU_LGP_01 = openmc.Cell( name='c_l_FU_LGP_01')
c_l_FU_LGP_02 = openmc.Cell( name='c_l_FU_LGP_02')
c_l_FU_LGP_03 = openmc.Cell( name='c_l_FU_LGP_03')

c_l_FU_LGP_01.region =  hex_WR_IN
c_l_FU_LGP_02.region =  hex_WR_OU & ~hex_WR_IN
c_l_FU_LGP_03.region = ~hex_WR_OU

c_l_FU_LGP_01.fill = l_FU_LGP
c_l_FU_LGP_02.fill = Ti316
c_l_FU_LGP_03.fill = Na_FU

u_FU_LGP = openmc.Universe()
u_FU_LGP.add_cells([c_l_FU_LGP_01, c_l_FU_LGP_02, c_l_FU_LGP_03])

# -------------------------------------------------------
# --- Bottop end plug (BEP)
# -------------------------------------------------------
l_FU_BEP = openmc.HexLattice()
l_FU_BEP.center = [0., 0.]
l_FU_BEP.pitch  = [ 0.695]
l_FU_BEP.universes = \
       [ [p_FU_BEP]*24, [p_FU_BEP]*18, [p_FU_BEP]*12, [p_FU_BEP]*6, [p_FU_BEP] ]
l_FU_BEP.outer  = p_FU_NIN

c_l_FU_BEP_01 = openmc.Cell( name='c_l_FU_BEP_01')
c_l_FU_BEP_02 = openmc.Cell( name='c_l_FU_BEP_02')
c_l_FU_BEP_03 = openmc.Cell( name='c_l_FU_BEP_03')

c_l_FU_BEP_01.region =  hex_WR_IN
c_l_FU_BEP_02.region =  hex_WR_OU & ~hex_WR_IN
c_l_FU_BEP_03.region = ~hex_WR_OU

c_l_FU_BEP_01.fill = l_FU_BEP
c_l_FU_BEP_02.fill = Ti316
c_l_FU_BEP_03.fill = Na_FU

u_FU_BEP = openmc.Universe()
u_FU_BEP.add_cells([c_l_FU_BEP_01, c_l_FU_BEP_02, c_l_FU_BEP_03])

# -------------------------------------------------------
# --- Lower connector (LCN)
# -------------------------------------------------------
c_l_FU_LCN_01 = openmc.Cell( name='c_l_FU_LCN_01')
c_l_FU_LCN_02 = openmc.Cell( name='c_l_FU_LCN_02')
c_l_FU_LCN_03 = openmc.Cell( name='c_l_FU_LCN_03')

c_l_FU_LCN_01.region =  hex_LCN_IN
c_l_FU_LCN_02.region =  hex_WR_OU & ~hex_LCN_IN
c_l_FU_LCN_03.region = ~hex_WR_OU

c_l_FU_LCN_01.fill = Na_FU
c_l_FU_LCN_02.fill = Ti316
c_l_FU_LCN_03.fill = Na_FU

u_FU_LCN = openmc.Universe()
u_FU_LCN.add_cells([c_l_FU_LCN_01, c_l_FU_LCN_02, c_l_FU_LCN_03])

# -------------------------------------------------------
# --- 3D fuel assembly
# -------------------------------------------------------
#

# 3D Universe - Fuel SA
c_FU_OUT = openmc.Cell( name='c_FU_OUT')
c_FU_HEA = openmc.Cell( name='c_FU_HEA')
c_FU_USH = openmc.Cell( name='c_FU_USH')
c_FU_UCN = openmc.Cell( name='c_FU_UCN')
c_FU_TEP = openmc.Cell( name='c_FU_TEP')
c_FU_SPR = openmc.Cell( name='c_FU_SPR')
c_FU_UBL = openmc.Cell( name='c_FU_UBL')
c_FU_FIS = openmc.Cell( name='c_FU_FIS')
c_FU_LBL = openmc.Cell( name='c_FU_LBL')
c_FU_LGP = openmc.Cell( name='c_FU_LGP')
c_FU_BEP = openmc.Cell( name='c_FU_BEP')
c_FU_LCN = openmc.Cell( name='c_FU_LCN')

c_FU_OUT.region =                +pz_FUEL_HEA
c_FU_HEA.region = -pz_FUEL_HEA & +pz_FUEL_USH
c_FU_USH.region = -pz_FUEL_USH & +pz_FUEL_UCN
c_FU_UCN.region = -pz_FUEL_UCN & +pz_FUEL_TEP
c_FU_TEP.region = -pz_FUEL_TEP & +pz_FUEL_SPR
c_FU_SPR.region = -pz_FUEL_SPR & +pz_FUEL_UBL
c_FU_UBL.region = -pz_FUEL_UBL & +pz_FUEL_FIS
c_FU_FIS.region = -pz_FUEL_FIS & +pz_FUEL_LBL
c_FU_LBL.region = -pz_FUEL_LBL & +pz_FUEL_LGP
c_FU_LGP.region = -pz_FUEL_LGP & +pz_FUEL_BEP
c_FU_BEP.region = -pz_FUEL_BEP & +pz_FUEL_LCN
c_FU_LCN.region = -pz_FUEL_LCN

c_FU_OUT.fill = u_FU_HEA
c_FU_HEA.fill = u_FU_HEA
c_FU_USH.fill = u_FU_USH
c_FU_UCN.fill = u_FU_UCN
c_FU_TEP.fill = u_FU_TEP
c_FU_SPR.fill = u_FU_SPR
c_FU_UBL.fill = u_FU_UBL
c_FU_FIS.fill = u_FU_FIS
c_FU_LBL.fill = u_FU_LBL
c_FU_LGP.fill = u_FU_LGP
c_FU_BEP.fill = u_FU_BEP
c_FU_LCN.fill = u_FU_LCN

c_FU_OUT.rotation = [0, 0, 90]
c_FU_HEA.rotation = [0, 0, 90]
c_FU_USH.rotation = [0, 0, 90]
c_FU_UCN.rotation = [0, 0, 90]
c_FU_TEP.rotation = [0, 0, 90]
c_FU_SPR.rotation = [0, 0, 90]
c_FU_UBL.rotation = [0, 0, 90]
c_FU_FIS.rotation = [0, 0, 90]
c_FU_LBL.rotation = [0, 0, 90]
c_FU_LGP.rotation = [0, 0, 90]
c_FU_BEP.rotation = [0, 0, 90]
c_FU_LCN.rotation = [0, 0, 90]

a_FU = openmc.Universe()
a_FU.add_cells([c_FU_OUT,
                c_FU_HEA,
                c_FU_USH,
                c_FU_UCN,
                c_FU_TEP,
                c_FU_SPR,
                c_FU_UBL,
                c_FU_FIS,
                c_FU_LBL,
                c_FU_LGP,
                c_FU_BEP,
                c_FU_LCN ])


#CORE Lattice
l_core = openmc.HexLattice()
l_core.center = [0., 0.]
l_core.pitch  = [6.12525]
l_core.universes = \
       [ [a_FU] ]


l_core.outer = a_OU

cell1000 = openmc.Cell(name='cell1000')

cell1000.region = hexcore & -pz_TOP & +pz_BOT

cell1000.fill = l_core

root = openmc.Universe(name='root universe')
root.add_cells([cell1000])
# Instantiate a Geometry, register the root Universe, and export to XML
geometry = openmc.Geometry(root)
geometry.export_to_xml()

###############################################################################
#                   Exporting to OpenMC settings.xml file
###############################################################################

# Instantiate a Settings object, set all runtime parameters, and export to XML
settings_file = openmc.Settings()
settings_file.batches   = 120  #1050   # sum of active & inactive cycles
settings_file.inactive  = 20   #50
settings_file.particles = 1000 #100000
settings_file.ptables   = True
settings_file.temperature['method']='interpolation'

# Create an initial uniform spatial source distribution over fissionable zones
bounds = [-5.0, -5.0, 120.0, 5.0,  5.0, 120.0]
uniform_dist = openmc.stats.Box(bounds[:3], bounds[3:], only_fissionable=True )
settings_file.source = openmc.source.IndependentSource(space=uniform_dist)

settings_file.export_to_xml()

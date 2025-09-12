!include ../common.i

# compute the inlet mass flux required to get a bulk temperature rise of 160 K,
# for the imposed power of ${power}. We evaluate the specific heat at the average
# of the inlet and outlet temperatures using a correlation.
temperature = ${fparse 0.5 * (outlet_temperature + inlet_temperature)}
dt = ${fparse 2503.3 - temperature}
Cp = ${fparse 7.3898e5 / dt / dt + 3.154e5 / dt + 1.1340e3 + -2.2153e-1 * dt + 1.1156e-4 * dt * dt}
total_mdot = ${fparse power / Cp / (outlet_temperature - inlet_temperature)}

# compute the mass flux by dividing the mass flowrate by the flow area
flow_area = ${fparse sqrt(3)/2 * (duct_inner_flat_to_flat*1e-2)^2 - 61*pi*(outer_clad_diameter*1e-2)^2/4}

mass_flux_in = ${fparse total_mdot / flow_area}

[TriSubChannelMesh]
  [subchannel]
    type = SCMTriSubChannelMeshGenerator
    nrings = 5
    n_cells = 100
    flat_to_flat = ${fparse duct_inner_flat_to_flat * 1e-2}
    heated_length = ${fparse height * 1e-2}
    pin_diameter = ${fparse outer_clad_diameter * 1e-2}
    pitch = ${fparse pin_pitch * 1e-2}
    dwire = ${fparse wire_diameter * 1e-2}
    hwire = ${fparse wire_pitch * 1e-2}
  []
  [fuel_pins]
    type = SCMTriPinMeshGenerator
    input = subchannel
    nrings = 5
    n_cells = 100
    pin_diameter = ${fparse outer_clad_diameter * 1e-2}
    dwire = ${fparse wire_diameter * 1e-2}
    hwire = ${fparse wire_pitch * 1e-2}
    heated_length = ${fparse height * 1e-2}
    pitch = ${fparse pin_pitch * 1e-2}
  []
[]

[AuxVariables]
  [mdot]
    block = subchannel
  []
  [SumWij]
    block = subchannel
  []
  [P]
    block = subchannel
  []
  [DP]
    block = subchannel
  []
  [h]
    block = subchannel
  []
  [T]
    block = subchannel
  []
  [rho]
    block = subchannel
  []
  [S]
    block = subchannel
  []
  [w_perim]
    block = subchannel
  []
  [mu]
    block = subchannel
  []
  [Tpin]
    block = fuel_pins
  []
  [q_prime]
    block = fuel_pins
  []
  [Dpin]
    block = fuel_pins
  []
  [displacement]
    block = fuel_pins
  []
  [q_prime_const]
    family = monomial
    order = constant
    block = fuel_pins
  []
[]

[FluidProperties]
  [sodium]
    type = PBSodiumFluidProperties
  []
[]

[Problem]
  type = TriSubChannel1PhaseProblem
  fp = sodium
  n_blocks = 1
  P_out = ${P_out}
  CT = 1.0
  compute_density = true
  compute_viscosity = true
  compute_power = true
  implicit = true
  segregated = false
  staggered_pressure = false
  monolithic_thermal = false
  P_tol = 1.0e-5
  T_tol = 1.0e-5
[]

[ICs]
  [Dpin_ic]
    type = ConstantIC
    variable = Dpin
    value = ${fparse 1e-2 * outer_clad_diameter}
  []
  [S_IC]
    type = SCMTriFlowAreaIC
    variable = S
  []
  [w_perim_IC]
    type = SCMTriWettedPerimIC
    variable = w_perim
  []
  [q_prime_IC]
    type = ConstantIC
    variable = q_prime_const
    value = ${fparse power/61/(height*1e-2)}
  []
  [T_ic]
    type = ConstantIC
    variable = T
    value = 500
  []
  [P_ic]
    type = ConstantIC
    variable = P
    value = 0.0
  []
  [DP_ic]
    type = ConstantIC
    variable = DP
    value = 0.0
  []
  [Viscosity_ic]
    type = ViscosityIC
    variable = mu
    p = ${P_out}
    T = T
    fp = sodium
  []
  [rho_ic]
    type = RhoFromPressureTemperatureIC
    variable = rho
    p = ${P_out}
    T = T
    fp = sodium
  []
  [h_ic]
    type = SpecificEnthalpyFromPressureTemperatureIC
    variable = h
    p = ${P_out}
    T = T
    fp = sodium
  []
  [mdot_ic]
    type = ConstantIC
    variable = mdot
    value = 0.0
  []
  [Tpin_ic]
    type = ConstantIC
    variable = Tpin
    value = 560
  []
[]

[AuxKernels]
  [T_in_bc]
    type = ConstantAux
    variable = T
    boundary = inlet
    value = ${inlet_temperature}
    execute_on = 'timestep_begin'
  []
  [mdot_in_bc]
    type = SCMMassFlowRateAux
    variable = mdot
    boundary = inlet
    area = S
    mass_flux = ${mass_flux_in}
    execute_on = 'timestep_begin'
  []
  [q_prime_ak]
    type = ProjectionAux
    variable = q_prime
    v = q_prime_const
    execute_on = 'initial timestep_begin'
  []
[]

[Postprocessors]
  [power]
    type = SCMPowerPostprocessor
  []
  [inlet_temp]
    type = SCMPlanarMean
    variable = T
    height = 0.0
  []
  [outlet_temp]
    type = SCMPlanarMean
    variable = T
    height = ${fparse height * 1e-2}
  []
[]

[Executioner]
  type = Steady
[]

[Outputs]
  exodus = true
[]

[MultiApps]
  [viz]
    type = FullSolveMultiApp
    input_files = 'viz.i'
    execute_on = 'timestep_end'
  []
[]

[Transfers]
  [transfer]
    type = SCMSolutionTransfer
    to_multi_app = viz
    variable = 'mdot P T rho S'
  []
[]

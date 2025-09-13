!include ../common.i

[Mesh]
  [file]
    type = FileMeshGenerator
    file = ../meshes/solid_in.e
  []
  [delete_coolant]
    type = BlockDeletionGenerator
    input = file
    block = '3 1000 1002'
  []
[]

[Variables]
  [T]
  []
[]

[AuxVariables]
  # Surface temperature of the cladding (computed by subchannel)
  [T_wall]
    initial_condition = 500.0
    block = '2'
  []

  # Heat source (from openmc)
  [heat_source]
    family = monomial
    order = constant
    initial_condition = 1e8
    block = '1'
  []

  # linear heat rate, postprocessed to send to subchannel
  [q_prime]
    family = MONOMIAL
    order = CONSTANT
    initial_condition = 0.0
    block = '1'
  []
[]

[AuxKernels]
  [q_prime]
    type = SpatialUserObjectAux
    variable = q_prime
    user_object = q_prime_uo
    block = '1'
  []
[]

[Kernels]
  [heat_conduction]
    type = HeatConduction
    variable = T
  []

  [heat_source_fuel]
    type = CoupledForce
    variable = T
    v = heat_source
    block = '1'
  []
[]

[Materials]
   [k_helium]
    type = GenericConstantMaterial
    prop_names = 'thermal_conductivity'
    prop_values = '1.5'
    block = '0'
  []
   [k_fuel]
    type = GenericConstantMaterial
    prop_names = 'thermal_conductivity'
    prop_values = '2.0'
    block = '1'
  []
   [k_clad]
    type = GenericConstantMaterial
    prop_names = 'thermal_conductivity'
    prop_values = '10.0'
    block = '2'
  []
   [k_duct]
    type = GenericConstantMaterial
    prop_names = 'thermal_conductivity'
    prop_values = '10.0'
    block = '1001'
  []
[]

[BCs]
  [cladding_outer_bc]
    type = MatchedValueBC
    variable = T
    v = T_wall
    boundary = '7'
  []
  [duct_inner_bc]
    type = DirichletBC
    variable = T
    value = 500
    boundary = '30501'
  []
[]

[Executioner]
  type = Transient
[]

[Postprocessors]
  [max_fuel_temp]
    type = ElementExtremeValue
    variable = T
    block = '1'
  []
  [conduction_power_integral]
    type = ElementIntegralVariablePostprocessor
    variable = heat_source
    block = '1'
    execute_on = 'transfer'
  []
[]

[Outputs]
  exodus = true
[]

[UserObjects]
  [q_prime_uo]
    type = NearestPointLayeredIntegral
    variable = heat_source
    block = '1'
    direction = z
    points_file = 'pin_centers.txt'
    num_layers = ${n_layers}
    execute_on = 'initial timestep_begin'
  []
[]

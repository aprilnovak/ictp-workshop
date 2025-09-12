[Mesh]
  [file]
    type = FileMeshGenerator
    file = ../meshes/solid_in.e
  []
[]

[Problem]
  type = OpenMCCellAverageProblem
  power = ${fparse 65e6 / 79}
  lowest_cell_level = 2
  scaling = 100
  verbose = true
  #temperature_blocks = '0 1 2 1001'

  #normalize_by_global_tally = false

  [Tallies]
    [power]
      type = CellTally
      score = 'kappa_fission'

      #type = MeshTally
      #mesh_template = '../meshes/solid_in.e'
    []
  []
[]

[Executioner]
  type = Transient
  num_steps = 5
[]

[Outputs]
  exodus = true
[]

[MultiApps]
  [conduction]
    type = TransientMultiApp
    input_files = 'conduction.i'
    sub_cycling = true
    execute_on = timestep_end
  []
[]

[Transfers]
  [power_to_conduction]
    type = MultiAppGeneralFieldNearestLocationTransfer
    to_multi_app = conduction
    source_variable = kappa_fission
    variable = heat_source
    from_postprocessors_to_be_preserved = openmc_power_integral
    to_postprocessors_to_be_preserved = conduction_power_integral
  []
[]

[Postprocessors]
  [openmc_power_integral]
    type = ElementIntegralVariablePostprocessor
    variable = kappa_fission
    execute_on = 'transfer timestep_end'
  []
[]

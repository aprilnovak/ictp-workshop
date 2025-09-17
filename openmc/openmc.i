!include ../common.i

[Mesh]
  [file]
    type = FileMeshGenerator
    file = ../meshes/mesh_in.e
  []
[]

[Problem]
  type = OpenMCCellAverageProblem
  power = ${power}
  lowest_cell_level = 2
  scaling = 100
  verbose = true
  normalize_by_global_tally = false

  temperature_blocks = 'helium fuel clad sodium'
  density_blocks = 'sodium'
  initial_properties = xml

  [Tallies]
    [power]
      type = CellTally
      score = 'kappa_fission'

      #type = MeshTally
      #mesh_template = '../meshes/mesh_in.e'
    []
  []
[]

[ICs]
  [temp]
    type = ConstantIC
    variable = temp
    value = 700.0
  []
  [density]
    type = ConstantIC
    variable = density
    value = 9000
  []
[]

[Executioner]
  type = Steady
[]

[Outputs]
  exodus = true
[]

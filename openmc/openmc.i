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
  normalize_by_global_tally = false

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
  type = Steady
[]

[Outputs]
  exodus = true
[]

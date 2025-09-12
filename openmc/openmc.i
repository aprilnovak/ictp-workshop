[Mesh]
  [file]
    type = FileMeshGenerator
    file = ../meshes/solid_in.e
  []
[]

#[ICs]
#  [temperature]
#    type = ConstantIC
#    variable = temp
#    value = 600
#  []
#[]

[Problem]
  type = OpenMCCellAverageProblem
  power = ${fparse 65e6 / 79}
  lowest_cell_level = 2
 # temperature_blocks = '1 2 3 1000 1001 1002'
  scaling = 100
  verbose = true

  [Tallies]
    [power]
      type = CellTally
      block = '1'
      score = 'kappa_fission'
    []
  []
[]

[Executioner]
  type = Steady
[]

[Outputs]
  exodus = true
[]

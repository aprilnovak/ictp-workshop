!include ../common.i

[Mesh]
  [file]
    type = FileMeshGenerator
    file = ../meshes/mesh_in.e
  []
[]

[Problem]

  [Tallies]
  []
[]

[ICs]
[]

[AuxVariables]
[]

[AuxKernels]
[]

[Executioner]
  type = Steady
[]

[Outputs]
  exodus = true
[]

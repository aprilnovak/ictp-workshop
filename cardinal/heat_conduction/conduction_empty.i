!include ../common.i

[Mesh]
  [file]
    type = FileMeshGenerator
    file = ../meshes/mesh_in.e
  []
  [delete_coolant]
    type = BlockDeletionGenerator
    input = file
    block = 'sodium'
  []
[]

[Variables]
[]

[Kernels]
[]

[Materials]
[]

[AuxVariables]
[]

[BCs]
[]

[AuxKernels]
  [q_prime]
    type = SpatialUserObjectAux
    variable = q_prime
    user_object = q_prime_uo
    block = 'fuel'
  []
[]

[UserObjects]
  [q_prime_uo]
    type = NearestPointLayeredIntegral
    variable = heat_source
    block = 'fuel'
    direction = z
    points_file = '../pin_centers.txt'
    num_layers = ${n_layers}
  []
[]

[Executioner]
  type = Steady
[]

[Outputs]
  exodus = true
[]

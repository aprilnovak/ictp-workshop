!include ../common.i

[Mesh]
  [subchannel]
    type = SCMDetailedTriSubChannelMeshGenerator
    nrings = 5
    n_cells = 100
    flat_to_flat = 0.2
    heated_length = ${fparse height * 1e-2}
    pin_diameter = ${fparse outer_clad_diameter * 1e-2}
    pitch = ${fparse pin_pitch * 1e-2}
  []
[]

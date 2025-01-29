### Range of n, h, g, d for random circuits

=== old ===

random_circuit_d_const ->
n -> (1, 30)
d -> (1, 30)
g -> arbitrary
h -> arbitrary

random_circuit_g_const ->
n -> (1, 30)
g -> (1, 500)
d -> arbitrary
h -> arbitrary

random_circuit_h_const ->
n -> (1, 30)
h -> (1, 30)
g -> arbitrary
d -> arbitrary


For PolySim -> limit `h` to 25
For DDSIM and Aer -> limit `n` to 25

=== new ===

random_circuit_d_const ->
n -> (1, 15)
d -> (1, 15)
g -> arbitrary
h -> arbitrary

random_circuit_g_const ->
n -> (1, 15)
g -> (1, 300)
d -> arbitrary
h -> arbitrary

random_circuit_h_const ->
n -> (1, 15)
h -> (1, 15)
g -> arbitrary
d -> arbitrary


For PolySim -> limit `h` to 15
For DDSIM and Aer -> limit `n` to 15
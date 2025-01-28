from discopy.monoidal import Ty, Box, Layer, Diagram

x, y, z = Ty('x'), Ty('y'), Ty('z')
f, g, h = Box('f', x, y @ z), Box('g', y, z), Box('h', z, z)

assert f >> g @ h == Diagram(
    dom=x, cod=z @ z, inside=(
        Layer(Ty(), f, Ty()),
        Layer(Ty(), g, z),
        Layer(z,    h, Ty())))

(f >> g @ h).draw()
from discopy import monoidal, python
from discopy.cat import factory, Category

@factory  # Ensure that composition of circuits remains a circuit.
class Circuit(monoidal.Diagram):
    ty_factory = monoidal.PRO  # Use natural numbers as objects.

    def __call__(self, *bits):
        F = monoidal.Functor(
            ob=lambda _: bool, ar=lambda f: f.data,
            cod=Category(python.Ty, python.Function))
        return F(self)(*bits)

class Gate(monoidal.Box, Circuit):
    """A gate is just a box in a circuit with a function as data."""

NAND = Gate("NAND", 2, 1, data=lambda x, y: not (x and y))
COPY = Gate("COPY", 1, 2, data=lambda x: (x, x))

XOR = COPY @ COPY >> 1 @ (NAND >> COPY) @ 1 >> NAND @ NAND >> NAND
CNOT = COPY @ 1 >> 1 @ XOR
NOTC = 1 @ COPY >> XOR @ 1
SWAP = CNOT >> NOTC >> CNOT  # Exercise: Find a cheaper SWAP circuit!

assert all(SWAP(x, y) == (y, x) for x in [True, False]
                                for y in [True, False])

SWAP.draw(figsize=(4, 8), wire_labels=False)

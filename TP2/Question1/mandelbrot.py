# Calcul de l'ensemble de Mandelbrot en python
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm


@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius:  float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex, smooth=False) -> int | float:
        z: complex
        iter: int

        # Vérification si le complexe appartient à une zone de convergence connue
        if c.real * c.real + c.imag * c.imag < 0.0625:
            return self.max_iterations
        if (c.real + 1) * (c.real + 1) + c.imag * c.imag < 0.0625:
            return self.max_iterations

        # Appartenance à la cardioïde {(1/4,0),1/2(1-cos(theta))}
        if -0.75 < c.real < 0.5:
            ct = c.real - 0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5 * (1 - ct.real / max(ctnrm2, 1.E-14)):
                return self.max_iterations

        # Itération principale
        z = 0
        for iter in range(self.max_iterations):
            z = z * z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z))) / log(2)
                return iter
        return self.max_iterations


# Paramètres de l'image et du calcul
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

scaleX = 3.0 / width
scaleY = 2.25 / height
convergence = np.empty((width, height), dtype=np.double)

# Calcul de l'ensemble de Mandelbrot :
start_time = time()
for y in range(height):
    for x in range(width):
        c = complex(-2.0 + scaleX * x, -1.125 + scaleY * y)
        convergence[x, y] = mandelbrot_set.convergence(c, smooth=True)
end_time = time()
print(f"Temps du calcul de l'ensemble de Mandelbrot : {end_time - start_time:.2f} s")

# Création et sauvegarde de l'image
start_time = time()
image = Image.fromarray(np.uint8(matplotlib.cm.plasma(convergence.T) * 255))
image.save("mandelbrot_output.png")  # Sauvegarde de l'image
end_time = time()
print(f"Temps de constitution et sauvegarde de l'image : {end_time - start_time:.2f} s")

# Affichage de l'image
image.show()

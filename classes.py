from math import pi

class Viga():
    def __init__(self):
        self.base = 0
        self.altura = 0
        self.mk = 0
        self.fck = 0
        self.aco = 50
        self.centroide = 0

    def sigmacd(self):
        return 0.85 * self.fck / 140

    def fyd(self):
        return self.aco / 11.5

    def mi(self):
        altura_util = self.altura - self.centroide
        return (140 * self.mk) / (self.sigmacd() * (altura_util ** 2) * self.base)

    def omega(self):
        return 1 - (1 - 2 * self.mi()) ** (1/2)

    def ks(self):
        altura_util = self.altura - self.centroide
        return (self.sigmacd() / self.fyd()) * self.base * altura_util

    def area_aco(self):
        return self.ks() * self.omega()

    def barras_aco(self, bitola):
        barras = 400 * self.area_aco() / (pi * bitola ** 2)
        if barras > round(barras):
            return round(barras+1, 0)
        else:
            return round(barras, 0)
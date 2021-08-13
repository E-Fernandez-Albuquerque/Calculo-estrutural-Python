from math import pi

class Viga_cisalhamento():
    def __init__(self):
        self.base = 0
        self.altura = 0
        self.vk = 0
        self.fck = 0
        self.aco = 50
        self.centroide = 5

    def twu(self):
        return 0.27 * (1 - self.fck/250) * (10 * self.fck / 1.4)

    def twd(self):
        return 1.4 * self.vk / (self.base * (self.altura - self.centroide))

    def asw(self):
        return (self.base * (100 * self.twd() - 9 * 30**(2/3))) / 392

    def espacamento(self, estribo):
        return (pi * estribo**2) / (2 * self.asw())


class Viga_flexao():
    def __init__(self):
        self.base = 0
        self.altura = 0
        self.mk = 0
        self.fck = 0
        self.aco = 50
        self.centroide = 5
        self.cobrimento = 3

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
        if round(barras) > barras:
            barras = round(barras, 0)
        else:
            barras = round(barras + 1, 0)
        return barras

    def camadas_armadura(self, bitola, diametro_brita, diametro_estribo):
        nbar = self.barras_aco(bitola)
        nbar_1cam = nbar
        e_hor = (self.base - 2 * (self.cobrimento + diametro_estribo/10) - nbar_1cam * bitola/10) / (nbar_1cam - 1)
        while e_hor <= diametro_brita:
            nbar_1cam -= 1
            e_hor = (self.base - 2 * (self.cobrimento + diametro_estribo/10) - nbar_1cam * bitola / 10) / (nbar_1cam - 1)
        if round(nbar / nbar_1cam) < nbar / nbar_1cam:
            ncam = round(nbar / nbar_1cam) + 1
        else:
            ncam = round(nbar / nbar_1cam)

        return [nbar_1cam, e_hor, ncam]

    # def calcular_centroide(self, bitola, diametro_brita, diametro_estribo):
    #     camadas = self.camadas_armadura(bitola, diametro_brita, diametro_estribo)[2]
    #     centroide = 0
    #     if camadas == 1:
    #         centroide = self.cobrimento + diametro_estribo/10 + bitola/20
    #     elif camadas == 2:
    #         n1 = self.camadas_armadura(20, 3, 5)[0] * (self.cobrimento + diametro_estribo/10 + bitola/10 + 2 +
    #                                                    bitola/20) * bitola/10
    #         n2 = (self.barras_aco(20) - self.camadas_armadura(20, 3, 5)[0]) * (n1 + bitola/20 + 2 + bitola/20) * \
    #              bitola/10
    #
    #         d = self.barras_aco(20) * bitola/10
    #         print(n1, n2, d)
    #         centroide = (n1 + n2) / d
    #     return centroide

class Laje_macica_flexao():
    def __init__(self):
        self.espessura = 0
        self.base = 100
        self.fck = 0
        self.mx = 0
        self.my = 0
        self.mxe = 0
        self.mye = 0
        self.centroide = 3
        self.aco = 0

    def sigmacd(self):
        return 0.85 * self.fck / 1.4

    def fyd(self):
        return self.aco / 11.5

    def mi(self):
        mix = 0.14 * self.mx / (self.sigmacd() * self.base * (self.espessura - self.centroide) ** 2)
        miy = 0.14 * self.my / (self.sigmacd() * self.base * (self.espessura - self.centroide) ** 2)
        mixe = 0.14 * abs(self.mxe) / (self.sigmacd() * self.base * (self.espessura - self.centroide) ** 2)
        miye = 0.14 * abs(self.mye) / (self.sigmacd() * self.base * (self.espessura - self.centroide) ** 2)
        return [mix, miy, mixe, miye]

    def omega(self):
        wx = 1 - (1 - 2 * self.mi()[0])
        wy = 1 - (1 - 2 * self.mi()[1])
        wxe = 1 - (1 - 2 * self.mi()[2])
        wye = 1 - (1 - 2 * self.mi()[3])
        return [wx, wy, wxe, wye]

    def ks(self):
        return (self.sigmacd() / self.fyd()) * self.base * (self.espessura - self.centroide)

    def area_aco(self):
        asx = self.ks() * self.omega()[0]
        asy = self.ks() * self.omega()[1]
        asxe = self.ks() * self.omega()[2]
        asye = self.ks() * self.omega()[3]
        return [asx, asy, asxe, asye]

    def espacamento(self, bitola):
        ex = pi * bitola ** 2 / (4 * self.area_aco()[0])
        ey = pi * bitola ** 2 / (4 * self.area_aco()[1])
        exe = pi * bitola ** 2 / (4 * self.area_aco()[2])
        eye = pi * bitola ** 2 / (4 * self.area_aco()[3])
        return [ex, ey, exe, eye]


class Sapata_isolada_flexao():
    def __init__(self):
        self.tensao_solo = 0
        self.carga_compressao = 0
        self.fck = 0
        self.altura_pilar = 0
        self.base_pilar = 0
        self.cobrimento = 5
        self.centroide = 5
        self.aco = 50
        self.mk = 0
        self.A = 0
        self.B = 0
        self.T_max = 0
        self.t_med = 0
        self.t_min = 0
        self.Lx = 0
        self.Ly = 0
        self.H = 0
        self.h = 0

    def dimensao_inicial(self):
        ab = (1.1 * self.carga_compressao / self.tensao_solo) ** (1/2)
        if ab > round(ab, 1):
            return round(ab + 0.1, 1)
        else:
            return round(ab, 1)

    def dimensao_final(self):
        self.A = round(self.dimensao_inicial() - (self.altura_pilar - self.base_pilar) / 2, 1)
        self.B = round(self.dimensao_inicial() + (self.altura_pilar - self.base_pilar) / 2, 1)
        return [self.A, self.B]

    def balanco(self):
        self.Lx = (self.dimensao_final()[0] - self.base_pilar) / 2
        self.Ly = (self.dimensao_final()[1] - self.altura_pilar) / 2
        return [round(self.Lx, 2), round(self.Ly, 2)]

    def tensoes(self):
        self.T_max = (1.1 * self.carga_compressao / (self.A * self.B)) + \
                (6 * self.mk / (self.A * self.B ** 2))

        self.T_med = (1.1 * self.carga_compressao / (self.A * self.B))

        self.T_min =(1.1 * self.carga_compressao / (self.A * self.B)) - \
                (6 * self.mk / (self.A * self.B ** 2))
        if self.T_max > 1.3 * self.tensao_solo or self.T_med > self.tensao_solo or self.T_min < 0:
            self.A += 0.1
            self.B += 0.1
            self.tensoes()
        return [round(self.T_max, 2), round(self.T_med, 2), round(self.T_min, 2)]

    def tensao_dimensionamento(self):
        return (self.carga_compressao / (self.A * self.B)) + (3 * self.mk / (self.A * self.B ** 2))

    def alturas(self):
        Hx = 100 * self.Lx / 1.5
        Hy = 100 * self.Ly / 1.5
        if Hx > Hy:
            self.H = round(Hx, 0)
        else:
            self.H = round(Hy, 0)

        while self.H % 5 != 0:
            self.H += 1

        if self.H / 3 > 20:
            self.h = round(self.H / 3, 0)
        else:
            self.h = 20
        while self.h % 5 != 0:
            self.h += 1

        h_util = self.H - self.centroide
        return [self.H, self.h, h_util]

    def comprimento_flexao(self):
        x = (2 * self.A - self.base_pilar) / 4
        y = (2 * self.B - self.altura_pilar) / 4
        return [x, y]

    def momentos_fletores(self):
        mx = round((self.tensao_dimensionamento() * self.comprimento_flexao()[0] ** 2) / 2, 2)
        my = round((self.tensao_dimensionamento() * self.comprimento_flexao()[1] ** 2) / 2, 2)
        return [mx, my]

    def area_aco(self):
        Asx = round(1.4 * self.momentos_fletores()[0] / ((self.aco / 11.5) * 0.87 * self.comprimento_flexao()[0]) * \
                    self.B, 2)
        Asy = round(1.4 * self.momentos_fletores()[1] / ((self.aco / 11.5) * 0.87 * self.comprimento_flexao()[1]) * \
                    self.A, 2)
        return [Asx, Asy]

    def armaduras(self, bitolax, bitolay):
        nbarx, nbary = 0, 0
        nx = 400 * self.area_aco()[0] / (pi * bitolax ** 2)
        if nx > round(nx):
            nbarx = round(nx+1, 0)
        else:
            nbarx = round(nx, 0)
        ny = 400 * self.area_aco()[1] / (pi * bitolay ** 2)
        if ny > round(ny):
            nbary = round(ny+1, 0)
        else:
            nbary = round(ny, 0)
        return [nbarx, nbary]

viga = Viga_flexao()
viga.base = 18
viga.altura = 65
viga.mk = 14
viga.fck = 30
viga.aco = 50
#cobrimento 3, estribo 5
print(viga.barras_aco(20))
print(viga.camadas_armadura(20, 3, 5))
print(viga.calcular_centroide(20, 3, 5))

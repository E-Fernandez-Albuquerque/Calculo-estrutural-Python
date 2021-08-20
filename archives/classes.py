from math import pi, sqrt


class VigaCisalhamento():
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

    def verificar(self, estribo):
        pass


class VigaFlexao():
    def __init__(self):
        self.base = 0
        self.altura = 0
        self.mk = 0
        self.fck = 0
        self.aco = 50
        self.centroide = 5
        self.cobrimento = 3
        self.altura_util = 0

    def calcular_altura_util(self):
        self.altura_util = self.altura - self.centroide

    def sigmacd(self):
        return round(0.85 * self.fck / 140, 4)

    def fyd(self):
        return round(self.aco / 11.5, 3)

    def mi(self):
        self.calcular_altura_util()
        return round((140 * self.mk) / (self.sigmacd() * (self.altura_util ** 2) * self.base), 4)

    def omega(self):
        return round(1 - sqrt((1 - 2 * self.mi())), 3)

    def ks(self):
        return round((self.sigmacd() / self.fyd()) * self.base * self.altura_util, 2)

    def area_aco(self):
        return self.ks() * self.omega()

    def barras_aco(self, bitola_t, bitola_c=10):
        if self.mi() < 0.3:
            barras = 400 * self.area_aco() / (pi * bitola_t ** 2)
            if round(barras) > barras:
                nbar = round(barras, 0)
            else:
                nbar = round(barras + 1, 0)
            return nbar
        else:
            barrasT = 400 * self.aco_tracionado() / (pi * bitola_t ** 2)
            barrasC = 400 * self.aco_comprimido() / (pi * bitola_c ** 2)
            if round(barrasT) > barrasT:
                nbarT = round(barrasT, 0)
            else:
                nbarT = round(barrasT + 1, 0)
            if round(barrasC) > barrasC:
                nbarC = round(barrasC, 0)
            else:
                nbarC = round(barrasC + 1, 0)
            return [nbarT, nbarC]

    def camadas_armadura(self, bitola_t, bitola_c, diametro_brita, diametro_estribo):
        if self.mi() < 0.3:
            nbar = self.barras_aco(bitola_t)
            nbar_1cam = nbar
            e_hor = (self.base - 2 * (self.cobrimento + diametro_estribo/10) - nbar_1cam * bitola_t / 10) / (nbar_1cam - 1)
            while e_hor <= diametro_brita:
                nbar_1cam -= 1
                e_hor = (self.base - 2 * (self.cobrimento + diametro_estribo/10) - nbar_1cam * bitola_t / 10) / (nbar_1cam - 1)
            if round(nbar / nbar_1cam) < nbar / nbar_1cam:
                ncam = round(nbar / nbar_1cam) + 1
            else:
                ncam = round(nbar / nbar_1cam)
            return [nbar_1cam, e_hor, ncam]
        else:
            nbarT = self.barras_aco(bitola_t)[0]
            nbarC = self.barras_aco(bitola_c)[1]
            nbarT_1cam = nbarT
            nbarC_1cam = nbarC
            e_horT = (self.base - 2 * (self.cobrimento + diametro_estribo / 10) - nbarT_1cam * bitola_t / 10) / (
                        nbarT_1cam - 1)
            while e_horT <= diametro_brita:
                nbarT_1cam -= 1
                e_horT = (self.base - 2 * (self.cobrimento + diametro_estribo / 10) - nbarT_1cam * bitola_t / 10) / (
                            nbarT_1cam - 1)
            if round(nbarT / nbarT_1cam) < nbarT / nbarT_1cam:
                ncamT = round(nbarT / nbarT_1cam) + 1
            else:
                ncamT = round(nbarT / nbarT_1cam)

            e_horC = (self.base - 2 * (self.cobrimento + diametro_estribo / 10) - nbarC_1cam * bitola_t / 10) / (
                        nbarC_1cam - 1)
            while e_horC <= diametro_brita:
                nbarC_1cam -= 1
                e_horC = (self.base - 2 * (self.cobrimento + diametro_estribo / 10) - nbarC_1cam * bitola_t / 10) / (
                            nbarC_1cam - 1)
            if round(nbarC / nbarC_1cam) < nbarC / nbarC_1cam:
                ncamC = round(nbarC / nbarC_1cam) + 1
            else:
                ncamC = round(nbarC / nbarC_1cam)
            return [[nbarT_1cam, e_horT, ncamT], [nbarC_1cam, e_horC, ncamC]]

    def calcular_centroide(self, bitola_t, bitola_c, diametro_brita, diametro_estribo):
        if self.mi() < 0.3:
            camadas = self.camadas_armadura(bitola_t, bitola_c, diametro_brita, diametro_estribo)[2]
        else:
            camadas = self.camadas_armadura(bitola_t, bitola_c, diametro_brita, diametro_estribo)[0][2]

        if camadas == 1:
            self.centroide = self.cobrimento + diametro_estribo / 10 + bitola_t / 20
        elif camadas == 2:
            n1 = (self.cobrimento + diametro_estribo / 10 + bitola_t / 20)
            n2 = (n1 + bitola_t / 20 + 2 + bitola_t / 20)
            d = self.barras_aco(bitola_t)
        else:
            self.centroide = 10
            print('\nCálculo de centroide em desenvolvimento. Valor genérico.')

            # FIXME: IDENTIFICAR ERRO - CÁLCULO DE CENTRÓIDE INCONSISTENTE 3+ CAMADAS
            # if self.mi() < 0.3:
            #     nbar_1cam = self.camadas_armadura(bitola_t, bitola_c, diametro_brita, diametro_estribo)[0][0]
            #     yCamada = [self.cobrimento + diametro_estribo + bitola_t/20]
            #     for x in range(0, camadas-1):
            #         yCamada.append(bitola_t/20 + 2 + bitola_t/20)
            #
            #     centroide = yCamada[0]*nbar_1cam
            #
            #
            #     self.centroide = round((self.camadas_armadura(bitola_t, bitola_c, diametro_brita, diametro_estribo)[0] * n1
            #     + (self.barras_aco(bitola_t) - self.camadas_armadura(bitola_t, bitola_c, diametro_brita,
            #                                                        diametro_estribo)[0]) * n2) / d, 2)
            # else:
            #     d = self.barras_aco(bitola_t)[0]
            #     self.centroide = round(self.camadas_armadura(bitola_t, bitola_c, diametro_brita, diametro_estribo)[0][
            #                          0] * n1 + (self.barras_aco(bitola_t)[0] -
            #                 self.camadas_armadura(bitola_t, bitola_c, diametro_brita, diametro_estribo)[0][0] * n2 /
            #                                     d), 2)

        self.calcular_altura_util()
        return self.centroide

    def verificar(self, bitola):
        if self.mi() < 0.3:
            area_aco_real = self.barras_aco(bitola) * pi * (bitola) ** 2 / 400
        else:
            area_aco_real = self.barras_aco(bitola)[0] * pi * (bitola) ** 2 / 400
        print(f'{area_aco_real}cm2')
        ks = self.ks()
        print(f'{ks}cm2')
        omega = area_aco_real / ks
        print(f'{omega}')
        mi = omega - (omega ** 2) / 2
        print(f'{mi}')
        mk_max = round((mi * self.sigmacd() * self.base * self.altura_util ** 2 / 1.4) / 100, 2)
        return mk_max

    def delta_mi(self):
        return round(self.mi() - 0.3, 2)

    def delta_d(self):
        return round(self.centroide / self.altura_util, 2)

    def aco_comprimido(self):
        return round((self.ks() * self.delta_mi()) / (1 - self.delta_d()), 2)

    def aco_tracionado(self):
        return round(self.aco_comprimido() + 0.36 * self.ks(), 2)


class LajeMacicaFlexao():
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


class SapataIsoladaFlexao():
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

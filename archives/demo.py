from classes import *

viga = VigaFlexao()
viga.base = 18
viga.altura = 65
viga.mk = 29
viga.fck = 30
viga.aco = 50


#cobrimento 3, estribo 5
bitolaT = 20
bitolaC = 10
cobrimento = 3
centroide = 5
brita = 2.5
estribo = 10

print(f'Sigma: {viga.sigmacd()}, fyd: {viga.fyd()}')
print(f'u: {viga.mi()}')
if viga.mi() < 0.30:
      print(f'w: {viga.omega()}, ks: {viga.ks()}cm2')
      print(f'Área de aço: {viga.area_aco()}cm2')
      print(f'Total de barras: {viga.barras_aco(bitolaT)}')
      print(f'cam1 = {viga.camadas_armadura(bitolaT, cobrimento, centroide)[0]} barras, Total de camadas = '
            f'{viga.camadas_armadura(bitolaT, cobrimento, centroide)[2]} camadas')
      print(f'Centroide: {viga.calcular_centroide(bitolaT, cobrimento, centroide)}cm')
      print(f'Mk limite: {viga.verificar(bitolaT)}')
else:
      print(f'Delta mi: {viga.delta_mi()}, Delta d: {viga.delta_d()}')
      print(f'Aço comprimido: {viga.aco_comprimido()} cm2')
      print(f'Aço tracionado: {viga.aco_tracionado()} cm2')
      print(f'Total de barras tracionadas: {viga.barras_aco(bitolaT, bitolaC)[0]}')
      print(f'Total de barras comprimidas: {viga.barras_aco(bitolaT, bitolaC)[1]}')
      print(f'\nArmadura de tração: ')
      print(f'Barras na primeira camada = {viga.camadas_armadura(bitolaT, bitolaC, cobrimento, centroide)[0][0]} '
            f'barras, Total de camadas = '
            f'{viga.camadas_armadura(bitolaT, bitolaC, cobrimento, centroide)[0][2]} camadas')

      print(f'Centroide: {viga.calcular_centroide(bitolaT, bitolaC, brita, estribo)}cm')
      print(f'Mk limite: {viga.verificar(bitolaT)}')

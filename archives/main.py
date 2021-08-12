from PyQt5 import uic, QtWidgets, QtGui
from classes import Viga_flexao, Viga_cisalhamento, Laje_macica_flexao, Sapata_isolada_flexao

def opcao_viga():
    tipo = inicio.comboBox_vigas.currentIndex()
    if tipo == 0:
        viga_flexao.show()
        inicio.close()
    elif tipo == 1:
        viga_cisalhamento.show()
        inicio.close()
    elif tipo == 2:
        viga_flexao_verif.show()
        inicio.close()
    elif tipo == 3:
        viga_cisalhamento_verif.show()
        inicio.close()
    else:
        print('Opção não identificada')


def opcao_laje():
    tipo = inicio.comboBox_lajes.currentIndex()
    if tipo == 0:
        lajem_flexao.show()
        inicio.close()
    elif tipo == 1:
        print('Laje Nervurada Unidirecional')
    elif tipo == 2:
        print('Laje Nervurada Bidirecional')
    elif tipo == 3:
        print('Verificação Laje maciça')
    elif tipo == 4:
        print('Verificação Laje Nervurada Unidirecional')
    elif tipo == 5:
        print('Verificação Laje Nervurada Bidirecional')
    else:
        print('Opção não identificada')


def opcao_sapata():
    tipo = inicio.comboBox_sapatas.currentIndex()
    if tipo == 0:
        print('Sapata isolada')
    else:
        print('Opção não identificada')


def opcao_pilar():
    tipo = inicio.comboBox_pilares.currentIndex()
    if tipo == 0:
        print('Pilar de canto')
    elif tipo == 1:
        print('Pilar de extremidade')
    elif tipo == 2:
        print('Pilar intermediário')
    else:
        print('Opção não identificada')


def calcular_vigas_flexao():
    viga = Viga_flexao()
    viga.base = viga_flexao.spinBox_base.value()
    viga.altura = viga_flexao.spinBox_altura.value()
    viga.mk = viga_flexao.doubleSpinBox_mk.value()
    viga.fck = int(list(viga_flexao.comboBox_fck.currentText())[0] + (list(viga_flexao.comboBox_fck.currentText())[
        1]))
    if viga_flexao.comboBox_aco.currentIndex() == 0:
        viga.aco = 50
    else:
        viga.aco = 60
    if viga_flexao.lineEdit_centroide.text() != '':
        viga.centroide = int(viga_flexao.lineEdit_centroide.text())

    print(viga.base, viga.altura, viga.mk, viga.fck, viga.aco, viga.centroide)
    print(viga.sigmacd())
    print(viga.fyd())
    print(viga.mi())
    print(viga.omega())
    print(viga.ks())
    print(viga.area_aco())
    print(viga.barras_aco(20))

#INTERFACE
programa = QtWidgets.QApplication([])
inicio = uic.loadUi('../GUI/main.ui')
viga_flexao = uic.loadUi('../GUI/viga_flexao.ui')
viga_cisalhamento = uic.loadUi('../GUI/viga_cisalhamento.ui')
lajem_flexao = uic.loadUi('../GUI/lajem_flexao.ui')
viga_flexao_verif = uic.loadUi('../GUI/viga_flexao_verificacao.ui')
viga_cisalhamento_verif = uic.loadUi('../GUI/viga_cisalhamento_verificacao.ui')


#BOTÕES E AÇÕES
inicio.pushButton_vigas.clicked.connect(opcao_viga)
inicio.pushButton_lajes.clicked.connect(opcao_laje)
inicio.pushButton_pilares.clicked.connect(opcao_pilar)
inicio.pushButton_sapatas.clicked.connect(opcao_sapata)

viga_flexao.pushButton_calcular.clicked.connect(calcular_vigas_flexao)

#EXECUÇÃO
inicio.show()
programa.exec()
from classes import *

def opcao_viga(tela0, tela1, tela2, tela3, tela4):
    tipo = tela0.comboBox_vigas.currentIndex()
    if tipo == 0:
        tela1.show()
        tela0.close()
    elif tipo == 1:
        tela2.show()
        tela0.close()
    elif tipo == 2:
        tela3.show()
        tela0.close()
    elif tipo == 3:
        tela4.show()
        tela0.close()

#FUNCOES
def calcular(data_container):
    viga = Viga_flexao()
    viga.base = data_container.spinBox_base.value()
    viga.altura = data_container.spinBox_altura.value()
    viga.mk = data_container.doubleSpinBox_mk.value()
    viga.fck = int(list(data_container.comboBox_fck.currentText())[0] + (list(data_container.comboBox_fck.currentText())[1]))
    if data_container.comboBox_aco.currentIndex() == 0:
        viga.aco = 50
    else:
        viga.aco = 60
    if data_container.lineEdit_centroide.text() != '':
        viga.centroide = int(data_container.lineEdit_centroide.text())

    print(viga.barras_aco(20))



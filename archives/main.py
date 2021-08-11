from PyQt5 import uic, QtWidgets, QtGui

def opcao_viga():
    tipo = inicio.comboBox_vigas.currentIndex()
    if tipo == 0:
        viga_flexao.show()
        inicio.close()
    elif tipo == 1:
        viga_cisalhamento.show()
        inicio.close()


#INTERFACE
programa = QtWidgets.QApplication([])
inicio = uic.loadUi('../GUI/main.ui')
viga_flexao = uic.loadUi('../GUI/viga_flexao.ui')
viga_cisalhamento = uic.loadUi('../GUI/viga_cisalhamento.ui')


#BOTÕES E AÇÕES
inicio.pushButton_vigas.clicked.connect(opcao_viga)
viga_flexao.pushButton_voltar.clicked.connect(tela_inicial)
viga_cisalhamento.pushButton_voltar.clicked.connect(tela_inicial)

#EXECUÇÃO
inicio.show()
programa.exec()
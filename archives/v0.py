from PyQt5 import uic, QtWidgets
from lajes_funcoes_variaveis import *
from vigas_funcoes_variaveis import *
from sapatas_funcoes_variaveis import *
from pilares_funcoes_variaveis import *


#INTERFACE
programa = QtWidgets.QApplication([])
inicio = uic.loadUi('../GUI/main.ui')
viga_flexao = uic.loadUi('../GUI/viga_flexao.ui')
viga_flexao_verif = uic.loadUi('../GUI/viga_flexao_verificacao.ui')
viga_cisalhamento = uic.loadUi('../GUI/viga_cisalhamento.ui')
viga_cisalhamento_verif = uic.loadUi('../GUI/viga_cisalhamento_verificacao.ui')
lajem_flexao = uic.loadUi('../GUI/lajem_flexao.ui')


#BOTOES E AÇÕES
inicio.pushButton_vigas.clicked.connect(lambda: opcao_viga(inicio, viga_flexao, viga_cisalhamento, viga_flexao_verif,
                                                           viga_cisalhamento_verif))
inicio.pushButton_lajes.clicked.connect(lambda: opcao_laje(inicio, lajem_flexao))
inicio.pushButton_pilares.clicked.connect(lambda: opcao_pilar)
inicio.pushButton_sapatas.clicked.connect(lambda: opcao_sapata(inicio, lajem_flexao))
viga_flexao.pushButton_calcular.clicked.connect(lambda: calcular(viga_flexao))

#EXECUÇÃO
inicio.show()
programa.exec()
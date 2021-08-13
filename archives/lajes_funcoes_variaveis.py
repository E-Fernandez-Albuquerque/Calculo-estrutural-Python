#INCOMPLETO
def opcao_laje(tela0, tela1):
    tipo = tela0.comboBox_lajes.currentIndex()
    if tipo == 0:
        tela1.show()
        tela0.close()
    elif tipo == 1:
        print('NU')
    elif tipo == 2:
        print('NB')
    elif tipo == 3:
        print('MV')
    elif tipo == 4:
        print('NUV')
    elif tipo == 5:
        print('NBV')

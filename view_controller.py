# -*- coding: utf-8 -*-

#dev by Jonas Duarte - Duzz System

from tkinter import *
from time import sleep

class sesp_view():
    def __init__(self):
        self.x = list()
        self.y = list()
        self.tela_inicial()

    def posiciona_janela(self):
        try:
            self.x.clear()
            self.y.clear()
        except:
            pass

        self.altura = int(self.tela.winfo_screenheight()/1.2)
        self.largura = int(self.tela.winfo_screenwidth()/1.2)

        self.x.append((self.largura/2)/4)
        self.y.append((self.altura/2)/4)
        self.y.append((self.altura/2)/1.27)
        self.y.append(self.altura/1.5)

    def tela_inicial(self):
        self.tela = Tk()
        self.posiciona_janela()
        self.tela.geometry(f"{self.largura}x{self.altura}+0+0")

        botao1 = Button(self.tela, text = "Atualizar Velórios", bg = "yellow", fg = "black", height = "7", width = "15", bd = "10", relief = "flat")
        botao2 = Button(self.tela, text = "Atualizar Velórios", bg = "yellow", fg = "black", height = "7", width = "15", bd = "10", relief = "flat")
        botao3 = Button(self.tela, text = "Atualizar Velórios", bg = "yellow", fg = "black", height = "7", width = "15", bd = "10", relief = "flat")


        botao1.place(x=f"{self.x[0]}", y = f"{self.y[0]}")
        botao2.place(x=f"{self.x[0]}", y = f"{self.y[1]}")
        botao3.place(x=f"{self.x[0]}", y = f"{self.y[2]}")
        self.tela.mainloop()


if __name__ == "__main__":
    main = sesp_view()

"""

    Para o programa verificar se foi corrigido ou não, devemos colocar como argumento na tela_inicial se o
programa está iniciando depois de alguma modificação.

    Após fazer alguma alteração que necessite reinício, o sesp se colocará como início automático e lança no txt o valor True.
antes de iniciar, o controller verifica no arquivo txt consta o valor True ou False.

    Se a resposta for positiva, o sesp envia para o servidor a etiqueta da máquina e o prodecimento decorrido.
Caso contrário, o sesp abrirá a página do glpi, induzindo o colaborador a abrir chamado para o T.I.

"""

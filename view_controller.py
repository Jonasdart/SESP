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

        self.altura = int(self.tela.winfo_screenheight()- 75)
        self.largura = int(self.tela.winfo_screenwidth())

        self.tela.state("zoomed")

        self.x.append((self.largura/2)/4)
        self.y.append((self.altura/2)/4)
        self.y.append((self.altura/2)/1.27)
        self.y.append(self.altura/1.5)

        if self.x[0] > 100:
            self.tamanho_fonte_botoes = "11"
        else:
            self.tamanho_fonte_botoes = "8"

        print(self.x)
        print(self.y)

    def tela_inicial(self):
        self.tela = Tk()
        self.posiciona_janela()
        self.tela.geometry(f"{self.largura}x{self.altura}+0+0")
        self.tela["bg"] = "#193E4D"

        botao1 = Button(self.tela, text = "Verificar Internet", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "8", width = "17", 
            bd = "1", relief = "flat", overrelief = "sunken")
        botao2 = Button(self.tela, text = "Verificar SPDATA", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "8", width = "17", 
            bd = "1", relief = "flat", overrelief = "sunken")
        botao3 = Button(self.tela, text = "Verificar Impressora", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "8", width = "17", 
            bd = "1", relief = "flat", overrelief = "sunken")


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

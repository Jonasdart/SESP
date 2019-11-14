# -*- coding: utf-8 -*-

#dev by Jonas Duarte - Duzz System

from tkinter import *
from time import sleep
from model import backend

class sesp_view():
    def __init__(self):
        self.backend = backend()

        self.botoes_menu_x = list()
        self.botoes_menu_y = list()
        self.botoes_controle_x = list()
        self.botoes_controle_y = list()
        self.tela_inicial()

    def posiciona_janela(self):
        try:
            self.x.clear()
            self.y.clear()
        except:
            pass

        self.altura = int(self.tela.winfo_screenheight()- 75)
        self.largura = int(self.tela.winfo_screenwidth())

        if self.largura/2/4 > 100:
            self.tamanho_fonte_botoes = "11"
        else:
            self.tamanho_fonte_botoes = "8"

        self.tela.state("zoomed")

    def botoes_menu(self):
        self.botoes_menu_x.append((self.largura/2)/10)
        self.botoes_menu_y.append((self.altura/2)/4)
        self.botoes_menu_y.append((self.altura/2)/1.27)
        self.botoes_menu_y.append(self.altura/1.5)


    def botoes_controle(self):
        self.botoes_controle_x.append((self.largura/1.18))
        self.botoes_controle_y.append((self.altura/2)/4)

    def tela_inicial(self):
        self.tela = Tk()
        self.posiciona_janela()
        self.botoes_menu()
        self.botoes_controle()
        self.tela.geometry(f"{self.largura}x{self.altura}+0+0")
        self.tela["bg"] = "#193E4D"

        verificar_internet = Button(self.tela, text = "Verificar Internet", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "8", width = "17", 
            bd = "1", relief = "flat", overrelief = "sunken")
        verificar_spdata = Button(self.tela, text = "Verificar SPDATA", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "8", width = "17", 
            bd = "1", relief = "flat", overrelief = "sunken")
        verificar_impressora = Button(self.tela, text = "Verificar Impressora", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "8", width = "17", 
            bd = "1", relief = "flat", overrelief = "sunken")

        meu_computador = Button(self.tela, text = "Meu Computador", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "20", 
            bd = "1", relief = "flat", overrelief = "sunken", command = self.backend.busca_cabecalho)



        verificar_internet.place(x=f"{self.botoes_menu_x[0]}", y = f"{self.botoes_menu_y[0]}")
        verificar_spdata.place(x=f"{self.botoes_menu_x[0]}", y = f"{self.botoes_menu_y[1]}")
        verificar_impressora.place(x=f"{self.botoes_menu_x[0]}", y = f"{self.botoes_menu_y[2]}")
        meu_computador.place(x=f"{self.botoes_controle_x[0]}", y = f"{self.botoes_controle_y[0]}")    
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

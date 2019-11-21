# -*- coding: utf-8 -*-

#dev by Jonas Duarte - Duzz System
import threading
from tkinter import *
from time import sleep
from model import backend
from controller import controller

class sesp_view():
    def __init__(self):
        self.backend = backend()
        self.controller = controller()

        self.botoes_menu_x = list()
        self.botoes_menu_y = list()
        self.botoes_controle_x = list()
        self.botoes_controle_y = list()
        
        self.tela_inicial()

    def tela_inicial(self):
        self.tela = Tk()
        self.posiciona_janela()
        self.botoes_controle()
        self.mostra_esconde_botoes()
        self.tela.geometry(f"{self.largura}x{self.altura}+0+0")
        self.tela["bg"] = "#193E4D"
 
        self.tela.mainloop()

    def posiciona_janela(self):
        self.gera_gif_carregamento()

        try:
            self.x.clear()
            self.y.clear()
        except:
            pass

        self.altura = int(self.tela.winfo_screenheight()+100)
        self.largura = int(self.tela.winfo_screenwidth())

        if self.largura/2/4 > 100:
            self.tamanho_fonte_botoes = "11"
        else:
            self.tamanho_fonte_botoes = "8"

        self.tela.state("zoomed")

    def mostra_esconde_botoes(self, mostrar = True):
        if mostrar:
            self.widgets_botoes_menu = self.botoes_menu()
            for i in range(len(self.widgets_botoes_menu)):
                self.widgets_botoes_menu[i].place(x=f"{self.botoes_menu_x[0]}", y = f"{self.botoes_menu_y[i]}")
            self.botao_lateral["text"] = "<"
            self.botao_lateral["command"] = lambda: self.mostra_esconde_botoes(mostrar = False)
        else:
            for i in range(len(self.widgets_botoes_menu)):
                self.widgets_botoes_menu[i].place_forget()
                self.botao_lateral["text"] = ">"
                self.botao_lateral["command"] = lambda: self.mostra_esconde_botoes()

    def botoes_menu(self, tela = None):
        self.posiciona_botoes_menu()

        if tela is None:
            tela = self.tela

        verificar_internet = Button(tela, text = "Internet Não Funciona", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "20", 
            bd = "1", relief = "flat", overrelief = "sunken")
        verificar_spdata = Button(tela, text = "SPDATA Não Abre", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "20", 
            bd = "1", relief = "flat", overrelief = "sunken")
        verificar_travamento_spdata = Button(tela, text = "SPDATA Travando", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "20", 
            bd = "1", relief = "flat", overrelief = "sunken")
        verificar_glpi = Button(tela, text = "GLPI Sem Acesso", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "20", 
            bd = "1", relief = "flat", overrelief = "sunken")
        verificar_computador = Button(tela, text = "Computador Travando", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "20", 
            bd = "1", relief = "flat", overrelief = "sunken")
        verificar_impressora = Button(tela, text = "Não Consigo Imprimir", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "20", 
            bd = "1", relief = "flat", overrelief = "sunken")

        #COMANDOS

        verificar_internet["command"] = lambda: self.armador('01')
        verificar_spdata["command"] = lambda: self.armador('02')
        verificar_travamento_spdata["command"] = lambda: self.armador('03')
        verificar_glpi["command"] = lambda: self.armador('04')
        verificar_computador["command"] = lambda: self.armador('05')
        verificar_impressora["command"] = lambda: self.armador('06')

        return [verificar_internet, verificar_spdata, verificar_travamento_spdata, verificar_glpi, verificar_computador, verificar_impressora]


    def botoes_controle(self, tela = None):
        self.posiciona_botoes_controle()

        if tela is None:
            tela = self.tela

        self.botao_meu_computador = Button(tela, text = "Meu Computador", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "20", 
            bd = "1", relief = "flat", overrelief = "sunken", command = self.backend.busca_cabecalho)
        self.botao_lateral = Button(tela, justify = "left", text = ">", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}", "bold"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "40", width = "2", 
            bd = "1", relief = "flat", overrelief = "sunken")

        self.botao_meu_computador.place(x=f"{self.botoes_controle_x[1]}", y = f"{self.botoes_controle_y[1]}")
        self.botao_lateral.place(x=f"{self.botoes_controle_x[0]}", y = f"{self.botoes_controle_y[0]}")

        #COMANDOS

        self.botao_meu_computador["command"] = self.gera_popup_informacoes
        self.botao_lateral["command"] = lambda: self.mostra_esconde_botoes()

    def posiciona_botoes_menu(self):
        #eixo x
        self.botoes_menu_x.append((self.largura/2)/10)
        #eixo y
        self.botoes_menu_y.append((self.altura/1)/8)
        self.botoes_menu_y.append((self.altura/1)/5)
        self.botoes_menu_y.append((self.altura/1)/3.62)
        self.botoes_menu_y.append((self.altura/1)/2.85)
        self.botoes_menu_y.append((self.altura/1)/2.35)
        self.botoes_menu_y.append((self.altura/1)/2)


    def posiciona_botoes_controle(self):
        self.botoes_controle_x.append(1)
        self.botoes_controle_x.append(self.largura/1.18)
        self.botoes_controle_y.append(1)
        self.botoes_controle_y.append((self.altura/2)/20)

    def gera_gif_carregamento(self):
        self.gif_frames = list()
        for x in range(100):
            try:
                self.gif_frames.append(PhotoImage(file=f'img/carregamento/gif_carregamento4.GIF', format = f'gif -index {x}'))
            except:
                break

    def armador(self, tipo):

        if tipo is '01':
            self.acao = threading.Thread(target = self.controller.corrigir_internet)
            self.acao.start()
        elif tipo is '02':
            self.acao = threading.Thread(target= self.controller.spdata_nao_abre)
            self.acao.start()
        elif tipo is '03':
            pass

        self.gera_popup_carregamento(self.gif_frames)

    def gera_popup_informacoes(self, ativo = False, popup_informacoes = None):
        if not ativo:
            self.botao_meu_computador["command"] = lambda: self.gera_popup_informacoes(ativo = True, popup_informacoes = popup_informacoes)
            self.botao_meu_computador["relief"] = "sunken"
            self.botao_meu_computador["bg"] = "#193E4D"
            altura = int((self.altura - 100) / 2)
            largura = int(self.largura / 2)
            popup_informacoes = Toplevel(self.tela)
            popup_informacoes["bg"] = "#091A1B"
            popup_informacoes.transient(self.tela)
            popup_informacoes.overrideredirect(True)
            popup_informacoes.geometry(f"{largura}x{altura}+{int(altura)}+{int(largura/3)}")
            popup_informacoes.lift()
            popup_informacoes.wm_attributes("-topmost", True)
            popup_informacoes.wm_attributes("-disabled", True)
            popup_informacoes.wm_attributes("-transparentcolor", "white")

            """string = f"Olá! Você está no computador {self.backend.cabecalho_etiqueta}\n"
                                                string += "Se o problema não for corrigido\nabra um chamado no sistema GLPI\n"
                                                string += f'O número do seu acesso remoto é:\n {self.backend.cabecalho_ip}'"""
            string = f'COMPUTADOR = {self.backend.cabecalho_etiqueta}\n\n'
            string+= f'ACESSO REMOTO = {self.backend.cabecalho_ip}\n\n'
            string+= f'SE O PROBLEMA NÃO FOR RESOLVIDO\nABRA UM CHAMADO COM O GLPI'

            label = Label(popup_informacoes, justify = "left", text = string, font = ("Verdana", "22", "bold"), fg = "#BADAE8", bg = "#091A1B", relief = "flat")
            label.pack(expand = True)
        else:
            self.botao_meu_computador["command"] = lambda: self.gera_popup_informacoes(ativo = False)
            self.botao_meu_computador["relief"] = "flat"
            self.botao_meu_computador["bg"] = "#0B1F22"
            popup_informacoes.destroy()

    def gera_popup_carregamento(self, gif):
        popup_carregamento = Toplevel(self.tela)

        popup_carregamento.transient(self.tela)
        popup_carregamento.overrideredirect(True)
        popup_carregamento.geometry(f"+600+300")
        popup_carregamento.lift()
        popup_carregamento.wm_attributes("-topmost", True)
        popup_carregamento.wm_attributes("-disabled", True)
        popup_carregamento.wm_attributes("-transparentcolor", "white")

        """label_f = Label(popup_fundo_carregamento, bg = "white", image=gif[0])
        label_f.pack()"""
        label = Label(popup_carregamento, bg="white")
        label.pack()

        self.inicia_gif_carregamento(popup_carregamento, gif, label)

    def inicia_gif_carregamento(self, popup, gif, label, indice = 0):
        try:
            label.configure(image = gif[indice])
        except:
            indice = 0
            label.configure(image = gif[indice])

        if self.acao.isAlive():
            popup.after(90, lambda: self.inicia_gif_carregamento(popup, gif, label, indice+1))
        else:
            popup.destroy()


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

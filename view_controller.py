#encoding: utf-8
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
        self.feedback_fixo = ''
        self.feedback = ''

        self.botoes_menu_x = list()
        self.botoes_menu_y = list()
        self.botoes_controle_x = list()
        self.botoes_controle_y = list()

        self.tela_inicial()

    def tela_inicial(self):
        self.tela = Tk()

        self.acao = threading.Thread(target = self.gera_gif_carregamento)
        self.acao.start()

        self.posiciona_janela()
        self.botoes_controle()
        self.mostra_esconde_botoes()

        self.tela.geometry(f"{self.largura}x{self.altura}+0+0")
        self.tela["bg"] = "#193E4D"

        self.label_feedback_fixo = Label(self.tela, text = self.feedback, font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            height = "2", bd = "1", relief = "flat")
        self.label_feedback_fixo.pack()#place(x = f'{self.largura/2.6}', y = f'{self.altura/5}')
        self.label_feedback = Label(self.tela, text = self.feedback, font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            height = "2", bd = "1", relief = "flat")
        self.label_feedback.pack()#place(x = f'{self.largura/2.4}', y = f'{self.altura/4}')
 
        try:
            self.acao_feedback = threading.Thread(target = self.busca_feedback)
            self.acao_feedback.start()
        except:
            raise

        self.tela.mainloop()

    def posiciona_janela(self):

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

        verificar_internet = Button(tela, text = "CORRIGIR INTERNET", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "22", 
            bd = "1", relief = "flat", overrelief = "sunken")
        corrigir_spdata = Button(tela, text = "CORRIGIR SPDATA", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "22", 
            bd = "1", relief = "flat", overrelief = "sunken")
        verificar_glpi = Button(tela, text = "GLPI SEM ACESSO", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "22", 
            bd = "1", relief = "flat", overrelief = "sunken")
        verificar_computador = Button(tela, text = "COMPUTADOR TRAVANDO", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "22", 
            bd = "1", relief = "flat", overrelief = "sunken")
        verificar_impressora = Button(tela, text = "NÃO CONSIGO IMPRIMIR", bg = "#0B1F22", font = ("Verdana", f"{self.tamanho_fonte_botoes}"), fg = "white", 
            highlightcolor = "white", activebackground = "#193E4D", activeforeground = "white", height = "2", width = "22", 
            bd = "1", relief = "flat", overrelief = "sunken")

        #COMANDOS

        verificar_internet["command"] = lambda: self.armador('01')
        corrigir_spdata["command"] = lambda: self.armador('02')
        verificar_glpi["command"] = lambda: self.armador('03')
        verificar_computador["command"] = lambda: self.armador('04_1')
        verificar_impressora["command"] = lambda: self.armador('05')

        return [verificar_internet, corrigir_spdata, verificar_glpi, verificar_computador, verificar_impressora]


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

        self.botao_meu_computador["command"] = lambda: self.gera_popup_informacoes()
        self.botao_lateral["command"] = lambda: self.mostra_esconde_botoes()


    def posiciona_botoes_menu(self):
        #eixo x
        self.botoes_menu_x.append((self.largura/2)/10)
        #eixo y
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
                self.gif_frames.append(PhotoImage(file=f'img/carregamento/carregamento_foguete.GIF', format = f'gif -index {x}'))
            except:
                break

    def busca_feedback(self):

        self.feedback_fixo = self.controller.feedback_fixo
        self.feedback = self.controller.feedback

        if len(self.feedback_fixo) is not 0:
            self.label_feedback_fixo["bg"] = "#193E4D"
        else:
            self.label_feedback_fixo["bg"] = "#193E4D"

        if len(self.feedback) is not 0:
            self.label_feedback["bg"] = "#193E4D"
            
        else:
            self.label_feedback["bg"] = "#193E4D"
            
        self.label_feedback_fixo["text"] = self.feedback_fixo
        self.label_feedback_fixo["width"] = f'{len(self.feedback_fixo)+2}'
        self.label_feedback["text"] = self.feedback
        self.label_feedback["width"] = f'{len(self.feedback)+2}'
        
        self.tela.after(10, self.busca_feedback)

    def armador(self, tipo):
        self.controller.restaura_mensagem_feedback()
        self.destruir_popup(mostrar_botoes = False)
        if tipo is '01':
            self.acao = threading.Thread(target = lambda: self.controller.corrigir_internet())
            #self.acao = threading.Thread(target = lambda: self.backend.buscar_ip(self.backend.cabecalho_etiqueta))
            self.acao.start()
        elif tipo is '02':
            self.comando_verificacao_spdata()
        elif tipo is '03':
            self.acao = threading.Thread(target = lambda: self.controller.corrigir_internet())
            self.acao.start()
        elif tipo is '04':
            self.acao = threading.Thread(target = lambda: self.controller.corrigir_travamento_computador())
            self.acao.start()
        elif tipo is '04_1':
            self.comando_correcao_travamento_pc()
        if len(tipo) is 2:
            self.gera_popup_carregamento(self.gif_frames)

    def comando_correcao_travamento_pc(self):
        mensagem = 'SALVE SEUS TRABALHOS\n\nO COMPUTADOR SERÁ REINICIADO'
        self.gera_popup_confirmacao(mensagem = mensagem, texto_botao_1 = 'Continuar', texto_botao_2 = 'Cancelar', comando_botao_1 = '04')
        
    def comando_verificacao_spdata(self, terminou_processo = False):
        if terminou_processo:
            if self.em_verificacao is not None:
                if not self.em_verificacao:
                    mensagem = "VERIFICAÇÃO CONCLUÍDA COM SUCESSO\nSISTEMA ESTÁ OK!\n\nPor favor, verifique se o problema foi corrigido e nos informe clicando no botão."
                    self.gera_popup_confirmacao(titulo = "Verificação SPDATA", bg = 'green', fg = "black", cor_botao = 'white', mensagem = mensagem, 
                        texto_botao_1 = "Funcionou", texto_botao_2 = "Não funcionou")
                else:
                    mensagem = self.em_verificacao
                    self.gera_popup_confirmacao(titulo = "Verificação", mensagem = mensagem, texto_botao_meio = "OK", bg = 'yellow', fg = 'black', cor_botao = 'white')

        else:
            self.acao = threading.Thread(target = lambda: self.busca_informacao_spdata())
            self.acao.start()           

    def terminou_processo(self, tela = None, processo = None):
        if processo is None:
            processo = self.acao
        if tela is None:
            tela = self.tela

        if processo.isAlive():
            tela.after(100, lambda: self.terminou_processo(tela = tela, processo = processo))
        else:
            self.comando_verificacao_spdata(terminou_processo = True)

    def busca_informacao_spdata(self):
        self.terminou_processo()
        try:
            self.em_verificacao = self.controller.corrigir_spdata()
        except:
            self.em_verificacao = None


    def gera_popup_confirmacao(self, tela = None, titulo = "AVISO", mensagem = "O computador será reiniciado...", 
        texto_botao_meio = None, texto_botao_1 = None, texto_botao_2 = None, bg = "#091A1B", fg = "yellow", 
        cor_botao = "#B8B63D", comando_botao_meio = None, comando_botao_1 = None, comando_botao_2 = None):

        self.destruir_popup(mostrar_botoes = False)

        if tela is None:
            tela = self.tela

        altura = int((self.altura - 50) / 2)
        largura = int(self.largura / 2)

        self.popup = Toplevel(tela)
        self.popup.geometry(f"{largura}x{altura}+{int(largura - 350)}+{int(altura - 250)}")
        self.popup.title(titulo)
        self.popup.resizable(0,0)
        self.popup["bg"] = bg

        label_mensagem = Label(self.popup, text = mensagem, font = ("Verdana", "15", "bold"), bg = bg, fg = fg)
        label_mensagem.pack(expand = True)
        label_borda = Label(self.popup, bg = bg, width = f'{largura}', height = "5")
        label_borda.pack()

        if texto_botao_meio is not None:
            botao_meio = Button(self.popup, text = texto_botao_meio, bg = cor_botao, fg = "black", 
                highlightcolor = "white", activebackground = "#193E4D", activeforeground = "black", height = "2", width = "13", 
                bd = "1", relief = "flat", overrelief = "sunken")

            if comando_botao_meio is None:
                botao_meio["command"] = lambda: self.destruir_popup()
            else:
                botao_meio["command"] = lambda: self.armador(comando_botao_meio)

            botao_meio.place(x = largura/2.4, y = altura/1.3)

        if texto_botao_1 is not None:
            botao_1 = Button(self.popup, text = texto_botao_1, bg = cor_botao, fg = "black", 
                highlightcolor = "white", activebackground = "#193E4D", activeforeground = "black", height = "2", width = "13", 
                bd = "1", relief = "flat", overrelief = "sunken")

            if comando_botao_1 is None: 
                botao_1["command"] = lambda: self.destruir_popup()
            else:
                botao_1["command"] = lambda: self.armador(comando_botao_1)

            botao_1.place(x = largura/3.7, y = altura/1.3)

        if texto_botao_2 is not None:
            botao_2 = Button(self.popup, text = texto_botao_2, bg = cor_botao, fg = "black", 
                highlightcolor = "white", activebackground = "#193E4D", activeforeground = "black", height = "2", width = "13", 
                bd = "1", relief = "flat", overrelief = "sunken")

            if comando_botao_2 is None: 
                botao_2["command"] = lambda: self.destruir_popup()
            else:
                botao_2["command"] = lambda: self.armador(comando_botao_2)

            botao_2.place(x = largura/1.772, y = altura/1.3)
        
    def gera_popup_informacoes(self, ativo = False, popup = None):
        self.backend.busca_cabecalho()
        if not ativo:
            
            altura = int((self.altura - 100) / 2)
            largura = int(self.largura / 2)

            self.popup = Toplevel(self.tela)
            self.popup["bg"] = "#091A1B"
            self.popup.transient(self.tela)
            self.popup.overrideredirect(True)
            self.popup.geometry(f"{largura}x{altura}+{int(altura)}+{int(largura/3)}")
            self.popup.lift()
            self.popup.wm_attributes("-topmost", True)
            self.popup.wm_attributes("-disabled", True)
            self.popup.wm_attributes("-transparentcolor", "white")

            self.botao_meu_computador["command"] = lambda: self.gera_popup_informacoes(ativo = True, popup = self.popup)
            self.botao_meu_computador["relief"] = "sunken"
            self.botao_meu_computador["bg"] = "#193E4D"

            string = f'COMPUTADOR = {self.backend.cabecalho_etiqueta}\n\n'
            string+= f'ACESSO REMOTO = {self.backend.cabecalho_ip}\n\n'
            string+= f'SE O PROBLEMA NÃO FOR RESOLVIDO\nABRA UM CHAMADO COM O GLPI'

            label = Label(self.popup, justify = "left", text = string, font = ("Verdana", "22", "bold"), fg = "#BADAE8", bg = "#091A1B", relief = "flat")
            label.pack(expand = True)
        else:
            self.botao_meu_computador["command"] = lambda: self.gera_popup_informacoes()
            self.botao_meu_computador["relief"] = "flat"
            self.botao_meu_computador["bg"] = "#0B1F22"
            self.popup.destroy()

    def gera_popup_carregamento(self, gif):
        
        label = Label(self.tela, bg = "#193E4D")
        label.pack(expand = True)

        self.inicia_gif_carregamento(gif, label)

    def destruir_popup(self, popup = None, label = None, mostrar_botoes = True):
        if mostrar_botoes:
            self.mostra_esconde_botoes()
        else:
            self.mostra_esconde_botoes(mostrar = False)

        try:
            self.popup.destroy()
        except:
            pass
        try:
            popup.destroy()
        except:
            pass
        try:
            label.pack_forget()
            label.place_forget()
        except:
            pass

    def inicia_gif_carregamento(self, gif, label, indice = 0):
        try:
            label.configure(image = gif[indice])
        except:
            indice = 0
            label.configure(image = gif[indice])

        if self.acao.isAlive():
            self.tela.after(50, lambda: self.inicia_gif_carregamento(gif, label, indice+1))
        else:
            self.destruir_popup(label = label)


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

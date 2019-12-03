#encoding: utf-8
# -*- coding: utf-8 -*-

#dev by Jonas Duarte - Duzz System

from model import backend
from time import sleep
from socket import *

class controller():

    def __init__(self):
        self.backend = backend()
        self.conectado = False
        self.feedback = ''
        self.feedback_fixo = ''

    def restaura_mensagem_feedback(self):
        self.feedback = ''
        self.feedback_fixo = ''

    def conecta_ao_servidor(self, cont = 3, ip_temp = False, verificou_com_ip_secundario = False):
        self.feedback_fixo = 'Estabelecendo Conexão com o servidor SESP'
        if not ip_temp:
            try:
                self.conectado = self.backend.conecta_ao_servidor()
            except:
                if cont is not 0:
                    self.feedback = "Tentando novamente"
                    self.conecta_ao_servidor(cont = cont-1)
                elif not verificou_com_ip_secundario:
                    self.feedback = "Tentando novamente com o IP temporário"
                    if self.usar_ip_temporario():
                        self.conecta_ao_servidor(ip_temp = True)
                    else:
                        self.conectado = False
                        return
                else:
                    self.conectado = False
                    self.feedback_fixo = "Não foi possível acessar o servidor SESP"
                    self.feedback = "Favor entrar em contato com o Administrador"
                    raise
            else:
                if self.conectado:
                    return True
                else:
                    self.feedback_fixo = "Não foi possível acessar o servidor SESP"
                    self.feedback = "Favor entrar em contato com o Administrador"
                    raise
        else:
            try:
                self.conectado = self.backend.conecta_ao_servidor()
            except:
                if cont is not 0:
                    self.feedback = "Tentando novamente com o IP temporário"
                    self.conecta_ao_servidor(cont = cont-1, ip_temp = True)
                else:
                    self.feedback = "Não foi possível acessar com o IP temporário"
                    self.conectado = False
                    self.restaurar_ip()
                        
                    self.conecta_ao_servidor(cont = 0, verificou_com_ip_secundario = True)
                    
            else:
                self.conectado = True
                self.atualizar_ip()
                self.conectado = False
                self.conecta_ao_servidor(verificou_com_ip_secundario = True)

    def desconectar_do_servidor(self):
        try:
            self.backend.encerrar_conexao()
        except:
            pass
        else:
            self.conectado = False

    def atualizar_horario(self):
        self.conecta_ao_servidor()
        try:
            data_e_hora_atuais = self.backend.buscar_horario_atual()
        except:
            raise
        else:
            try:
                data_e_hora_atuais = data_e_hora_atuais.decode("utf-8")
            except:
                raise
                
            else:
                self.backend.atualizar_horario(data_e_hora_atuais)

    def usar_ip_temporario(self, ip = None):
        if ip is None:
            ip = self.backend.cabecalho_ip_secundario

        msg_confirmacao = self.backend.atualizar_ip(ip)

        return msg_confirmacao

    def atualizar_ip(self):
        self.conecta_ao_servidor()
        self.backend.busca_cabecalho()
        try:
            ip = self.backend.buscar_ip(self.backend.cabecalho_etiqueta)
        except:
            raise
        if len(ip) is not 0:
            try:
                self.backend.atualizar_ip(ip)
            except:
                raise
            else:
                try:
                    self.backend.atualiza_cabecalho(ip = ip)
                except:
                    raise

    def restaurar_ip(self, ip = None):
        if ip is None:
            ip = self.backend.cabecalho_ip

        self.feedback = "Voltando ao IP cadastrado"

        msg_confirmacao = self.backend.atualizar_ip(ip)

        return msg_confirmacao

    def corrigir_internet(self):
        try:
            self.backend.definir_proxy()
        except:
            raise
        
        self.conecta_ao_servidor()

        try:
            self.atualizar_ip()
        except:
            raise
        
        try:
            self.atualizar_horario()
        except:
            raise


    def verificar_spdata(self):
        self.conecta_ao_servidor()
        try:
            status = self.backend.verificar_spdata()
        except:
            raise
        else:
            self.restaura_mensagem_feedback()
            print(status)
            status = status.decode("utf-8")
            if "False" in status:
                self.feedback_fixo = f"Não possui nenhum procedimento interrompendo o funcionamento do sistema"
                self.feedback = 'Entre em contato com o Administrador'
                retorno = False
            else:
                self.feedback_fixo = f"Sistema SPDATA está em manutenção travamentos poderão acontecer"
                self.feedback = status
                
                retorno = f"Sistema SPDATA está em manutenção \ntravamentos poderão acontecer \n\n\n{status}"
                
        return retorno 

    def spdata_nao_abre(self):
        self.conecta_ao_servidor()
        self.feedback_fixo = 'Corrigindo SPDATA'
        try:
            self.feedback = 'Atualizando horário do computador'
            self.atualizar_horario()
        except:
            self.feedback = 'Não foi possível atualizar a data e hora'
            #aqui se não conseguir buscar o horário, o problema provavelmente está na internet
            #portanto devemos chamar a função de correção de internet
            pass
        try:
            self.feedback = 'Fazendo o mapeamento do SPDATA'
            mapeamento_msg_confirmacao = self.backend.mapear_spdata()
        except:
            self.feedback_fixo = 'Não foi possível mapear o SPDATA'
            self.feedback = 'Entre em contato com o Administrador'
            pass
        return mapeamento_msg_confirmacao

    def corrigir_travamento_computador(self, chkdsk = False):
        self.conecta_ao_servidor()
        if chkdsk:
            try:
                self.backend.realizar_correcao_de_disco()
            except:
                pass
        try:
            self.backend.reiniciar_maquina()
        except:
            raise


if __name__ == "__main__":
    main = controller()
    try:
        main.atualizar_horario()
    except:
        pass
    else:
        main.verificar_spdata()
    #main.inicio()

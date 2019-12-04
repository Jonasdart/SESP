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
                    try:
                        self.usar_ip_temporario()
                    except:
                        self.conectado = False
                        raise
                    else:
                        self.conecta_ao_servidor(ip_temp = True)
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
            self.feedback = 'Buscando horário atual...'
            data_e_hora_atuais = self.backend.buscar_horario_atual()
        except:
            self.feedback = 'Não foi possível encontrar o horário atual no servidor'
        else:
            try:
                self.feedback = 'Decodificando configuração de data/hora...'
                data_e_hora_atuais = data_e_hora_atuais.decode("utf-8")
            except:
                self.feedback = 'Não foi possível decodificar a data e hora'
                
            else:
                self.feedback = 'Atualizando a configuração de data/hora...'
                self.backend.atualizar_horario(data_e_hora_atuais)

    def usar_ip_temporario(self, ip = None):
        if ip is None:
            ip = self.backend.cabecalho_ip_secundario

        try:
            self.backend.atualizar_ip(ip)
        except:
            self.feedback = 'Não foi possível configurar o IP temporário'
            raise

    def atualizar_ip(self):
        self.conecta_ao_servidor()
        self.backend.busca_cabecalho()
        try:
            self.feedback = 'Buscando o endereço de IP...'
            ip = self.backend.buscar_ip(self.backend.cabecalho_etiqueta)
        except:
            self.feedback = f'Não foi possível encontrar o IP da máquina {self.backend.cabecalho_etiqueta}'
        else:
            if len(ip) is not 0:
                try:
                    self.backend.atualizar_ip(ip)
                except:
                    self.feedback = f'Não foi possível definir o IP {ip} como principal'
                else:
                    try:
                        self.backend.atualiza_cabecalho(ip = ip)
                    except:
                        self.feedback = f'Não foi possível atualizar o cabeçalho'

    def restaurar_ip(self, ip = None):
        if ip is None:
            ip = self.backend.cabecalho_ip

        self.feedback = "Voltando ao IP cadastrado"

        try:
            self.backend.atualizar_ip(ip)
        except:
            self.feedback = 'Não foi possível voltar ao IP cadastrado'

    def corrigir_internet(self):
        self.feedback_fixo = 'Corrigindo conexão à internet'
        try:
            self.feedback = 'Definindo configurações de proxy'
            self.backend.definir_proxy()
        except:
            self.feedback = 'Não foi possível configurar o proxy'
        
        self.conecta_ao_servidor()

        try:
            self.atualizar_ip()
        except:
            pass
        
        try:
            self.atualizar_horario()
        except:
            pass


    def verificar_spdata(self):
        self.conecta_ao_servidor()

        try:
            status = self.backend.verificar_spdata()
        except:
            self.feedback = 'Não foi possível verificar o spdata'
        else:
            self.restaura_mensagem_feedback()
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

        try:
            self.feedback_fixo = 'Corrigindo SPDATA'
            self.feedback = 'Fazendo o mapeamento do SPDATA'
            mapeamento_msg_confirmacao = self.backend.mapear_spdata()
        except:
            self.feedback_fixo = 'Não foi possível mapear o SPDATA'
            self.feedback = 'Entre em contato com o Administrador'
            pass
        else:
            self.feedback = 'Mapeamento concluído'
        return mapeamento_msg_confirmacao

    def corrigir_travamento_computador(self, chkdsk = False):
        self.conecta_ao_servidor()
        self.feedback_fixo = 'Corrigindo problemas no sistema operacional'
        if chkdsk:
            try:
                self.backend.realizar_correcao_de_disco()
            except:
                pass
        try:
            self.backend.reiniciar_maquina()
        except:
            self.feedback = 'Não foi possível reiniciar o computador'

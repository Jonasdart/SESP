#encoding: utf-8
# -*- coding: utf-8 -*-

#dev by Jonas Duarte - Duzz System

from model import backend
from time import sleep
from socket import *
from selenium import webdriver

class controller():
    def __init__(self):
        self.backend = backend()
        self.feedback = ''
        self.feedback_fixo = ''

    def restaura_mensagem_feedback(self):
        self.feedback = ''
        self.feedback_fixo = ''

    def conecta_ao_servidor(self, cont = 3):
        self.feedback_fixo = 'Estabelecendo Conexão com o servidor SESP'
        if not self.backend.conectado:
            try:
                self.backend.conectado = self.backend.conecta_ao_servidor()
            except:
                if cont is not 0:
                    self.feedback = "Tentando novamente"
                    self.conecta_ao_servidor(cont = cont-1)
                else:
                    self.backend.conectado = False
                    self.feedback_fixo = "Não foi possível acessar o servidor SESP"
                    self.feedback = "Favor entrar em contato com o Administrador"
                    raise
            else:
                if self.backend.conectado:
                    return True
                else:
                    self.feedback_fixo = "Não foi possível acessar o servidor SESP"
                    self.feedback = "Favor entrar em contato com o Administrador"
                    raise
        else:
            self.feedback = 'Conectado ao SESP'

    def desconectar_do_servidor(self):
        try:
            self.backend.encerrar_conexao()
        except:
            pass
        else:
            self.backend.conectado = False

    def enviar_log(self, procedimento):
        try:
            self.feedback_fixo = 'Gerando arquivo de log'
            log = self.backend.gerar_log(procedimento)
        except:
            self.feedback_fixo = 'Erro ao gerar log'
            raise
        try:
            self.conecta_ao_servidor()
        except:
            raise
        try:
            self.feedback_fixo = 'Enviando log ao servidor'
            self.backend.enviar_log(log)
        except:
            self.feedback_fixo = 'Não foi possível enviar o log ao servidor'
            raise
        else:
            self.restaura_mensagem_feedback()

    def atualizar_horario(self):
        try:
            self.conecta_ao_servidor()
        except:
            raise
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

    def atualizar_ip(self):
        try:
            self.conecta_ao_servidor()
        except:
            raise
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
        
        try:
            self.conecta_ao_servidor()
        except:
            raise

        try:
            self.atualizar_ip()
        except:
            pass
        
        try:
            self.atualizar_horario()
        except:
            pass

    def corrigir_spdata(self):
        try:
            self.conecta_ao_servidor()
        except:
            raise
        manutencao = self.verificar_spdata()
        if manutencao is not None:
            if not manutencao:
                self.spdata_nao_abre()

        return manutencao

    def verificar_spdata(self):
        try:
            self.conecta_ao_servidor()
        except:
            raise

        try:
            status = self.backend.verificar_spdata()
        except:
            self.feedback = 'Não foi possível verificar o spdata'
        else:
            self.restaura_mensagem_feedback()
            status = status.decode("utf-8")
            if "False" in status:
                self.feedback_fixo = f"Não possui nenhum procedimento interrompendo o funcionamento do sistema"
                retorno = False
            else:
                self.feedback_fixo = f"Sistema SPDATA está em manutenção travamentos poderão acontecer"
                self.feedback = status
                
                retorno = f"Sistema SPDATA está em manutenção \ntravamentos poderão acontecer \n\n\n{status}"
                
        return retorno 

    def spdata_nao_abre(self):
        try:
            self.conecta_ao_servidor()
        except:
            raise
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
            try:
                self.backend.mapear_spdata()
            except:
                self.feedback_fixo = 'Não foi possível mapear o SPDATA'
                self.feedback = 'Entre em contato com o Administrador'
        except:
            self.feedback_fixo = 'Não foi possível mapear o SPDATA'
            self.feedback = 'Entre em contato com o Administrador'
            pass
        else:
            self.feedback = 'Mapeamento concluído'

    def corrigir_travamento_computador(self, chkdsk = False):
        try:
            self.conecta_ao_servidor()
        except:
            raise
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

    def abrir_glpi(self):
        firefox = webdriver.Firefox(firefox_binary= "C:\Program Files\Mozilla Firefox\geckodriver.exe")
        firefox.get('aroldotourinho.com.br')
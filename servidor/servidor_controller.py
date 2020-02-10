#dev by Jonas Duarte - Duzz System

import configparser
from sesp_update import update
from servidor_model import backend
from socket import *
from time import sleep

class controller():
    def __init__(self):
        self.backend = backend()
        
    def iniciar_servidor(self):
        self.servidor = self.backend.iniciar_servidor()
        
        self.espera_requisicao()

    def reiniciar_servidor(self):
        try:
            print('Reiniciando o servidor SESP')
            self.servidor.close()
        except:
            pass

        self.iniciar_servidor()

    def fechar_conexao(self):
        try:
            self.conexao.close()
        except:
            pass
            
        self.espera_requisicao()

    def espera_requisicao(self):
        try:
            while True:
                self.conexao, id_conexao = self.servidor.accept()

                print(f"Nova Conexão de {id_conexao}")

                while True:
                    requisicao = self.conexao.recv(1024)
                    if not requisicao: 
                        break
                    try:
                        self.conexao.send(self.trata_requisicao(requisicao))
                    except:
                        raise
            self.fechar_conexao()
        except:
            self.reiniciar_servidor()

    def trata_requisicao(self, requisicao):
        requisicao = requisicao.decode('utf-8')
        try:
            requisicao = requisicao.split(';')
        except:
            raise
        return self.armador(requisicao)

    def salvar_log(self, log):
        try:
            self.backend.salvar_log(log)
        except:
            raise
        else:
            return bytes('OK', 'utf-8')

    def armador(self, requisicao):
        if requisicao[0] == 'update':
            retorno = bytes(True, 'utf-8')
            retorno = self.retornar_novo_executavel()
        elif requisicao[0] == '000':
            retorno = self.retornar_versao_vigente()
        elif requisicao[0] == '00':
            retorno = self.salvar_log(requisicao[1])
        elif requisicao[0] == '01':
            retorno = self.data_e_hora_atuais()
        elif requisicao[0] == '02':
            retorno = self.verificar_spdata()
        elif requisicao[0] == '03':
            retorno = self.buscar_ip_maquina(requisicao[1])
        elif requisicao[0] == '04':
            #RETORNAR A IMPRESSORA EM REDE DE ACORDO COM A ETIQUETA E IP DO SERVIDOR
            pass
        elif requisicao[0] == '05':
            pass
            #RETORNAR A IMPRESSORA PADRÃO DE ACORDO COM A ETIQUETA DA MAQUINA
            
        return retorno

    def data_e_hora_atuais(self):
        hora = self.backend.busca_hora_atual()
        data = self.backend.busca_data_atual()

        data_e_hora = f"{data} | {hora}"

        return bytes(data_e_hora, 'utf-8')

    def verificar_spdata(self):
        return self.backend.status_spdata().encode('utf-8')

    def retornar_versao_vigente(self):
        return self.backend.retornar_versao_vigente().encode('utf-8')

    def retornar_novo_executavel(self):
        print('Enviando executável pela conexão')
        return self.backend.retornar_executavel()

    def buscar_ip_maquina(self, numero_inventario):
        try:
            id_maquina = self.backend.buscar_id_maquina(numero_inventario)
        except:
            raise Exception

        return bytes(self.backend.retornar_ip_maquina(id_maquina), 'utf-8')

import os

if __name__ == "__main__":
    main = controller()
    try:
        main.iniciar_servidor()
    except:
        raise



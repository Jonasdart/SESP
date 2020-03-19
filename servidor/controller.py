#dev by Jonas Duarte - Duzz System

import configparser
from model import Backend
from socket import *
from time import sleep
from sesp_update import Update

class Controller():
    def __init__(self):
        self.backend = Backend()
        self.update = Update()
        
        
    def salvar_log(self, log):
        try:
            self.backend.salvar_log(log)
        except:
            raise
        else:
            return bytes('OK', 'utf-8')

    def data_e_hora_atuais(self):
        hora = self.backend.busca_hora_atual()
        data = self.backend.busca_data_atual()

        data_e_hora = f"{data} | {hora}"

        return bytes(data_e_hora, 'utf-8')

    def verificar_spdata(self):
        return self.backend.status_spdata().encode('utf-8')

    def buscar_ip_maquina(self, numero_inventario):
        try:
            id_maquina = self.backend.buscar_id_maquina(numero_inventario)
        except:
            raise Exception

        return bytes(self.backend.retornar_ip_maquina(id_maquina), 'utf-8')

    def retornar_versao_vigente(self):
        return self.update.retornar_versao_vigente()

    def control_update(self, requisicao, item = None, connection = None):
        if requisicao == 'version':
            return bytes(self.update.retornar_versao_vigente(), 'utf-8')
        elif requisicao == 'len':
            return bytes(str(len(self.update.prepara_arquivos())), 'utf-8')

        else:
            if connection is not None:
                print('Atualizando')
                lista_arquivos = self.update.prepara_arquivos()
                if not self.update.bytes_gerados:
                    self.update.organizar_arquivos(lista_arquivos)
                    
                return bytes(self.update.envia_item_por_item(item, connection), 'utf-8')
            else:
                raise Exception('Connection is None')


if __name__ == "__main__":
    main = Controller()
    try:
        main.iniciar_servidor()
    except:
        raise


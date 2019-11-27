from model import backend
from time import sleep
from socket import *

class controller():

    def __init__(self):
        self.backend = backend()
        self.conectado = False

    def inicio(self):
        pass

    def conecta_ao_servidor(self, cont = 3, ip_temp = False, verificou_com_ip_secundario = False):
        if not self.conectado:
            if not ip_temp:
                try:
                    self.conectado = self.backend.conecta_ao_servidor()
                except:
                    if cont is not 0:
                        self.feedback = "Tentando novamente"
                        self.conecta_ao_servidor(cont = cont-1)
                    elif not verificou_com_ip_secundario:
                        self.feedback = "\n\nTentando novamente com o IP temporário"
                        if self.usar_ip_temporario():
                            self.conecta_ao_servidor(ip_temp = True)
                        else:
                            self.conectado = False
                            raise
                    else:
                        self.conectado = False
                        raise
                else:
                    self.conectado = True
                    return
            else:
                try:
                    self.conectado = self.backend.conecta_ao_servidor()
                except:
                    if cont is not 0:
                        self.conecta_ao_servidor(cont = cont-1, ip_temp = True)
                    else:
                        self.conectado = False
                else:
                    self.atualizar_ip()
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
            print("Não foi possível acessar o servidor SESP")
            raise
        else:
            try:
                data_e_hora_atuais = data_e_hora_atuais.decode("utf-8")
            except:
                print("Não foi possível acessar o servidor SESP")
                
            else:
                self.backend.atualizar_horario(data_e_hora_atuais)

    def usar_ip_temporario(self, ip = None):
        if ip is None:
            ip = self.backend.cabecalho_ip_secundario

        msg_confirmacao = self.backend.atualizar_ip(ip)

        return msg_confirmacao

    def atualizar_ip(self):
        try:
            ip = self.backend.buscar_ip(self.backend.cabecalho_etiqueta)
        except:
            raise
        try:
            self.backend.atualizar_ip(ip)
        except:
            raise

    def corrigir_internet(self):
        self.conecta_ao_servidor()
        try:
            self.atualizar_ip()
        except:
            raise
        try:
            self.backend.definir_proxy()
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
            status = status.decode("utf-8")
            if "False" in status:
                return True
            else:
                return f"Sistema SPDATA está em manutenção travamentos poderão acontecer - {status}"

    def spdata_nao_abre(self):
        self.conecta_ao_servidor()
        try:
            self.atualizar_horario()
        except:
            #aqui se não conseguir buscar o horário, o problema provavelmente está na internet
            #portanto devemos chamar a função de correção de internet
            pass
        try:
            mapeamento_msg_confirmacao = self.backend.mapear_spdata()
        except:
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

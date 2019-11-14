from socket import *
from time import sleep
import os

class backend():
    def __init__(self):
        pass

    def conecta_servidor(self, cont = 3, ip_temp = False, verificou_com_ip_secundario = False):
        self.servidor = socket(AF_INET, SOCK_STREAM)
        if not ip_temp:
            try:
                #self.servidor.connect(('192.168.1.0', 50007))
                self.servidor.connect(('localhost', 50007))
            except:
                if cont is not 0:
                    print("\n\nTentando novamente em um segundo e meio")
                    sleep(1.5)
                    self.conecta_servidor(cont = cont-1)
                elif not verificou_com_ip_secundario:
                    self.atualizar_ip(self.cabecalho_ip_secundario)
                    self.conecta_servidor(ip_temp = True)
                else:
                    return False
            else:
                return True
        else:
            try:
                #self.servidor.connect(('192.168.1.0', 50007))
                self.servidor.connect(('localhost', 50007))
            except:
                if cont is not 0:
                    print("\n\nTentando novamente em um segundo e meio com o IP temporário")
                    sleep(1.5)
                    self.conecta_servidor(cont = cont-1, ip_temp = True)
                else:
                    return False
            else:
                ip = self.buscar_ip(self.cabecalho_etiqueta)
                self.atualizar_ip(ip)
                self.conecta_servidor(verificou_com_ip_secundario = True)

    def busca_cabecalho(self):
        info_cabecalho = open("cabecalho.txt", "r")
        cabecalho = info_cabecalho.readlines()

        self.cabecalho_etiqueta = cabecalho[0].split("=")[1]
        self.cabecalho_ip = cabecalho[1].split("=")[1]
        self.cabecalho_ip_secundario = cabecalho[2].split("=")[1]

        print(f"\n\nVocê está usando a máquina etiqueta {self.cabecalho_etiqueta}")
        print(f"O IP padrão da máquina é o {self.cabecalho_ip}")
        print(f"O ip secundário de suporte SESP é o {self.cabecalho_ip_secundario}")

        return cabecalho

    def verificar_spdata(self):
        if self.conecta_servidor():
            try:
                self.servidor.send(b'02')
            except:
                raise
            else:
                status = self.servidor.recv(1024)
                try:
                    self.servidor.close()
                except:
                    pass
                return status
        else:
            raise

    def mapear_spdata(self):
        pass

    def mapear_impressora(self, ip, impressora):
        if self.conecta_servidor():
            try:
                self.servidor.send(b'04')
            except:
                pass
        else:
            print("Não foi possível alcançar o servidor SESP")
    def buscar_impressora_padrao(self, maquina):
        pass

    def definir_impressora_padrao(self, impressora):
        pass

    def criar_atalho_no_desktop(self):
        pass

    def buscar_horario_atual(self):
        if self.conecta_servidor():
            try:
                self.servidor.send(b'01')
            except:
                raise
            else:
                horario_atual = self.servidor.recv(1024)
                try:
                    self.servidor.close()
                except:
                    pass
                return horario_atual
        else:
            print("Não foi possível alcançar o servidor SESP")

    def atualizar_horario(self, horario):
        data, hora = horario.split("|")
        try:
            os.system(f"date {data}")
            os.system(f"time {hora}")
        except:
            pass
    def reiniciar_maquina(self):
        retorno = True

        try:
            os.system("shutdown /r")
        except:
            retorno = False

        return retorno


    def buscar_ip(self, maquina):
        pass

    def atualizar_ip(self, ip):
        pass

"""teste = backend()
teste.reiniciar_maquina()"""
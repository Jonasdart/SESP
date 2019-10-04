from socket import *
from time import sleep
import os

class backend():

    def __init__(self):
        pass

    def conecta_servidor(self):
        self.servidor = socket(AF_INET, SOCK_STREAM)
        try:
            #self.servidor.connect(('192.168.0.22', 50007))
            self.servidor.connect(('localhost', 50007))
        except:
            print("\n\nTentando novamente em um segundo e meio")
            sleep(1.5)
            self.conecta_servidor()
        else:
            return True

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

    def mapear_spdata(self):
        pass

    def mapear_impressora(self, impressora):
        pass

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
            print("Deu erro")


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
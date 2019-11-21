from socket import *
from time import sleep
import os
import subprocess

class backend():
    def __init__(self):
        self.busca_cabecalho()
        self.conectado = False

    def conecta_servidor(self, cont = 3, ip_temp = False, verificou_com_ip_secundario = False):
        self.servidor = socket(AF_INET, SOCK_STREAM)

        if not ip_temp:
            try:
                #self.servidor.connect(('192.168.1.0', 50007))
                self.servidor.connect(('localhost', 50007))
            except:
                if cont is not 0:
                    print("\n\nTentando novamente")
                    self.conecta_servidor(cont = cont-1)
                elif not verificou_com_ip_secundario:
                    print("\n\nTentando novamente com o IP temporário")
                    if self.atualizar_ip(self.cabecalho_ip_secundario):
                        self.conecta_servidor(ip_temp = True)
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
                #self.servidor.connect(('192.168.1.0', 50007))
                self.servidor.connect(('localhost', 50007))
            except:
                if cont is not 0:
                    print("\n\nTentando novamente com o IP temporário")
                    self.conecta_servidor(cont = cont-1, ip_temp = True)
                else:
                    self.conectado = False
            else:
                ip = self.buscar_ip(self.cabecalho_etiqueta)
                self.atualizar_ip(ip)
                self.conecta_servidor(verificou_com_ip_secundario = True)

    def atualiza_cabecalho(self, ip = None, etiqueta = None):
        pass

    def busca_cabecalho(self):
        info_cabecalho = open("cabecalho.txt", "r")
        cabecalho = info_cabecalho.readlines()

        self.cabecalho_etiqueta = cabecalho[0].split("=")[1].strip()
        self.cabecalho_ip = cabecalho[1].split("=")[1].strip()
        self.cabecalho_ip_secundario = cabecalho[2].split("=")[1].strip()
        self.cabecalho_excessoes = cabecalho[3].split("=")[1].strip()
        return cabecalho

    def verificar_spdata(self):
        if not self.conectado:
            try:
                self.conecta_servidor()
            except:
                raise
            else:
                self.verificar_spdata()
        else:
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
        try:
            os.system("net use I: /delete >nul")
        except:
            pass
        try:
            os.system("net use I: \\\\192.168.0.251\\spdatai /user:192.168.0.251\\administrador 123456 /persistent:yes")
        except:
            return False
        else:
            return True



    def mapear_impressora(self, ip, impressora):
        if not self.conectado:
            try:
                self.conecta_servidor()
            except:
                raise
            else:
                self.mapear_impressora(ip, impressora)
        else:
            pass

    def buscar_impressora_padrao(self, maquina):
        pass

    def definir_impressora_padrao(self, impressora):
        pass

    def criar_atalho_no_desktop(self):
        pass

    def buscar_horario_atual(self):

        if not self.conectado:
            try:
                self.conecta_servidor()
            except:
                raise
            else:
                self.buscar_horario_atual()
        else:
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

    def atualizar_horario(self, horario):
        data, hora = horario.split("|")
        try:
            os.system(f"date {data}")
            os.system(f"time {hora}")
        except:
            pass

    def reiniciar_maquina(self):
        try:
            os.system("shutdown /r")
        except:
            return False
        else:
            return True

    def buscar_ip(self, maquina):
        if not self.conectado:
            try:
                self.conecta_servidor()
            except:
                raise
            else:
                self.buscar_ip(maquina)
        else:
            try:
                requisicao = f'03-{maquina}'
                self.servidor.send(bytes(requisicao, 'utf-8'))
            except:
                raise
            else:
                ip = self.servidor.recv(1024)
                try:
                    self.servidor.close()
                except:
                    pass
                else:
                    self.conectado = False
                print(ip)
                return ip

    def atualizar_ip(self, ip):
        try:
            os.system(f'netsh int ip set address name="Conexão Local" source=static {ip} 255.255.255.0 192.168.0.1 1')
            os.system('netsh int ip set dns "Conexão Local" static 8.8.8.8')
            os.system('netsh int ip set wins "Conexão Local" static 8.8.4.4')
        except:
            return False
        else:
            return True

    def definir_proxy(self):
        try:
            os.system('REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f')
            os.system('REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d 192.168.0.1:8080 /f')
            os.system(f'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyOverride /t REG_SZ /d "{self.cabecalho_excessoes}" /f')
        except:
            pass
"""teste = backend()
teste.reiniciar_maquina()"""
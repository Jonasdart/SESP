from socket import *
from time import sleep
import os
import subprocess

class backend():
    def __init__(self):
        self.busca_cabecalho()
        self.conectado = False

    def conecta_ao_servidor(self):
        ip, porta = self.ip_servidor_sesp()
        if not self.conectado:
            try:
                self.servidor.close()
            except:
                pass
            try:
                self.servidor = socket(AF_INET, SOCK_STREAM)
                #self.servidor.connect(('192.168.0.69', 50007))
                self.servidor.connect((f'{ip}', porta))
            except:
                raise
            else:
                return True
        else:
            return True

    def encerrar_conexao(self):
        try:
            self.servidor.close()
        except:
            pass
        else:
            self.conectado = False

    def ip_servidor_sesp(self):
        arq = open('sesp.txt', 'r')
        info_servidor = arq.readlines()
        arq.close()

        ip = info_servidor[0].split('=')[1].strip()
        porta = int(info_servidor[1].split('=')[1].strip())
        
        return ip, porta


    def busca_cabecalho(self):
        info_cabecalho = open("cabecalho.txt", "r")
        cabecalho = info_cabecalho.readlines()
        info_cabecalho.close()

        self.cabecalho_etiqueta = cabecalho[0].split("=")[1].strip()
        self.cabecalho_ip = cabecalho[1].split("=")[1].strip()
        self.cabecalho_ip_secundario = cabecalho[2].split("=")[1].strip()
        self.cabecalho_excessoes = cabecalho[3].split("=")[1].strip()
        return cabecalho

    def atualiza_cabecalho(self, ip = None, etiqueta = None, ip_secundario = None):
        if ip is not None:
            cabecalho_antigo = open("cabecalho.txt", "r")
            linhas_cabecalho_antigo = cabecalho_antigo.readlines()
            cabecalho_antigo.close()

            texto_ip = linhas_cabecalho_antigo[1].split('=')

            novo_cabecalho = open("cabecalho.txt", "w")
            contador = 0

            for linha in linhas_cabecalho_antigo:
                if contador is not 1:
                    novo_cabecalho.write(linha)
                else:
                    novo_cabecalho.write(f'{texto_ip[0]}= {ip}\n')
                contador += 1
            novo_cabecalho.close()

    def verificar_spdata(self):
        try:
            self.servidor.send(b'02')
        except:
            raise
        else:
            status = self.servidor.recv(1024)
            try:
                self.encerrar_conexao()
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
        pass

    def buscar_impressora_padrao(self, maquina):
        pass

    def definir_impressora_padrao(self, impressora):
        pass

    def criar_atalho_no_desktop(self):
        pass

    def buscar_horario_atual(self):
        try:
            self.servidor.send(b'01')
        except:
            raise
        else:
            horario_atual = self.servidor.recv(1024)
            try:
                self.encerrar_conexao()
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

    def realizar_correcao_de_disco(self):
        pass

    def reiniciar_maquina(self):
        try:
            os.system("shutdown /r")
        except:
            return False
        else:
            return True

    def buscar_ip(self, maquina):
        try:
            requisicao = f'03-{maquina}'
            self.servidor.send(bytes(requisicao, 'utf-8'))
        except:
            raise
        else:
            ip = self.servidor.recv(1024)
            ip = ip.decode('utf-8')
            try:
                self.encerrar_conexao()
            except:
                pass
            
            self.atualiza_cabecalho(ip = ip)

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
            
if __name__ == "__main__":
    main = backend()
    try:
        main.servidor_sesp()
    except:
        raise
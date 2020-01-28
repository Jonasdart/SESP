from socket import *
from datetime import datetime
from time import sleep
import os
import subprocess
import platform
import configparser

class backend():
    def __init__(self):
        self.busca_cabecalho()
        self.conectado = False

    def conecta_ao_servidor(self):
        ip, porta = self.ip_servidor_sesp()
        if not self.conectado:
            self.encerrar_conexao()
            try:
                self.servidor = socket(AF_INET, SOCK_STREAM)
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
        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        porta = int(config.get('ConfigServer', 'Porta'))
        ip = config.get('ConfigServer', 'IpServer')
        
        return ip, porta

    def gerar_log(self, procedimento):
        info_computador = self.busca_info_computador()
        nome_computador = info_computador['nome']
        sistema_operacional = info_computador['so']
        log = f'{nome_computador}|{self.cabecalho_etiqueta}\t{self.cabecalho_ip} | {sistema_operacional} | {procedimento}'
        print(log)
        return log

    def enviar_log(self, log):
        try:
            log = f'00;{log}'
            self.servidor.send(bytes(log, 'utf-8'))
        except:
            raise
        else:
            try:
                self.encerrar_conexao()
            except:
                pass

    def busca_info_computador(self):
        nome_pc = platform.node()
        sistema_operacional_pc = platform.platform()

        return {'nome': nome_pc, 'so': sistema_operacional_pc}

    def busca_cabecalho(self):
        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        self.cabecalho_etiqueta = config.get('Cabecalho', 'EtiquetaPC')
        self.cabecalho_ip = config.get('Cabecalho', 'IpMaquina')
        self.cabecalho_excessoes = config.get('Cabecalho', 'ExcessõesProxy')
        
        return True

    def atualiza_cabecalho(self, ip = None, etiqueta = None, ip_secundario = None):
        if ip is not None:
            with open('cabecalho.cfg') as cabecalho_antigo:
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
            raise
        else:
            return



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
            print(horario_atual)
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
            requisicao = f'03;{maquina}'
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
            if ip is not None:
                self.atualiza_cabecalho(ip = ip)
                return ip
            else:
                raise

    def atualizar_ip(self, ip):
        try:
            os.system(f'netsh int ip set address name="Conexão local" source=static {ip} 255.255.255.0 192.168.0.1 1')
            os.system('netsh int ip set dns "Conexão Local" static 8.8.8.8')
            os.system('netsh int ip set wins "Conexão Local" static 8.8.4.4')
        except:
            raise

    def definir_proxy(self):
        try:
            os.system('REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f')
            os.system('REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d 192.168.0.1:8080 /f')
            os.system(f'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyOverride /t REG_SZ /d "{self.cabecalho_excessoes}" /f')
        except:
            pass

    def definir_papel_parede(self):
        pass
            
if __name__ == "__main__":
    main = backend()
    try:
        main.servidor_sesp()
    except:
        raise
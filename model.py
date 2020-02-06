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

        porta = int(config.get('config_server', 'porta'))
        ip = config.get('config_server', 'ip_server')
        
        return ip, porta

    def gerar_log(self, procedimento):
        info_pc = self.busca_cabecalho()
        
        nome = info_pc.get('NomePc')
        etiqueta = info_pc.get('CabecalhoEtiqueta')
        ip = info_pc.get('CabecalhoIp')
        sistema_operacional = info_pc.get('SistemaOperacional')
        
        log = f'{nome}|{etiqueta}\t{ip} | {sistema_operacional} | {procedimento}'
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

        return {'nome': nome_pc, 
                'so': sistema_operacional_pc}

    def busca_cabecalho(self):
        nome = self.busca_info_computador()['nome'] 
        sistema_operacional = self.busca_info_computador()['so']

        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        etiqueta = config.get('cabecalho', 'etiqueta_pc')
        ip = config.get('cabecalho', 'ip_maquina')
        excessoes_proxy = config.get('cabecalho', 'excessoes_proxy')
        
        return {'CabecalhoEtiqueta': etiqueta, 
                'CabecalhoIp' : ip,
                'ExcessoesProxy' : excessoes_proxy,
                'NomePc' : nome,
                'SistemaOperacional' : sistema_operacional}

    def atualiza_cabecalho(self, ip = None, etiqueta = None):
        parser = configparser.ConfigParser()
        parser.read('sesp.cfg')
        if ip is not None:
            parser.set('cabecalho', 'ip', ip)
        
        if etiqueta is not None:
            parser.set('cabecalho', 'etiqueta', etiqueta)
                
        with open('cabecalho.cfg', 'w') as cfg:
            parser.write(cfg)

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
        """
        Recebe um horário → data | hora
        """
        data, hora = horario.split("|")
        try:
            os.system(f"date {data}")
            os.system(f"time {hora}")
        except:
            pass

    def agendar_correcao_de_disco(self):
        """
        Envia comando ao prompt de comando para agendar checagem de disco
        após o próximo reinício
        """
        pass

    def reiniciar_maquina(self):
        """
        Envia comando ao prompt de comando do computador 
        para agendar o reinício do mesmo para após um minuto.
        """
        try:
            os.system("shutdown /r")
        except:
            return False
        else:
            return True

    def buscar_ip(self, maquina):
        """
        Recebe a etiqueta (Número de inventário) do computador.
        Retorna o endereço de IP da mesma, após solicitar ao servidor
        """
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
                raise Exception('IP Inválido')

    def atualizar_ip(self, ip):
        """
        Recebe um endereço de IP.
        Configura o IP utilizando o recebido.
        Configura o DNS e WINS utilizando o do google.
        """
        try:
            os.system(f'netsh int ip set address name="Conexão local" source=static {ip} 255.255.255.0 192.168.0.1 1')
            os.system('netsh int ip set dns "Conexão Local" static 8.8.8.8')
            os.system('netsh int ip set wins "Conexão Local" static 8.8.4.4')
        except:
            raise

    def definir_proxy(self):
        """
        Define as excessões de proxy, que podem ser configuradas
        no sesp.cfg entre aspas '' e separadas por ';'
        """
        excessoes = self.busca_cabecalho()['ExcessoesProxy']
        excessoes = excessoes.split('"')[1]

        try:
            os.system('REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f')
            os.system('REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d 192.168.0.1:8080 /f')
            os.system(f'REG ADD "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyOverride /t REG_SZ /d "{self.cabecalho_excessoes}" /f')
        except:
            pass

    def buscar_papel_parede_por_grupo(self, grupo):
        """
        Recebe um grupo, padrão GLPI
        Retorna um diretório de imagem
        """
        pass

    def definir_papel_parede(self, caminho_imagem):
        """
        Recebe o caminho de diretório de alguma imagem
        e a define como papel de parede.
        """
        pass

    def definir_nome_computador(self):
        """
        Define o nome do computador para a etiqueta do computador, 
        sendo necessário ter um prefixo
        que é definido no [parametros] do config.cfg
        """
        parser = configparser.ConfigParser()
        parser.read('config.cfg')

        prefixo_nome = parser.get('parametros', 'prefixo_nome')
    
        nome_atual = self.busca_info_computador()['nome']
        novo_nome = self.busca_cabecalho()['CabecalhoEtiqueta']
        novo_nome = f'{prefixo_nome}-{novo_nome}'
        acao = f'wmic computersystem where name="{nome_atual}" rename "{novo_nome}"'

        os.system(acao)

    def clear(self):
        """
        Utilizado para melhor experiência nos testes
        """
        os.system('cls')
            
if __name__ == "__main__":
    main = backend()
    try:
        main.servidor_sesp()
    except:
        raise
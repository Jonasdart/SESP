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

    def gerar_log(self, procedimento):
        """
        Gera um texto de log padronizado por:
        Nome PC|Num.Inventario IP | Sistema Operacional | Sucesso/falha :: Procedimento

        retorna o log gerado
        """
        info_pc = self.busca_cabecalho()
        
        nome = info_pc.get('NomePc')
        etiqueta = info_pc.get('CabecalhoEtiqueta')
        ip = info_pc.get('CabecalhoIp')
        sistema_operacional = info_pc.get('SistemaOperacional')
        
        log = f'{nome}|{etiqueta}\t{ip} | {sistema_operacional} | {procedimento}'
        print(log)
        return log

    def enviar_log(self, log):
        """
        Recebe um texto de log e o envia ao servidor para ser guardado no diretório de log
        """
        try:
            log = f'00;{log}'
            self.servidor.send(bytes(log, 'utf-8'))
        except:
            raise
        else:
            try:
                self.encerrar_conexao()
            except:
                raise Exception('Falha ao enviar o LOG ao servidor')

    def busca_info_computador(self):
        """
        Retorna as informações do computador em um dicionário

        'nome' = Nome do computador,
        'so' = Sistema Operacional do Computador
        """
        nome_pc = platform.node()
        sistema_operacional_pc = platform.platform()

        return {'nome': nome_pc, 
                'so': sistema_operacional_pc}

    def busca_cabecalho(self):
        """
        Busca o cabeçalho do computador no arquivo de configuração sesp.cfg
        Retorna o cabeçalho, em um dicionário:
        'CabecalhoEtiqueta' : Etiqueta do Computador
        'NomePc' : Nome do Computador
        'Sistema Operacional' : Sistema Operacional do Computador
        'CabecalhoIp' : IP do Computador
        'ExcessoesProxy' : Excessões do proxy do computador
        """
        nome = self.busca_info_computador()['nome'] 
        sistema_operacional = self.busca_info_computador()['so']

        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        etiqueta = config.get('cabecalho', 'etiqueta_pc')
        ip = config.get('cabecalho', 'ip_maquina')
        excessoes_proxy = config.get('cabecalho', 'excessoes_proxy')
        
        return {'CabecalhoEtiqueta': etiqueta,
                'NomePc' : nome,
                'SistemaOperacional' : sistema_operacional,
                'CabecalhoIp' : ip,
                'ExcessoesProxy' : excessoes_proxy
                }

    def atualiza_cabecalho(self, ip = None, etiqueta = None):
        """
        Atualiza o cabeçalho no arquivo de configuração conforme informações recebidas como argumentos.
        Podendo receber o novo IP e/ou nova etiqueta
        """
        parser = configparser.ConfigParser()
        parser.read('sesp.cfg')
        if ip is not None:
            parser.set('cabecalho', 'ip', ip)
        
        if etiqueta is not None:
            parser.set('cabecalho', 'etiqueta', etiqueta)
                
        with open('cabecalho.cfg', 'w') as cfg:
            parser.write(cfg)

    def verificar_spdata(self):
        """
        Envia comando ao Servidor SESP, recebe e retorna status de funcionamento do SPDATA
        """
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
        """
        Envia comando ao CMD para que mapeie a pasta do SPDATA
        """
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
        """
        Padroniza o horário;
        Envia comando ao servidor SESP, recebe e retorna data e hora atuais do servidor.
        """
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
        """
        Recebe um horário → data | hora
        Envia comando ao CMD que define o horário para o recebido
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
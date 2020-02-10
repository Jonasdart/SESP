from socket import *
import configparser
from os import system


class update():
    def __init__(self):
        self.conectado = False

    def ip_servidor_sesp(self):
        """
        Busca e retorna as configurações de conexão do servidor SESP
        retorno = [ip, porta]
        """
        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        porta = int(config.get('config_server', 'porta'))
        ip = config.get('config_server', 'ip_server')
        
        return ip, porta

    def conecta_ao_servidor(self):
        """
        Faz conexão com o servidor SESP
        Retorna Erro ou True
        """
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
        """
        Encerra a conexão com o servidor SESP
        """
        try:
            self.servidor.close()
        except:
            pass
        else:
            self.conectado = False

    def identificar_versao_atual(self):
        """
        Busca a versão atual do SESP presente no arquivo de configuração sesp.cfg
        retorno = Versão 
        """
        
        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        versao_atual = config.get('version_sesp', 'version')

        return versao_atual

    def identificar_versao_vigente(self):
        """
        Identifica a versão atual do sistema
        retorna a identificação da mesma
        """
        self.conecta_ao_servidor()
        try:
            self.servidor.send(b'000')
        except:
            raise Exception('Não foi possível enviar requisição ao servidor SESP')
        else:
            versao_vigente = self.servidor.recv(1024)

        return versao_vigente

    def atualiza(self):
        versao_atual = self.identificar_versao_atual()
        versao_vigente = self.identificar_versao_vigente().decode()
        print(versao_atual)
        print(versao_vigente)

        if versao_atual is not versao_vigente:
            self.salva_novos_arquivos(self.busca_novos_arquivos())
        else:
            return True

    def busca_novos_arquivos(self):
        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        tam_max = config.get('config_server', 'tam_max')

        self.conecta_ao_servidor()
        try:
            self.servidor.send(b'update')
        except:
            raise Exception('Não foi possível enviar requisição ao servidor SESP')
        else:
            bytes_arquivo = self.servidor.recv(int(tam_max))

        print(len(bytes_arquivo))
        return bytes_arquivo

    def salva_novos_arquivos(self, bytes_arquivo):
        with open('sesp.exe', 'wb') as sesp:
            sesp.write(bytes_arquivo)

        return True
    
    def clear(self):
        system('cls')
        system('clear')
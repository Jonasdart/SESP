from socket import *
import configparser
from os import system


class update():
    def __init__(self):
        self.conectado = bool()

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
                self.conectado = True
                return True
        else:
            self.conectado = True
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
        
        return True

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
        self.conectado = self.conecta_ao_servidor()
        try:
            self.servidor.send(b'000')
        except:
            raise #Exception('Não foi possível enviar requisição ao servidor SESP')
        else:
            versao_vigente = self.servidor.recv(1024)

        return versao_vigente

    def atualiza(self):
        versao_atual = self.identificar_versao_atual()
        versao_vigente = self.identificar_versao_vigente().decode('utf-8')

        print(versao_atual)
        print(versao_vigente)

        if versao_atual is not versao_vigente:
            self.recebe_novos_arquivos()
        else:
            return True

    def verifica_tamanho_atualizacao(self):
        self.conectado = self.conecta_ao_servidor()
        try:
            self.servidor.send(b'len')
        except:
            raise Exception('Não foi possível enviar requisição ao servidor SESP')
        else:
            tamanho_att = self.servidor.recv(1024)

        return int(tamanho_att.decode('utf-8'))

    def recebe_novos_arquivos(self):
        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        tamanho_maximo = config.get('config_server', 'tam_max')
        tamanho_maximo = int(tamanho_maximo)

        tamanho_att = self.verifica_tamanho_atualizacao()

        self.conectado = self.conecta_ao_servidor()

        for i in range(tamanho_att):
            try:
                texto_requisicao = f'update;{i}'
                self.servidor.send(bytes(texto_requisicao, 'utf-8'))
            except:
                raise
                #raise Exception('Não foi possível enviar requisição ao servidor SESP')
            else:
                self.salva_novos_arquivos(tamanho_maximo)

    def salva_novos_arquivos(self, tamanho_maximo):
        arquivo = self.servidor.recv(tamanho_maximo)
        arquivo = self.trata_arquivo(arquivo)

        with open(arquivo.get('Diretorio'), 'wb') as arq:
            arq.write(arquivo.get('Dados'))

        return True
    
    def trata_arquivo(self, arquivo):
        
        cabecalho_arquivo = arquivo.split(b'-*-*-')
        cabecalho_arquivo_decoded = cabecalho_arquivo[1].decode('utf-8').split("'")[1]
        print(cabecalho_arquivo_decoded)

        nome_arquivo, pasta_arquivo = cabecalho_arquivo_decoded.split('\\\\')[1], cabecalho_arquivo_decoded.split('/')
        print(f'EU SOU A PASTA ARQUIVO {pasta_arquivo}')
        pasta_arquivo = pasta_arquivo[len(pasta_arquivo)-1].split('\\\\')[0]
        print(nome_arquivo)
        print(pasta_arquivo)
        
        if pasta_arquivo[len(pasta_arquivo)-2] is b'SESP':
            print(pasta_arquivo[len(pasta_arquivo)-2])
            pasta_arquivo = 'SESP/' + pasta_arquivo[len(pasta_arquivo)-1]

        else:
            pasta_arquivo = ''

        arquivo = {
            'Pasta': pasta_arquivo,
            'Nome' : nome_arquivo,
            'Diretorio' : pasta_arquivo + nome_arquivo,
            'Dados' : cabecalho_arquivo[2]
        }

        print(arquivo)

        return arquivo

    def clear(self):
        system('cls')
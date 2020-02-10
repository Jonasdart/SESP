import configparser
import servidor_model
import os

class update():
    #def __init__(self, conexao):
     #   self.conexao = conexao

    def retornar_versao_vigente(self):
        """
        Busca a versão atual do SESP presente no arquivo de configuração sesp.cfg
        retorno = Versão 
        """
        
        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        versao_atual = config.get('version_sesp', 'version')

        return versao_atual

    def listar_arquivos_atualizados(self):
        config = configparser.ConfigParser()
        config.read('sesp.cfg')
        pasta = config.get('version_sesp', 'path_atualizacao')

        caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
        itens_pasta = [arq for arq in caminhos]
        arquivos = []

        for item in itens_pasta:
            arquivos.append(self.trata_caminho_arquivo(item))

        return arquivos

    def trata_caminho_arquivo(self, caminho):
        split_caminho = caminho.split('\\')
        caminho = split_caminho[0] + '/' + split_caminho[1]

        return caminho
    
    def gera_nome_arquivo(self, arquivo):
        print(arquivo)
        split_nome_arq = arquivo.split('Update/')
        print(split_nome_arq)
        nome_arq = split_nome_arq[1]

        return nome_arq
        
    def retornar_arquivos(self, arquivos):
        for arquivo in arquivos:
            print(arquivo)
            print(self.gera_nome_arquivo(arquivo))
            #b_arquivo = bytes(arquivo, 'utf-8')

            #self.conexao.send(f'N-{b_arquivo}')

            #with open(arquivo, 'rb') as arq:
                #bytes_executavel = arq.read()

            #self.conexao.send(bytes_executavel)
            
        return True
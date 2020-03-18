import configparser
import servidor_model
import os

class update():
    def __init__(self, conexao):
        self.conexao = conexao
        self.retorno = []
        self.bytes_gerados = False
        self.gerado = False

    def retornar_versao_vigente(self):
        """
        Busca a versão atual do SESP presente no arquivo de configuração sesp.cfg
        retorno = Versão 
        """
        
        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        versao_atual = config.get('version_sesp', 'version')

        return str(versao_atual)

    def buscar_path_atualizacao(self):
        config = configparser.ConfigParser()
        config.read('sesp.cfg')
        path = config.get('version_sesp', 'path_atualizacao')

        return path

    def trata_caminho_arquivo(self, caminho):
        split_caminho = caminho.split('\\')
        caminho = split_caminho[0] + '/' + split_caminho[1]

        return caminho
    
    def gera_nome_arquivo(self, path):
        pastas = [path]
        caminhos = []
        self.arquivos = []
        for pasta in pastas:
            for nome in os.listdir(pasta):
                caminhos.append(os.path.join(pasta, nome))
            
            for caminho in caminhos:
                if os.path.isfile(caminho):
                    if caminho not in self.arquivos:
                        self.arquivos.append(caminho)
                else:
                    pasta = caminho.split('\\')[0] + '/' + caminho.split('\\')[1]
                    if pasta not in pastas:
                        pastas.append(pasta)
        self.gerado = True
        return self.arquivos
        
    def organizar_arquivos(self, arquivos):
        
        for arquivo in arquivos:
            b_arquivo = bytes(arquivo, 'utf-8')
            envio = bytes(f'-*-*-{b_arquivo}-*-*-', 'utf-8')
            
            path_arquivo = self.trata_caminho_arquivo(arquivo)
            print('Copiando ' + path_arquivo)

            with open(path_arquivo, 'rb') as arq:
                bytes_executavel = arq.read()

            self.retorno.append(envio + bytes_executavel)

        self.bytes_gerados = True
        return self.retorno
        
    def envia_item_por_item(self, indice):
        indice = int(indice)

        self.conexao.send(self.retorno[indice])
            
        return ''

    def prepara_arquivos(self):
        if not self.gerado:
            path = self.buscar_path_atualizacao()
            lista_arquivos = self.gera_nome_arquivo(path)
        else:
            lista_arquivos = self.arquivos

        return lista_arquivos

    def controller(self, requisicao, item = None):
        if requisicao == '00':
            return bytes(self.retornar_versao_vigente(), 'utf-8')
        elif requisicao == 'len':
                        
            return bytes(str(len(self.prepara_arquivos())), 'utf-8')

        else:
            print('Atualizando')
            lista_arquivos = self.prepara_arquivos()
            if not self.bytes_gerados:
                self.organizar_arquivos(lista_arquivos)
                
            return bytes(self.envia_item_por_item(item), 'utf-8')

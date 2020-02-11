import configparser
import servidor_model
import os

class update():
    def __init__(self, conexao):
        print('update')
        self.conexao = conexao

    def retornar_versao_vigente(self):
        """
        Busca a versão atual do SESP presente no arquivo de configuração sesp.cfg
        retorno = Versão 
        """
        
        config = configparser.ConfigParser()
        config.read('sesp.cfg')

        versao_atual = config.get('version_sesp', 'version')

        return versao_atual

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
        subpastas = []
        arquivos = []
        for pasta in pastas:
            
            for nome in os.listdir(pasta):
                caminhos.append(os.path.join(pasta, nome))
            
            for caminho in caminhos:
                
                if os.path.isfile(caminho):
                    if caminho not in arquivos:
                        arquivos.append(caminho)
                else:
                    if caminho in pastas:
                        continue
                    else:
                        subpastas.append(caminho)
            
            for pasta in subpastas:
                pasta = pasta.split('\\')[0] + '/' + pasta.split('\\')[1]
                if pasta in pastas:
                    continue
                else:
                    pastas.append(pasta)

        return arquivos
        
    def retornar_arquivos(self, arquivos):
        for arquivo in arquivos:
            print(bytes(arquivo, 'utf-8'))
            b_arquivo = bytes(arquivo, 'utf-8')
            envio = f'N-{b_arquivo}'
            
            self.conexao.send(bytes(envio, 'utf-8'))

            path_arquivo = self.trata_caminho_arquivo(arquivo)

            with open(path_arquivo, 'rb') as arq:
                bytes_executavel = arq.read()

            self.conexao.send(bytes_executavel)
            
        return True

    def controller(self, requisicao):
        if requisicao == '00':
            return self.retornar_versao_vigente()
        else:
            path = self.buscar_path_atualizacao()
            lista_arquivos  = self.gera_nome_arquivo(path)
            
            return self.retornar_arquivos(lista_arquivos) 
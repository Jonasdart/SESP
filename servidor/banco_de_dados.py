import MySQLdb as mdb
import configparser
from mysql_manager import gera_query

class glpi():
    def __init__(self):
        self.gerador_de_query = gera_query()
        self.conectado = False

    def conecta(self):
        self.credenciais = self.credencia()
        try:
            self.banco = mdb.connect(self.credenciais[0], self.credenciais[1], 
                self.credenciais[2], self.credenciais[3])
        except:
            self.conectado = False
            raise
        else:
            self.cursor = self.banco.cursor()
            self.conectado = True

    def credencia(self):
        """
        Utiliza as informações presentes no glpi.cfg para\n
        retorná-las em forma de lista como credenciais

        Retorno -> Lista:\n
        [0] IP banco, [1] Usuario Banco\n
        [2] Senha Usuario, [3] Nome Banco
        """
        config = configparser.ConfigParser()
        config.read('glpi.cfg')

        caminho_bd = config.get('Banco', 'CaminhoBD')
        nome_bd = config.get('Banco', 'NomeBD')
        usuario = config.get('Credenciais', 'Usuario')
        senha = config.get('Credenciais', 'Senha')

        return [caminho_bd, usuario, senha, nome_bd]

    def buscar_info_maquina(self, maquina):
        self.conecta()
        query = self.gerador_de_query.buscar_dados_da_tabela(tabela = "glpi_ipaddresses", 
            where = True, coluna_verificacao = ["mainitems_id", "mainitemtype"], valor_where = [maquina, "Computer"])

        return self.commit_com_retorno(query)
        
    def commit_sem_retorno(self, query):
        if not self.conectado:
            try:
                self.conecta()
            except:
                raise
            else:
                self.commit_sem_retorno(query)
        else:  
            try:
                self.cursor.execute(query)
            except:
                raise
            else:
                self.banco.commit()
                return True

    def commit_com_retorno(self, query):
        if not self.conectado:
            try:
                self.conecta()
            except:
                raise
            else:
                self.commit_com_retorno(query)
        else:  
            try:
                self.cursor.execute(query)
            except:
                raise
            else:
                return self.cursor.fetchall()
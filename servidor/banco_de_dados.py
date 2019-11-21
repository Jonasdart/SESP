import MySQLdb as mdb
from mysql_manager import gera_query

class glpi():
    def __init__(self):
        self.gerador_de_query = gera_query()
        self.conectado = False

    def conecta(self):
        self.credenciais = self.credencia()
        print(self.credenciais)
        try:
            self.banco = mdb.connect(self.credenciais[0], self.credenciais[1], 
                self.credenciais[2], self.credenciais[3])
        except:
            print("Tentando novamente")
            self.conecta()
        else:
            print("Conectado")
            self.cursor = self.banco.cursor()
            self.conectado = True
    def credencia(self):
        try:
            retorno_credenciais.clear()
        except:
            pass

        arquivo_credenciais = open("credenciais.txt", "r")
        credenciais = arquivo_credenciais.readlines()
        retorno_credenciais = list()

        for item in credenciais:
            retorno_credenciais.append(item.split('=')[1].strip())

        return retorno_credenciais

    def buscar_info_maquina(self, maquina):
        if not self.conectado:
            print("Tentando conectar ao GLPI...")
            self.conecta()

        query = self.gerador_de_query.buscar_dados_da_tabela(tabela = "glpi_ipaddresses", 
            where = True, coluna_verificacao = ["mainitems_id", "mainitemtype"], valor_where = [maquina, "Computer"])

        return self.commit_com_retorno(query)
        
    def commit_sem_retorno(self, query):
        try:
            self.cursor.execute(query)
        except:
            raise
        else:
            self.banco.commit()
            return True

    def commit_com_retorno(self, query):
        try:
            self.cursor.execute(query)
        except:
            raise
        else:
            return self.cursor.fetchall()
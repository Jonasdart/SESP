import MySQLdb as mdb
from mysql_manager import gera_query

class glpi():
	def __init__(self):
		self.gerador_de_query = gera_query()
		self.conectado = False

	def conecta(self)
		self.credenciais = self.credencia()
		try:
			self.banco = mdb.connect(self.credenciais[0], self.credenciais[1], 
				self.credenciais[2], self.credenciais[3])
		except:
			pass
		else:
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

		for x in range(len(credenciais)):
			retorno_credenciais.append(credenciais[x].split("="))

		return retorno_credenciais

	def buscar_ip_da_maquina(self, maquina):
		if not self.conectado:
			self.conecta()

		query = self.gerador_de_query.buscar_dados_da_tabela()
		
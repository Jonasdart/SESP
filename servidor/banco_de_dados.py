import MySQLdb as mdb

class glpi():
	def __init__(self):
		self.credencia()
		try:
			self.banco = mdb.connect("caminho_do_bd", self.credenciais_usuario, self.credenciais_senha, "nome_do_bd")
		except:
			pass
		else:
			self.cursor = self.banco.cursor()
	def credencia(self):
		arquivo_credenciais = open("credenciais.txt", "r")
		credenciais = arquivo_credenciais.readlines()
		self.credenciais_usuario = credenciais[0].split("=")[1]
		self.credenciais_senha = credenciais[1].split("=")[1]

	def buscar_ip_da_maquina(self, maquina):
		pass
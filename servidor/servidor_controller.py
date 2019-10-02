from servidor_model import backend
from socket import *

class controller():
    def __init__(self):
        self.backend = backend()
        self.endereco = 'localhost'
        self.porta = 50007

    def iniciar_servidor(self):
        self.servidor = socket(AF_INET, SOCK_STREAM)
        self.servidor.bind((self.endereco, self.porta))

        self.servidor.listen(5)

        self.espera_requisicao()

    def espera_requisicao(self):
        while True:
            endereco, conexao = self.servidor.accept()

            print(f"Nova Conexão de {conexao}")

            while True:
                requisicao = endereco.recv(1024)
                if not requisicao: 
                    break

                endereco.send(self.trata_requisicao(requisicao))

            endereco.close()

    def trata_requisicao(self, requisicao):
        requisicao = requisicao.decode("utf-8")

        return self.armador(f"{requisicao}")

    def armador(self, requisicao):
        if requisicao == '01':
            return self.data_e_hora_atuais()
        elif requisicao == '02':
            pass
        elif requisicao == '03':
            pass
        elif requisicao == '04':
            pass

    def data_e_hora_atuais(self):
        hora = self.backend.busca_hora_atual()
        data = self.backend.busca_data_atual()

        data_e_hora = f"{data} | {hora}"

        return bytes(data_e_hora, 'utf-8')

if __name__ == "__main__":
    main = controller()
    main.iniciar_servidor()

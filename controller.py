from model import backend
from socket import *

class controller():

    def __init__(self):
        self.backend = backend()
        self.servidor = socket(AF_INET, SOCK_STREAM)

    def conecta_servidor(self):
        try:
            self.servidor.connect(('192.168.0.22', '8080'))
        except:
            return False
        else:
            return True

    def atualizar_horario(self):

        data_e_hora_atuais = self.backend.buscar_horario_atual()
        print(data_e_hora_atuais)

if __name__ == "__main__":
    main = controller()
    main.atualizar_horario()
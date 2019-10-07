from servidor_model import backend
from socket import *
from time import sleep

class controller():
    def __init__(self):
        self.backend = backend()
        #self.endereco = '192.168.0.22'
        self.endereco = "localhost"
        self.porta = 50007

    def iniciar_servidor(self):
        self.servidor = socket(AF_INET, SOCK_STREAM)
        self.servidor.bind((self.endereco, self.porta))

        self.servidor.listen(5)

        self.espera_requisicao()

    def espera_requisicao(self):
        while True:
            self.id_conexao, conexao = self.servidor.accept()

            print(f"Nova Conexão de {conexao}")

            while True:
                requisicao = self.id_conexao.recv(1024)
                if not requisicao: 
                    break

                self.id_conexao.send(self.trata_requisicao(requisicao))
            try:
                self.id_conexao.close()
            except:
                pass
            else:
                print("Conexão fechada")
    def trata_requisicao(self, requisicao):
        requisicao = requisicao.decode("utf-8")

        return self.armador(f"{requisicao}")

    def armador(self, requisicao):
        if requisicao == '01':
            return self.data_e_hora_atuais()
        elif requisicao == '02':
            return self.verificar_spdata()
        elif requisicao == '03':
            #RETORNAR O IP DA MAQUINA DE ACORDO COM A ETIQUETA
            pass
        elif requisicao == '04':
            #RETORNAR A IMPRESSORA EM REDE DE ACORDO COM A ETIQUETA E IP DO SERVIDOR
            pass
        elif requisicao == "05":
            #RETORNAR A IMPRESSORA PADRÃO DE ACORDO COM A ETIQUETA DA MAQUINA

    def data_e_hora_atuais(self):
        hora = self.backend.busca_hora_atual()
        data = self.backend.busca_data_atual()

        data_e_hora = f"{data} | {hora}"

        return bytes(data_e_hora, 'utf-8')

    def verificar_spdata(self):
        return bytes(self.backend.status_spdata(), "utf-8")

if __name__ == "__main__":
    main = controller()
    try:
        main.iniciar_servidor()
    except:
        print("Reiniciando Servidor...")
        sleep(1)
        try:
            main.id_conexao.close()
        except:
            raise
        else:
            print("Conexão fechada")
        main.iniciar_servidor()

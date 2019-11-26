from servidor_model import backend
from socket import *
from time import sleep

class controller():
    def __init__(self):
        self.backend = backend()
        self.endereco = '192.168.0.69'
        #self.endereco = 'localhost'
        self.porta = 50007

    def iniciar_servidor(self):
        self.servidor = socket(AF_INET, SOCK_STREAM)
        self.servidor.bind((self.endereco, self.porta))

        self.servidor.listen(100)

        self.espera_requisicao()

    def reiniciar_servidor(self):
        try:
            self.servidor.close()
        except:
            pass

        self.iniciar_servidor()

    def fechar_conexao(self):
        try:
            self.conexao.close()
        except:
            pass
        else:
            print("Conexão fechada")
            self.espera_requisicao()

    def espera_requisicao(self):
        while True:
            self.conexao, id_conexao = self.servidor.accept()

            print(f"Nova Conexão de {id_conexao}")

            while True:
                requisicao = self.conexao.recv(1024)
                if not requisicao: 
                    break

                self.conexao.send(self.trata_requisicao(requisicao))
        self.fechar_conexao()

    def trata_requisicao(self, requisicao):
        requisicao = requisicao.decode('utf-8')
        try:
            requisicao = requisicao.split('-')
        except:
            raise


        return self.armador(requisicao)

    def armador(self, requisicao):
        if requisicao[0] == '01':
            return self.data_e_hora_atuais()
        elif requisicao[0] == '02':
            return self.verificar_spdata()
        elif requisicao[0] == '03':
            print(requisicao[1])
            return self.buscar_ip_maquina(requisicao[1])
        elif requisicao[0] == '04':
            #RETORNAR A IMPRESSORA EM REDE DE ACORDO COM A ETIQUETA E IP DO SERVIDOR
            pass
        elif requisicao[0] == '05':
            pass
            #RETORNAR A IMPRESSORA PADRÃO DE ACORDO COM A ETIQUETA DA MAQUINA

    def data_e_hora_atuais(self):
        hora = self.backend.busca_hora_atual()
        data = self.backend.busca_data_atual()

        data_e_hora = f"{data} | {hora}"

        return bytes(data_e_hora, 'utf-8')

    def verificar_spdata(self):
        return bytes(self.backend.status_spdata(), 'utf-8')

    def buscar_ip_maquina(self, etiqueta):
        return bytes(self.backend.retornar_ip_maquina(etiqueta), 'utf-8')

if __name__ == "__main__":
    main = controller()
    try:
        main.iniciar_servidor()
    except:
        print("Reiniciando Servidor...")
        sleep(1)
        try:
            main.reiniciar_servidor()
        except:
            raise
    else:
        print("Reiniciando Servidor...")
        sleep(1)
        try:
            main.reiniciar_servidor()
        except:
            raise

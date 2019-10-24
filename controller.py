from model import backend

class controller():

    def __init__(self):
        self.backend = backend()

    def inicio(self):
        pass

    def atualizar_horario(self):

        data_e_hora_atuais = self.backend.buscar_horario_atual()
        data_e_hora_atuais = data_e_hora_atuais.decode("utf-8")
        self.backend.atualizar_horario(data_e_hora_atuais)

    def verificar_spdata(self):
        status = self.backend.verificar_spdata()
        status = status.decode("utf-8")

        if "False" in status:
            return True
        else:
            print(f"Sistema SPDATA está em manutenção travamentos poderão acontecer - {status}")

if __name__ == "__main__":
    main = controller()
    main.verificar_spdata()
    main.atualizar_horario()
    #main.inicio()

    984052829 walter unimed - dois medicos unimed irao atuar aqui. 
    suspender a reserva do notebook de gracielle hoje e amanha
from model import backend

class controller():

    def __init__(self):
        self.backend = backend()

    def inicio(self):
        pass

    def atualizar_horario(self):
        try:
            data_e_hora_atuais = self.backend.buscar_horario_atual()
        except:
            print("Não foi possível acessar o servidor SESP")
            raise
        else:
            data_e_hora_atuais = data_e_hora_atuais.decode("utf-8")
            self.backend.atualizar_horario(data_e_hora_atuais)

    def verificar_spdata(self):
        try:
            status = self.backend.verificar_spdata()
        except:
            print("Não foi possível alcançar o servidor SESP")
            raise
        else:
            status = status.decode("utf-8")
            if "False" in status:
                return True
            else:
                print(f"Sistema SPDATA está em manutenção travamentos poderão acontecer - {status}")

if __name__ == "__main__":
    main = controller()
    try:
        main.atualizar_horario()
    except:
        pass
    else:
        main.verificar_spdata()
    #main.inicio()

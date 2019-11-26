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
            try:
                data_e_hora_atuais = data_e_hora_atuais.decode("utf-8")
            except:
                print("Não foi possível acessar o servidor SESP")
                
            else:
                self.backend.atualizar_horario(data_e_hora_atuais)

    def corrigir_internet(self):
        try:
            ip = self.backend.buscar_ip(self.backend.cabecalho_etiqueta)
        except:
            pass
        try:
            self.backend.atualizar_ip(ip)
        except:
            pass
        try:
            self.backend.definir_proxy()
        except:
            pass
        try:
            self.atualizar_horario()
        except:
            raise


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

    def spdata_nao_abre(self):
        try:
            self.atualizar_horario()
        except:
            #aqui se não conseguir buscar o horário, o problema provavelmente está na internet
            #portanto devemos chamar a função de correção de internet
            pass
        try:
            mapeamento_msg_confirmacao = self.backend.mapear_spdata()
        except:
            pass
        return mapeamento_msg_confirmacao

if __name__ == "__main__":
    main = controller()
    try:
        main.atualizar_horario()
    except:
        pass
    else:
        main.verificar_spdata()
    #main.inicio()

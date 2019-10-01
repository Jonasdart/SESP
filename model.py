import os

class backend():

    def __init__(self):
        pass

    def mapear_spdata(self):
        pass

    def mapear_impressora(self, impressora):
        pass

    def buscar_impressora_padrao(self, maquina):
        pass

    def definir_impressora_padrao(self, impressora):
        pass

    def criar_atalho_no_desktop(self):
        pass

    def buscar_horario_atual(self):
        pass

    def atualizar_horario(self):
        pass

    def reiniciar_maquina(self):
        retorno = True

        try:
            os.system("shutdown /r")
        except:
            retorno = False

        return retorno


    def buscar_ip(self, maquina):
        pass

    def atualizar_ip(self, ip)
        pass

"""teste = backend()
teste.reiniciar_maquina()"""
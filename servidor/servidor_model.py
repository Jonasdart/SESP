from datetime import datetime

class backend():
    def __init__(self):
        pass

    def busca_hora_atual(self):
        hora = datetime.now().strftime('%H:%M')

        return hora

    def busca_data_atual(self):
        data = datetime.now().strftime('%d-%m-%Y')

        return data
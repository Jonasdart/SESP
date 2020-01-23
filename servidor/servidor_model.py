from datetime import datetime
from banco_de_dados import glpi

class backend():
    def __init__(self):
        pass
        self.glpi = glpi()

    def busca_hora_atual(self):
        hora = datetime.now().strftime('%H:%M')

        return hora

    def busca_data_atual(self):
        data = datetime.now().strftime('%d-%m-%Y')

        return data

    def status_spdata(self):
        arquivo_status = open("status_spdata.txt", "r")
        status = arquivo_status.readlines()
        arquivo_status.close()
        horario_previsto = status[1].split("=")[1].strip()
        status = status[0]
        status = status.split("=")[1].strip()

             
        if "True" in status:     
            return horario_previsto
        else:
            return "False"

    def busca_info_maquina(self, etiqueta):
        try:
            info = self.glpi.buscar_info_maquina(etiqueta)
        except:
            return 'error'
        else:
            return info

    def retornar_ip_maquina(self, etiqueta):
        try:
            info = self.busca_info_maquina(etiqueta)
        except:
            pass

        try:
            info = info[0]
        except:
            return 'error'
        try:
            ip = info[5]
        except:
            return 'error'
        else:
            return ip

    def salvar_log(self, log):
        try:
            hora = self.busca_hora_atual()
            data = self.busca_data_atual()
            log = f'{hora} | {log}'
        except:
            raise
        
        try:
            try:
                arquivo_log = open(f'logs/{data}.txt', 'a')
            except:
                raise
            arquivo_log.write(f'{log}\n')
            arquivo_log.close()
        except:
            raise

        return True
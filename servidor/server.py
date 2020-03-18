import socketserver
import configparser
import model

class Backends():
    def __init__(self):
        backend = model.Backend()
        self.returned(backend)
    def returned(self, backend):
        return backend
 
def bind_server():
    config = configparser.ConfigParser()
    config.read('conf.cfg')

    port = int(config.get('config_server', 'porta'))
    ip = config.get('config_server', 'ip_server')

    server = {
        'ip_address' : ip,
        'server_port' : port
    }
    
    return server
 
class Controller(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server, backend):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def handle(self):
        while True:
            # Recebe data do cliente
            lenght_of_data_received = int.from_bytes(self.request.recv(2), byteorder='big')
            data_received = self.request.recv(lenght_of_data_received)
            if not data_received: break
 
            server_response = self.rigger(self.treat_request)
            length_of_response = len(server_response).to_bytes(2, byteorder='big')
            self.request.send(length_of_response)
            self.request.send(server_response.encode())
 
        self.request.close()

    def rigger(self, request):
        """
        O armador de requisições;
        Função que recebe e solicita 
        a devida info ao backend
        """

        if request[0] == 'update':
            return self.update.controller('update', item = requisicao[1])
        elif request[0] == 'len':
            return self.update.controller('len')
        elif request[0] == '000':
            return self.retornar_versao_vigente()
        elif request[0] == '00':
            return self.salvar_log(requisicao[1])
        elif request[0] == '01':
            return self.data_e_hora_atuais()
        elif request[0] == '02':
            return self.verificar_spdata()
        elif request[0] == '03':
            return self.buscar_ip_maquina(requisicao[1])
        elif request[0] == '04':
            #RETORNAR A IMPRESSORA EM REDE DE ACORDO COM A ETIQUETA E IP DO SERVIDOR
            pass
        elif request[0] == '05':
            pass
            #RETORNAR A IMPRESSORA PADRÃO DE ACORDO COM A ETIQUETA DA MAQUINA
            

    def treat_request(self, request):
        """
        Trata a requisição recebida do cliente.
        Modelo de requisição :
        | TIPO ; PARAMETRO1, PARAMETRO2, ... |
        sendo o ';' separador entre tipo e parametros
        sendo a ',' separador entre os parametros
        
        :return: request[0] = tipo, request[1] = parametros
        """
        
        request = request.decode()
        try:
            request = request.split(';')
        except:
            raise Exception('Requests prefix incorrect')

        try:
            request = [request[0], request[1].split(',')]
        except:
            Exception('The request contains only one parameter or has none')
        
        return request
    
    def paretto_x_date(self, date):
        df = self.backends.dFrame_total_refugos(date=date)
        response = self.backends.gera_paretto_total_refugo(df)

        return response

 
bind_server = bind_server()

ip = bind_server.get('ip_address')
port = bind_server.get('server_port')

backends = Backends()

server = socketserver.ThreadingTCPServer((ip, port, backends), backends, Controller)
server.serve_forever()
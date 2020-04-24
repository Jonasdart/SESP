import socketserver
import configparser
import model
import controller

def Backend():
    return model.Backend()
 
def bind_server():
    config = configparser.ConfigParser()
    config.read('sesp.cfg')

    port = int(config.get('config_server', 'porta'))
    ip = config.get('config_server', 'ip_server')

    server = {
        'ip_address' : ip,
        'server_port' : port
    }
    
    return server
 
class Controller(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.backends = Backend()
        self.controller = controller.Controller()
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

            server_response = self.rigger(self.treat_request(data_received))
            length_of_response = len(server_response).to_bytes(2, byteorder='big')

            self.request.send(length_of_response)
            self.request.send(server_response)
 
        self.request.close()

    def rigger(self, request):
        """
        O armador de requisições;
        Função que recebe e solicita 
        a devida info ao backend
        """

        if request[0] == 'version':
            """
            Retornar a versão vigente
            """
            return self.controller.control_update('version')
        elif request[0] == 'len':
            """
            Retorna o tamanho da atualização
            """
            return self.controller.control_update('len')
        elif request[0] == 'update':
            """
            Retorna os dados dos arquivos para serem salvos
            """
            return self.controller.control_update('update', item = request[1], connection=self.request)
        elif request[0] == '00':
            """
            Salva o log de ação do servidor
            """
            return self.controller.salvar_log(request[1])
        elif request[0] == '01':
            """
            Retorna a data e hora atual
            """
            return self.controller.data_e_hora_atuais()
        elif request[0] == '02':
            """
            Verifica se há backup ocorrendo no spdata
            """
            return self.controller.verificar_spdata()
        elif request[0] == '03':
            """
            Retorna o IP do computador
            """
            return self.controller.buscar_ip_maquina(request[1])
        elif request[0] == '04':
            #RETORNAR A IMPRESSORA EM REDE DE ACORDO COM A ETIQUETA E IP DO SERVIDOR
            pass
        elif request[0] == '05':
            pass
            #RETORNAR A IMPRESSORA PADRÃO DE ACORDO COM A ETIQUETA DA MAQUINA
        else:
            raise Exception('requisition parameters are incorrect')
            

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
 
bind_server = bind_server()

ip = bind_server.get('ip_address')
port = bind_server.get('server_port')

server = socketserver.ThreadingTCPServer((ip, port), Controller)
server.serve_forever()
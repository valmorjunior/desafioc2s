import socket
import json
from django.core.serializers import serialize
from django.db.models import Q
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_automoveis.settings')
django.setup()

from automoveis.models import Automovel

class MCPServer:
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Servidor MCP rodando em {self.host}:{self.port}")

    def processar_filtros(self, filtros):
        try:
            filtros = json.loads(filtros)
            query = Q()
            
            if 'marca' in filtros:
                query &= Q(marca=filtros['marca'])
            if 'modelo' in filtros:
                query &= Q(modelo__icontains=filtros['modelo'])
            if 'ano_min' in filtros:
                query &= Q(ano_fabricacao__gte=filtros['ano_min'])
            if 'ano_max' in filtros:
                query &= Q(ano_fabricacao__lte=filtros['ano_max'])
            if 'combustivel' in filtros:
                query &= Q(combustivel=filtros['combustivel'])
            if 'preco_min' in filtros:
                query &= Q(preco__gte=filtros['preco_min'])
            if 'preco_max' in filtros:
                query &= Q(preco__lte=filtros['preco_max'])
            if 'disponivel' in filtros:
                query &= Q(disponivel=filtros['disponivel'])
            
            automoveis = Automovel.objects.filter(query)
            # Ensure proper JSON serialization with ensure_ascii=False to handle special characters
            serialized_data = serialize('json', automoveis)
            # Parse the serialized data to ensure it's valid JSON
            parsed_data = json.loads(serialized_data)
            # Re-serialize with proper options
            return json.dumps(parsed_data, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao processar filtros: {e}")
            return json.dumps({'error': str(e)})

    def iniciar(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexão estabelecida com {addr}")
            
            try:
                # Increase buffer size to handle larger data
                data = client_socket.recv(8192).decode('utf-8')
                if not data:
                    continue
                    
                print(f"Recebido: {data}")
                resposta = self.processar_filtros(data)
                # Send in chunks to handle larger responses
                client_socket.sendall(resposta.encode('utf-8'))
            except Exception as e:
                print(f"Erro na comunicação: {e}")
                try:
                    error_msg = json.dumps({'error': str(e)})
                    client_socket.sendall(error_msg.encode('utf-8'))
                except:
                    pass
            finally:
                client_socket.close()

if __name__ == '__main__':
    servidor = MCPServer()
    servidor.iniciar()

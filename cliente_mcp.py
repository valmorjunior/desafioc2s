import socket
import json

class MCPClient:
    def __init__(self, host='mcp_server', port=9999):
        self.host = host
        self.port = port

    def enviar_consulta(self, filtros):
        client_socket = None
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))
            
            # Ensure proper JSON encoding with ensure_ascii=False
            filtros_json = json.dumps(filtros, ensure_ascii=False)
            client_socket.sendall(filtros_json.encode('utf-8'))
            
            # Receive data in chunks to handle larger responses
            chunks = []
            while True:
                chunk = client_socket.recv(8192)
                if not chunk:
                    break
                chunks.append(chunk)
            
            resposta = b''.join(chunks).decode('utf-8')
            
            try:
                return json.loads(resposta)
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar JSON: {e}")
                print(f"Resposta recebida: {resposta[:100]}...")
                return {'error': f"Erro na consulta MCP: {e}"}
        except Exception as e:
            return {'error': f"Erro na consulta MCP: {e}"}
        finally:
            if client_socket:
                client_socket.close()

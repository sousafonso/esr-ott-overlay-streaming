import socket

class Client:

    def __init__(self, server_ip="127.0.0.1", server_port=8000, bufsize=1024):
        self.server_ip = server_ip
        self.server_port = server_port
        self.bufsize = bufsize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.id = None

    def connect(self):
        self.sock.connect((self.server_ip, self.server_port))
        # after connecting, expect server to send assigned id as 'ID:<number>'
        try:
            data = self.sock.recv(self.bufsize)
            if data:
                text = data.decode("utf-8")
                if text.startswith("ID:"):
                    try:
                        self.id = int(text.split(":", 1)[1])
                    except Exception:
                        self.id = None
        except Exception:
            # ignore if no id received; keep id as None
            pass

        print(f"Conectado ao servidor {self.server_ip}:{self.server_port} (cliente id={self.id})")

    def interact(self):
        try:
            while True:
                mensagem = input("Mensagem para o servidor: ")
                self.sock.send(mensagem.encode("utf-8")[:self.bufsize])
                resposta = self.sock.recv(self.bufsize).decode("utf-8")
                print(f"Resposta do servidor: {resposta}")
                if resposta.lower() == "closed":
                    break
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            self.close()

    def close(self):
        self.sock.close()
        print("Cliente encerrou conexão.")

if __name__ == "__main__":
    # exemplo simples: criar um cliente e conectar; o id será atribuído automaticamente
    client = Client()
    client.connect()
    client.interact()

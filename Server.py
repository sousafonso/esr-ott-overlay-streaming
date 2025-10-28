import socket
import threading

class Server:
    def __init__(self, ip="127.0.0.1", port=8000, bufsize=1024):
        self.ip = ip
        self.port = port
        self.bufsize = bufsize
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # keep track of active client threads/sockets if needed
        self.clients = {}
        self._lock = threading.Lock()
        # next client id to assign (incremental per connection)
        self._next_client_id = 1

    def start(self):
        """Start the server and accept incoming connections.

        For each accepted connection a new thread is spawned to handle it.
        """
        self.sock.bind((self.ip, self.port))
        # allow a small backlog of pending connections
        self.sock.listen(5)
        print(f"Servidor escutando em {self.ip}:{self.port}")

        try:
            while True:
                client_sock, addr = self.sock.accept()
                # assign a client id and inform the client immediately
                with self._lock:
                    client_id = self._next_client_id
                    self._next_client_id += 1
                try:
                    # send the assigned id to the client using a simple protocol: 'ID:<number>'
                    client_sock.send(f"ID:{client_id}".encode("utf-8"))
                except Exception as e:
                    print(f"Falha ao enviar id para {addr}: {e}")
                    client_sock.close()
                    continue

                print(f"Conexão aceite de {addr[0]}:{addr[1]} (id={client_id})")
                thread = threading.Thread(target=self._handle_client, args=(client_sock, addr, client_id), daemon=True)
                with self._lock:
                    self.clients[addr] = (client_sock, thread)
                thread.start()
        except KeyboardInterrupt:
            print("Interrompido pelo utilizador, encerrando servidor...")
        finally:
            self.close()

    def _handle_client(self, client_sock, addr, client_id=None):
        """Handle a single client connection in its own thread."""
        try:
            while True:
                data = client_sock.recv(self.bufsize)
                if not data:
                    print(f"Cliente {addr[0]}:{addr[1]} (id={client_id}) desconectou")
                    break
                mensagem = data.decode("utf-8")
                print(f"Recebido de {addr[0]}:{addr[1]} (id={client_id}): {mensagem}")
                if mensagem.lower() == "close":
                    client_sock.send("closed".encode("utf-8"))
                    break
                client_sock.send("accepted".encode("utf-8"))
        except Exception as e:
            print(f"Erro na conexão {addr}: {e}")
        finally:
            try:
                client_sock.close()
            except Exception:
                pass
            with self._lock:
                if addr in self.clients:
                    del self.clients[addr]
            print(f"Conexão com {addr[0]}:{addr[1]} (id={client_id}) encerrada.")

    def close(self):
        # close all client sockets
        with self._lock:
            for addr, (client_sock, thread) in list(self.clients.items()):
                try:
                    client_sock.close()
                except Exception:
                    pass
            self.clients.clear()

        try:
            self.sock.close()
        except Exception:
            pass
        print("Servidor encerrado.")


if __name__ == "__main__":
    server = Server()
    server.start()

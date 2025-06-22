import socket
import threading
import time

class ClientManager:

    def __init__(self, host='127.0.0.1', port=8080):
        """
        Inicializa o gerenciador de clientes
        :param host: Endereço do servidor
        :param port: Porta padrão 8080
        """
        self.host = host
        self.port = port
        self.threads = []

    def worker(self, thread_id, message):
        """
        Método de trabalho utilizado por cada thread
        Cria um socket, conecta, envia a mensagem e fecha.
        :param message: Texto que será enviado
        :param thread_id:
        :return:
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                print(f"Thread {thread_id}: Conectando ao servidor {self.host}:{self.port}...")
                sock.connect((self.host, self.port))
                print(f"Thread {thread_id}: Conectado. Enviando mensagem...")
                sock.sendall(message.encode('utf-8'))
                print(f"Thread {thread_id}: Mensagem enviada com sucesso.")
                # Pequena pausa para analisar o comportamento
                time.sleep(1)
        except ConnectionRefusedError:
            print(f"Thread {thread_id}: A conexão foi recusada. O servidor está ativo?")
        except Exception as e:
            print(f"Thread {thread_id}: Ocorreu um erro: {e}")
        finally:
            print(f"Thread {thread_id}: Finalizando...")

    def start(self, num_threads=5, message=''):
        messages = message.split('|')
        for i in range(num_threads):
            thread = threading.Thread(target=self.worker, args=(i + 1,messages[i]))
            self.threads.append(thread)
            thread.start()
            print(f"Iniciando a Thread {i+1}")

        # Aguarda o trabalho de cada thread para finalizá-la
        for thread in self.threads:
            thread.join()

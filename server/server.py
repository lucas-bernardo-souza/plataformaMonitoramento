import socket
import threading

class Server:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Fila para armazenar mensagens e o Lock para garantir thread-safety
        self.message_queue = []
        self.queue_lock = threading.Lock()

        self.log_file_name = 'log_backup.log'
        # Garante que a escrita no arquivo seja thread-safe
        self.file_write_lock = threading.Lock()

        print(f"Servidor de Lotes será iniciado em {self.host}:{self.port}")

    def handle_client(self, conn,address):
        """
        Lida com a conexão de um único cliente. Recebe a mensagem e a adiciona de forma segura à fila de processamento.

        :param conn:
        :param address:
        :return:
        """
        print(f"[NOVA CONEXÃO] Cliente {address} conectado.")
        batch_to_process = None
        try:
            with conn:
                data = conn.recv(1024)
                if not data:
                    return

                message = data.decode('utf-8')
                print(f"    [DADOS RECEBIDOS] de {address}: '{message}'")
                # Início da seção crítica, trataremos uma thread por vez
                with self.queue_lock:
                    self.message_queue.append(message)
                    print(f"[FILA] Mensagem adicionada. Tamanho atual da fila: {len(self.message_queue)}")

                    # Verificando se o lote está completo
                    if len(self.message_queue) == 5:
                        print("[LOTE COMPLETO] Atingiu 5 mensagens. Copiando para processamento...")
                        batch_to_process = self.message_queue.copy()
                        self.message_queue.clear()
            if batch_to_process:
                self.process_batch(batch_to_process)
        except Exception as e:
            print(f"[ERRO] Ocorreu um erro com o cliente {address}: {e}")
        finally:
            print(f"[FIM DA CONEXÃO] A thread para o cliente {address} está finalizada.")

    def process_batch(self, batch):
        """
        Processa um lote de 5 mensagens.
        Neste caso, junta em uma string
        :param batch:
        :return:
        """
        print("\n--- PROCESSANDO LOTE DE MENSAGENS ---")
        try:
            final_string = " | ".join(batch)
            print("Mensagem consolidade do lote:")
            print(f">>>{final_string}")
            self.write_to_log(final_string)
        except Exception as e:
            print(f"[ERRO NO PROCESSAMENTO] Não foi possível processar o lote: {e}")
        print("--- FIM DO PROCESSAMENTO DO LOTE ---\n")

    def write_to_log(self, message_line):
        with self.file_write_lock:
            try:
                with open(self.log_file_name, 'a', encoding='utf-8') as f:
                    f.write(message_line + '\n')
            except Exception as e:
                print(f"[ERRO DE ESCRITA NO LOG] Não foi possível escrever no arquivo: {e}")


    def start(self):
        """
        Inicia o loop principal do servidor para aceitar conexões continuamente.
        """

        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            print("Servidor está escutando continuamente... Precione CTRL+C para parar.")

            while True:
                conn, address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, address))
                client_thread.start()
        except KeyboardInterrupt:
            print("\n[DESLIGANDO] Recebido comando para desligar o servidor (CTRL+C).")
            if self.message_queue:
                print(f"[AVISO] Processando lote final incompleto com {len(self.message_queue)} mensagens.")
                self.process_batch(self.message_queue)
        finally:
            print("[ENCERRANDO] Fechando o socket do servidor.")
            self.server_socket.close()

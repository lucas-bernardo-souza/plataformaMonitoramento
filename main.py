from ssh_connector import SSHConnector
from client_manager import ClientManager
from server.server import Server
import threading

def main():
    HOST = "137.131.153.86"
    USER = "a201250942"
    PASS = "kI92w9sU"
    ARQUIVO_DE_LOG_REMOTO = "Monitoramento/simula-log.log"

    # --- Instanciação dos objetos ---
    server = Server(host='127.0.0.1', port=8080)
    gerenciador_de_clientes = ClientManager(host='127.0.0.1', port=8080)

    # Criando uma thread para o servidor
    server_thread = threading.Thread(target=server.start)

    # Iniciando a thread do servidor
    # Servidor começará a escutar em segundo plano
    server_thread.start()
    try:
        with SSHConnector(host=HOST, username=USER, password=PASS) as ssh:
            print(f"--- Monitorando o arquivo '{ARQUIVO_DE_LOG_REMOTO}' em tempo real")
            print("--- Pressione CTRL+C para parar ---")

            for nova_linha in ssh.monitor_log_file(ARQUIVO_DE_LOG_REMOTO):
                #print(f"[NOVO LOG]: {nova_linha}")
                gerenciador_de_clientes.start(num_threads=5, message=nova_linha)

                if "ERROR" in nova_linha.upper():
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(f"ALERTA DE ERRO DETECTADO: {nova_linha}")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                elif "CONNECT" in nova_linha.upper():
                    print("--- Conexão detectada no log ---")
    except ConnectionError as e:
        print(f"ERRO DE CONEXÃO: Não foi possível conectar ao servidor. Detalhes: {e}")
    except Exception as e:
        # Pega qualquer outra exceção que a classe SSHConnector possa levantar (ex: autenticação)
        print(f"ERRO INESPERADO: Ocorreu um problema durante a operação. Detalhes: {e}")

if __name__ == "__main__":
    main()
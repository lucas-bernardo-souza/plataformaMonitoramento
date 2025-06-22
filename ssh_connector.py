import paramiko
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class SSHConnector:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client = None

        if not self.password:
            raise ValueError("Você deve fornecer uma senha")
        if not self.host:
            raise ValueError("Você deve forncener o endereço (ip - externo) do host")

    def connect(self):
        if self.client and self.client.get_transport().is_active():
            logging.info("Já existe uma conexão ativa.")
            logging.info("Conectado a: " + self.host)
            return

        try:
            logging.info(f"Conectado ao servidor {self.host}...")
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.client.connect(hostname=self.host, username=self.username, password=self.password, timeout=10)
            logging.info("Conectado a: " + self.host)
        except paramiko.AuthenticationException:
            logging.error("Fala na autenticação. Verifique suas credenciais")
            raise
        except Exception as e:
            logging.error(f"Ocorreu um erro ao conectar: {e}")
            self.client = None
            raise

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
            logging.info("Conexão SSH fechada")

    def execute_comando(self, command):
        """
        :param command:
        :return: Uma tupla (stdout, stderr) contendo a saída e os erros do comando.
        """
        if not self.client:
            logging.error("Não é possível executar o comando. Cliente não está conectado")
            raise ConnectionError("A conexão SSH não está ativa.")

        logging.info(f"Executando comando: '{command}'")
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()

    def monitor_log_file(self, remote_filepath):
        if not self.client or not self.client.get_transport().is_active():
            raise ConnectionError("A conexão SSH não está ativa.")

        command = f"tail -f -n 0 {remote_filepath}"
        logging.info(f"Iniciando monitoramento de '{remote_filepath}'... Pressione Ctrl+C para parar.")
        stdin, stdout, stderr = self.client.exec_command(command, bufsize=1, get_pty=True)

        try:
            for line in iter(stdout.readline, ""):
                yield line.strip()
        except KeyboardInterrupt:
            logging.info("Monitoramento interrompido pelo usuário.")
        finally:
            logging.info("Fechando o canal de monitoramento.")
            stdout.channel.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
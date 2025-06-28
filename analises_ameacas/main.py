import os
import time
from log_analyzer import LogAnalyzer

class LogMonitor:
    """
    Monitora um arquivo de log, lendo novas linhas continuamente
    """
    def __init__(self, log_filepath, analyzer):
        self.log_filepath = log_filepath
        self.analyzer = analyzer
        self.last_position = 0

        # Garante que o arquivo existe, caso contrário, cria-o.
        if not os.path.exists(self.log_filepath):
            with open(self.log_filepath, "w") as file:
                pass

    def _get_current_file_size(self):
        """
        :return: tamanho do arquivo
        """
        try:
            return os.path.getsize(self.log_filepath)
        except FileNotFoundError:
            return 0

    def tail(self):
        """
        Lê novas linhas do arquivo de log, começando da última posição lida
        :return:
        """
        current_size = self._get_current_file_size()

        if current_size < self.last_position:
            self.last_position = 0

        with open(self.log_filepath, 'r') as f:
            f.seek(self.last_position)
            while True:
                line = f.readline()
                if not line:
                    break
                self.analyzer.analyze_line(line.strip())
                self.last_position = f.tell()

if __name__ == "__main__":
    LOG_FILE = "log_backup.log"

    LOG_FILE_PATCH = os.path.join(os.path.dirname(__file__), "..", LOG_FILE)

    analyzer = LogAnalyzer()
    monitor = LogMonitor(LOG_FILE_PATCH, analyzer)

    print(f"Monitorando o arquivo de log: {LOG_FILE}")
    print(f"Presione Ctrl+C para sair.")
    try:
        while True:
            monitor.tail()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado...")
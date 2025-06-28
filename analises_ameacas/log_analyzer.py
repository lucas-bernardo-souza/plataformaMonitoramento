import re

class LogAnalyzer:
    """
    Analisa as linhas do log, buscando padrões específicos
    """
    def analyze_line(self, line):
        """
        :param line: recebe uma linha de log
        :return: estrai o código do usuário e verifica padrões
        """
        parts = line.split(' | ')
        if len(parts) >= 2:
            user_info = parts[1].strip() # "user - codigo"

            match = re.search(r'-\s*(\d+)', user_info)
            if match:
                user_code = match.group(1)
                self._check_repeated_numbers(user_info, user_code)

    def _check_repeated_numbers(self, user_info, user_code):
        """
        Verifica se há de 2 a 4 números repetidos em sequência no código do usuário
        :param user_info:
        :param user_code:
        :return:
        """

        # Expressão regular para encontrar 2, 3 ou 4 dígitos iguais em sequencia
        pattern = r'(\d)\1{1,3}'

        if re.search(pattern, user_code):
            print(f"{user_info} - Possível Ameaça!")
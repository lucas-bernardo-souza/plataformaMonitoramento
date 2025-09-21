# Sistema de Monitoramento e Análise de Logs em Tempo Real

Este projeto implementa um sistema em Python para monitorar arquivos de log de um servidor remoto, agregar esses logs localmente e analisá-los em tempo real em busca de padrões que possam indicar ameaças à segurança.

## Visão Geral da Arquitetura

O sistema é dividido em três componentes principais que operam de forma interligada: o **Coletor**, o **Agregador** e o **Analisador**.

1.  **Coletor (`main.py`, `ssh_connector.py`)**
    * Conecta-se a um servidor remoto via SSH usando a biblioteca `paramiko`.
    * Monitora um arquivo de log específico (`tail -f`) para capturar novas linhas em tempo real.

2.  **Agregador e Distribuidor (`server.py`, `client_manager.py`)**
    * Para cada linha de log capturada, um `ClientManager` simula um ambiente distribuído, criando 5 clientes concorrentes.
    * Cada cliente envia um fragmento da linha de log para um servidor TCP local.
    * O `Server` (agregador) é multi-thread e escuta esses fragmentos. Ele os agrupa em lotes de 5, reconstrói a linha de log original e a salva em um arquivo local chamado `log_backup.log`.

3.  **Analisador (`mainAnalisesAmeacas.py`, `log_analyzer.py`)**
    * Um script independente monitora o arquivo `log_backup.log`.
    * Quando novas linhas são adicionadas, o `LogAnalyzer` as inspeciona usando expressões regulares para identificar padrões suspeitos (por exemplo, sequências de dígitos repetidos em um código de usuário).
    * Alertas de "Possível Ameaça" são impressos no console quando um padrão é encontrado.

### Tecnologias Utilizadas

* **Python 3**
* **paramiko:** Para a conectividade SSH com o servidor remoto.
* **socket e threading:** Para a construção do servidor TCP concorrente e do gerenciador de clientes.
* **re (Regex):** Para a análise e detecção de padrões nos logs.

---

## Como Executar o Projeto

Para executar este sistema, você precisará de Python 3, acesso a um servidor remoto via SSH e dois terminais para rodar o Coletor/Agregador e o Analisador simultaneamente.

### 1. Pré-requisitos

* Python 3 e pip instalados.
* Um servidor remoto com um arquivo de log que possa ser acessado via SSH.

### 2. Instalação das Dependências

Clone o repositório e instale a única dependência externa, a biblioteca `paramiko`.

```bash
# Clone o repositório
git clone https://github.com/lucas-bernardo-souza/plataformaMonitoramento.git
cd plataformaMonitoramento

# Instale a dependência
pip install paramiko
```

### 3. Configuração

Abra o arquivo `main.py` e edite as seguintes variáveis com suas próprias credenciais e caminhos:

```python
# Endereço IP ou hostname do seu servidor remoto
HOST = "SEU_IP_AQUI"
# Seu nome de usuário SSH
USER = "SEU_USUARIO_AQUI"
# Sua senha SSH
PASS = "SUA_SENHA_AQUI"
# Caminho completo para o arquivo de log no servidor remoto
ARQUIVO_DE_LOG_REMOTO = "caminho/para/seu/arquivo.log"
```

### 4. Execução do Sistema

O sistema precisa de dois processos rodando em paralelo. Abra dois terminais na pasta do projeto.

**No Terminal 1 - Inicie o Analisador de Ameaças:**

Este script ficará monitorando o arquivo `log_backup.log` em busca de novas entradas para analisar.

```bash
python mainAnalisesAmeacas.py
```
Você verá a mensagem: `Monitorando o arquivo de log: log_backup.log`.

**No Terminal 2 - Inicie o Coletor e o Agregador:**

Este é o script principal que inicia o servidor local, conecta-se ao servidor remoto e começa o processo de coleta.

```bash
python main.py
```
Você verá as mensagens de conexão SSH e o sistema começará a processar as novas linhas do log remoto à medida que elas aparecerem.

Agora, o fluxo completo está ativo. Novas linhas no log remoto serão capturadas, processadas pelo servidor local, salvas em `log_backup.log` e, finalmente, analisadas pelo script no primeiro terminal.

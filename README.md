# plataformaMonitoramento
Trabalho desenvolvido na disciplina de Computação Distribuida e Paralela.

O arquivo main na pasta raiz inicializa o servidor local, se conecta no servidor remoto por meio da classe "ssh_conector"
e acessa o arquivo de log.
Uma vez que a conexão é estabelecida o main vai ler linha a linha do arquivo de log do servidor remoto, na sequência
chamara o método "start" da classe "ClientManager".
A classe "ClientManager" recebe linha a linha do arquivo de log e envia para o servidor local. Para isso ela utiliza
cinco threads. A mensagem é dividida em cinco pacotes e cada um deles é enviado de forma paralela por cada uma das cinco
threads.
O servidor por sua vez que está no diretório "server" é inicializado pelo main do programa, o usuário não precisa se 
preocupar em inicializa-lo. Ele vai ter cinco threads para receber os pacotes, juntar as mensagens e salvar no arquivo
"log_backup.log".
Por fim, temos outro programa chamado "analises_ameacas" que vai buscar possíveis ameaças por meio do arquivo de log.
Esse sistema pode ser inicializado em conjunto com a execução da plataforma de monitoramento ou não. Ele vai analisar o 
arquivo "log_backup.log" e buscar por padrões, caso encontrar algo suspeito vai printar na tela o usuário suspeito.

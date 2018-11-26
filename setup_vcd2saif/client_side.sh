#!/bin/bash
#
# Autor: Pedro Henrique Exenberger Becker (phebecker@inf.ufrgs.br)
# Modificado por: Marcelo Brandalero (mbrandalero@inf.ufrgs.br)
#
# Data: 20/11/2018
#
# Descrição:
# Script para executar simulador BOOM e transferir vcd para servidor remoto,
# onde será executada a ferramenta vcd2saif.

# Cria um named pipe local chamado "fifo"
mkfifo fifo

# Cria um named pipe remoto chamado "fifo"
# Substituir username por seu usuário do NSCAD
# Substituir ufrgs-server-10 por qualquer servidor do NSCAD
ssh seu_user@ufrgs-server-10.inf.ufrgs.br "mkfifo fifo"

# Configura ambiente Synopsis no servidor e executa vcd2saif
# Mantém a conexão ssh aberta e vai para o background do shell
ssh seu_user@ufrgs-server-10.inf.ufrgs.br ". ~/server_side.sh && vcd2saif -input fifo -output boom.saif" &

# Redireciona o conteúdo do named pipe para o servidor
# Mantém a conexão ssh aberta e vai para o background do shell
cat fifo | ssh seu_user@ufrgs-server-10.inf.ufrgs.br "cat > ~/fifo" &

# Executa simulador do BOOM, escrevendo o VCD no arquivo chamado fifo,
# com a aplicação "pk hello"
./simulator-boom --vcd=fifo -c pk ~/boom-template/progs/hello 

# Apaga o FIFO após o termino do processo
rm fifo

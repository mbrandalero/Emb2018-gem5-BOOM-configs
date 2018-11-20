Processo para gerar o arquivo SAIF, com a atividade de chaveamento de cada estrutura do pipeline, necessário para cálculo de potência.

# Motivação:
O processo de compilação do BOOM funciona da seguinte forma.
1) Uma especificação em linguagem de alto-nível (Chisel) é convertida para Verilog sintetizável.
2) O Verilog sintetizável é convertido (usando uma ferramenta chamada Verilator) em um simulador C++ capaz de gerar waveforms da atividade do processador (arquivo VCD) durante a execução de uma aplicação. O arquivo VCD pode ser utilizado para determinar a atividade de chaveamento.

## Problema:
O arquivo VCD fica grande muito facilmente (++GBs), e contém informações desnecessárias para a análise de potência (chaveamento de todos os sinais a cada ciclo, quando o necessário é apenas a média do chaveamento para cada sinal).

## Solução:
Converter o VCD em um arquivo SAIF, que contém apenas os valores médios de chaveamento para cada sinal. Isto pode ser feito utilizando a ferramenta vcd2saif, disponível no servidor do NSCAD.

## Problema:
Transmitir o arquivo VCD (++GBs) para o servidor NSCAD, que tem espaço de armazenamento limitado.

## Solução:
Efetuar à conversão à medida que o arquivo vai sendo gerado - i.e., usar um sistema produtor-consumidor que evite a necessidade de armazenar ++GBs de dados antes de efetuar a conversão - através de um name pipes.


# Procedimento
vão haver dois processo sendo executados, um no lado cliente (máquina pessoal) e outro no lado do servidor (NSCAD).

## No lado do cliente:
- Criar um named pipe onde o simulador do BOOM escreve o VCD à medida que executa
- Transferir conteúdo do named pipe local para named pipe no servidor

## No lado do servidor:
- Criar um named pipe para receber o conteúdo do VCD sendo transmitido
- Usar o programa vcd2saif no conteúdo do named pipe.

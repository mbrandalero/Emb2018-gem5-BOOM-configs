
# Instruções

Clonar o repositório. 

## gem5

Utilizar o arquivo **simulate.py** como script de configuração para o gem5. 

Exemplo, executando um *Hello World* com a CPU 4-Wide: `gem5 simulate.py --cpu="OoO-4W" run-benchmark -c="hello"`.

Opções de CPU: *OoO-1W*, *OoO-2W*, *OoO-4W*.

## BOOM

Adicionar as linhas dos arquivos **Configs.scala** e **configs.scala** aos arquivos de configuração correspondentes em **boom/src/main/scala/system/Configs.scala** e **boom/src/main/scala/common/configs.scala**.

Compilar o simulador do BOOM usando

`make CONFIG=Emb20184WBoom` (para 4-Wide)
ou
`make CONFIG=Emb20182WBoom` (para 2-Wide)
ou
`make CONFIG=Emb20181WBoom` (para 1-Wide)

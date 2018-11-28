## Template para síntese lógica no Cadence GENUS
## Autor: Marcelo Brandalero
##
## Data: 14.08.2018

# Seu design aqui - arquivos que serão lidos
set DESIGNS "~/Designs/freechips/Boom/boom.system.DefaultConfig.v"
# Seu modulo topo aqui - no caso do BOOM, vai ser o BoomCore
set MODULE_NAME "BoomCore"
# Isso aqui é pra fazer análise de potencia - o saif é o arquivo que contem a atividade média de chaveamento de cada sinal, carregado antes da síntese pra estimar o chaveamento e potencia das coisas.
set SAIF_PATH "/workareas/meu.user/boom.saif"

# auto-explicativo
# o map-effort tem que ser no maximo medium se não quiser que ele desagrupe os modulos.
# se colocar em high sai um design otimizado, mas não vai ser possível fazer o breakdown da potencia/area das coisas
set CLOCK_DELAY 500
set DESIGN_NAME design_2000MHz
set SYN_EFF medium
set MAP_EFF medium

# caminho da lib
set_attribute lib_search_path ./
# nome do arquivo da lib (dentro do caminho)
set_attribute library cell_lib.lib

# serviria pra usar o mesmo modelo de fio (capacitancias) pra todo o circuito, mas a biblioteca que usamos não tem isso
# se a biblioteca que tu usar tiver, tem que setar o atributo wireload_MODEL (nota que é outro) pro nome do modelo
set_attribute wireload_mode top
# lp são os atributos relacionados à analise de potencia
# default_probability é a probabilidade de uma rede estar em nível lógico 1
# tem que setar também o lp_default_toggle_rate, que é dado em chaveamentos/ns (ou ps, dependendo da lib) - aqui eu não setei pq a análise era feita em cima do VCD
set_attribute lp_default_probability 0.5
# auto explicativo
set_attribute lp_power_analysis_effort high

# aqui o toggle rate que falei acima
# a conta se refere a "metade do chavemento maximo" - nota que ele chaveia 0.5 vezes a cada ciclo de clock
set_attribute lp_default_toggle_rate [expr 0.5 * double(1000) / ${CLOCK_DELAY}]

# auto explicativo
read_hdl ${DESIGNS}
puts "Runtime & Memory after 'read_hdl'"
timestat

# transforma os hdl em uma representação na memoria
elaborate ${MODULE_NAME}
puts "Runtime & Memory after 'elaborate'"
timestat

# le o saif para análise de potência
read_saif -instance ${MODULE_NAME} ${SAIF_PATH}

# pra otimizar pra potencia dinamica, seta max potencia dinamica = 0
set_attribute max_dynamic_power 0 [find / -des *]

# isso aqui é pra ele tratar as redes de clock como ideais, sem delay
# a geração da árvore de clock, que minimiza os delays dessa rede, é feita apenas durante o place & route, que é posterior à sintese logica que é feita aqui
create_clock -period ${CLOCK_DELAY} clock
set_ideal_network clock
set_dont_touch_network clock

# síntese "to generic" - quer dizer, gera netlist independente da tecnologia
synthesize -to_generic -eff ${SYN_EFF} ${MODULE_NAME}
puts "Runtime & Memory after 'synthesize -to_generic'"
timestat

# mapeia o netlist gerado para a biblioteca de células
synthesize -to_mapped  -eff ${MAP_EFF} ${MODULE_NAME}
puts "Runtime & Memory after 'synthesize -to_mapped'"
timestat

# auto explicativo - dá pra passar as opções "-detail" aqui
report timing  > reports/timing/timing_${DESIGN_NAME}_default.txt
report area    > reports/area/area_${DESIGN_NAME}_default.txt
report power   > reports/power/power_${DESIGN_NAME}_default.txt

# auto explicativo - o -tcf gera um arquivo com atividade de chaveamento, se tu for usar um vcd ou coisa parecida
write_design -basename designs/${DESIGN_NAME} -hierarchical -tcf

#quit

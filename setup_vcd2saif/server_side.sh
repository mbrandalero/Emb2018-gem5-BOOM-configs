#!/bin/bash
#
# Autor: Yuri Silva Paludo E-mail: suporte@nscad.org.br
# Modificado por: Pedro Henrique Exenberger Becker (phebecker@inf.ufrgs.br)
#                 em 20/11/2019.
#     Removida a necessidade de input do usuário.
#
# Data de criacao: 25/01/2013
#
# Descricao:
# Configurar licencas para ferramentas Synopsys. Configurar variaveis de ambiente das ferramentas.
#
# Atualizacao: 12/04/2016
# Realizada por: Alonso Schmidt
# Descricao: Atualizado IC Compiler
#
# Atualizacao: 26/04/2017
# Realizada por: Alonso Schmidt
# Descricao: Atualizado HSPICE
#


###
### Funcoes
###

function configuraSentaurus ()
{
# Sentaurus 2016
export PATH="$PATH:$SYNOPSYS_TOOLS/$SO/sentaurus_vL_2016.03/bin"
}

# function configuraDesignCompiler ()
# {
# echo "Qual versão do Design Compiler deseja configurar?"
# echo
# echo -e "\t[1] Design Compiler vL 2016.03"
# echo -e "\t[2] Design Compiler vG 2012.06"
# echo -n "Opção: "
# read DCOMPILER_VERSION

# case $DCOMPILER_VERSION in
# 1)
# # Design Compiler 2016
# 
export PATH="$PATH:$SYNOPSYS_TOOLS/$SO/design_compiler_L-2016.03/bin"
# ;;
# 2)
# # Design Compiler 2012
# 
export PATH="$PATH:$SYNOPSYS_TOOLS/$SO/syn_vG-2012.06/bin"
# ;;
# *)
# echo "Opção Invalida."
# ;;
# esac
# }

###
### Inicio do script
###
echo -e '\E[34;1;1m'"
################################################################
# #
# UFRGS - Universidade Federal do Rio Grande do Sul #
# NSCAD - Nucleo de Suporte a CAD #
# #
# SYNOPSYS ENVIRONMENT SETUP #
# #
################################################################
"
echo -e '\E[0m'""

SERVER_NAME="ufrgs-server-01.inf.ufrgs.br"
SERVER_PORT="27010"

SYNOPSYS_TOOLS="/tools/synopsys"
SO="rhel5"

export SYNOPSYS="$SYNOPSYS_TOOLS/$SO"

export SNPSLMD_LICENSE_FILE="$SERVER_PORT@$SERVER_NAME"
export LM_LICENSE_FILE="$SNPSLMD_LICENSE_FILE:$LM_LICENSE_FILE"


# Customer Designer
export PATH="$PATH:$SYNOPSYS/customdesigner_vG-2012.09/bin"

# Cosmos Scope
export PATH="$SYNOPSYS/cosmosscope_L-2016.03/ai_bin:$PATH"

# Design Compiler
#export PATH="$PATH:$SYNOPSYS/design_compiler_L-2016.03/bin"
export SYNOPSYS_SYN_ROOT="$SYNOPSYS/syn_vL-2016.03"
export PATH="$PATH:$SYNOPSYS/syn_vL-2016.03/bin"
# configuraDesignCompiler

# IC Compiler
export PATH="$PATH:$SYNOPSYS/icc_vJ-2014.09/bin"
#export PATH="$PATH:$SYNOPSYS/icc_vK-2015.06/bin"
#export PATH="$PATH:$SYNOPSYS/icc_vG-2012.06/bin"

# IC Validator
export PATH="$PATH:$SYNOPSYS/icvalidator_vI-2013.12/bin/AMD.64"

# Hercules
export PATH="$PATH:$SYNOPSYS/hercules_vB-2008.09/bin/amd64"

# HSPICE
export PATH="$PATH:$SYNOPSYS/hspice_L-2016.06/hspice/bin"
#source $SYNOPSYS/hspice_L-2016.06/hspice/bin/kshrc.meta

# Library Compiler
export SYNOPSYS_LC_ROOT="$SYNOPSYS/lc_vL-2016.06"
export PATH="$PATH:$SYNOPSYS/lc_vL-2016.06/bin"

# Milkyway
export PATH="$PATH:$SYNOPSYS/milkyway_vJ-2014.09/bin/AMD.64"

# Prime Time
export PATH="$PATH:$SYNOPSYS/pts_vH-2012.12/amd64/syn/bin"

# Sentaurus
configuraSentaurus

# StarRC
export PATH="$PATH:$SYNOPSYS/starrc_vH-2013.06/amd64_starrc/bin"

# Synphony C Compiler
export PATH="$PATH:$SYNOPSYS/scc_vI-2013.12/amd64/bin"
export PATH="$PATH:$SYNOPSYS/scc_vI-2013.12/bin"

# VCS
export VCS_HOME="$SYNOPSYS/vcs_vK-2015.09-SP1-1"
export PATH="$PATH:$VCS_HOME/bin"

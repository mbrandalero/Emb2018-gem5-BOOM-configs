# -*- coding: utf-8 -*-

import m5
from m5.objects import *

from m5.objects import BaseCache
from m5.objects import DDR3_1600_8x8
from m5.objects import DerivO3CPU
from m5.objects import System
from m5.objects import SystemXBar

###############################################################################

## Unidades funcionais
##
## Cada classe especifica um tipo de unidade funcional.
##
## O campo opList especifica os tipos de operação que a FU executa e o campo
## count especifica a quantidade de unidades desse tipo.

###############################################################################

class MyIntALU(FUDesc):
    opList = [ OpDesc(opClass='IntAlu') ]
    count = 2

class MyIntMultDiv(FUDesc):
    opList = [ OpDesc(opClass='IntMult', opLat=3, pipelined=True),
               OpDesc(opClass='IntDiv', opLat=16, pipelined=False) ]

    # DIV and IDIV instructions in x86 are implemented using a loop which
    # issues division microops.  The latency of these microops should really be
    # one (or a small number) cycle each since each of these computes one bit
    # of the quotient.
    if buildEnv['TARGET_ISA'] in ('x86'):
        opList[1].opLat=1

    count = 1

class My_FP_ALU(FUDesc):
    opList = [ OpDesc(opClass='FloatAdd', opLat=2),
               OpDesc(opClass='FloatCmp', opLat=2),
               OpDesc(opClass='FloatCvt', opLat=2) ]
    count = 1

class My_FP_MultDiv(FUDesc):
    opList = [ OpDesc(opClass='FloatMult', opLat=4),
               OpDesc(opClass='FloatDiv',  opLat=12, pipelined=False),
               OpDesc(opClass='FloatSqrt', opLat=24, pipelined=False) ]
    count = 1

class My_SIMD_Unit(FUDesc):
    opList = [ OpDesc(opClass='SimdAdd',          opLat=2),
               OpDesc(opClass='SimdAddAcc',       opLat=2),
               OpDesc(opClass='SimdAlu',          opLat=2),
               OpDesc(opClass='SimdCmp',          opLat=2),
               OpDesc(opClass='SimdCvt',          opLat=2),
               OpDesc(opClass='SimdMisc',         opLat=2),
               OpDesc(opClass='SimdMult',         opLat=2),
               OpDesc(opClass='SimdMultAcc',      opLat=2),
               OpDesc(opClass='SimdShift',        opLat=2),
               OpDesc(opClass='SimdShiftAcc',     opLat=2),
               OpDesc(opClass='SimdSqrt',         opLat=2),
               OpDesc(opClass='SimdFloatAdd',     opLat=2),
               OpDesc(opClass='SimdFloatAlu',     opLat=2),
               OpDesc(opClass='SimdFloatCmp',     opLat=2),
               OpDesc(opClass='SimdFloatCvt',     opLat=2),
               OpDesc(opClass='SimdFloatDiv',     opLat=2),
               OpDesc(opClass='SimdFloatMisc',    opLat=2),
               OpDesc(opClass='SimdFloatMult',    opLat=2),
               OpDesc(opClass='SimdFloatMultAcc', opLat=2),
               OpDesc(opClass='SimdFloatSqrt',    opLat=2) ]
    count = 1

class MyMemUnit(FUDesc):
    opList = [ OpDesc(opClass='MemRead'),
               OpDesc(opClass='MemWrite'),
               OpDesc(opClass='IprAccess', opLat = 2, pipelined = False) ]
    count = 1

class MyFUPool(FUPool):
    FUList = [ MyIntALU(), MyIntMultDiv(), My_FP_ALU(),
               My_FP_MultDiv(), My_SIMD_Unit(),
               MyMemUnit() ]


############################################################

## Processador

############################################################

class OoO2WCPU(DerivO3CPU):

############################################################
## Preditor de desvios
############################################################
    branchPred = TournamentBP() # Branch Predictor

############################################################
## Latências entre os diferentes estágios do pipeline.
## Pode ser usado para simular pipelines mais profundos.
############################################################
    #### Latências de avanço
    fetchToDecodeDelay   = 3 # Fetch to decode delay
    decodeToRenameDelay  = 2 # Decode to rename delay
    renameToIEWDelay     = 2 # Rename to Issue/Execute/Writeback delay
    renameToROBDelay     = 2 # Rename to reorder buffer delay
    issueToExecuteDelay  = 2 # Issue to execute delay internal to the IEW stage
    iewToCommitDelay     = 2 # Issue/Execute/Writeback to commit delay

    #### Latências de retorno
    decodeToFetchDelay   = 1 # Decode to fetch delay

    renameToFetchDelay   = 1 # Rename to fetch delay
    renameToDecodeDelay  = 1 # Rename to decode delay

    iewToFetchDelay      = 1 # Issue/Execute/Writeback to fetch delay
    iewToDecodeDelay     = 1 # Issue/Execute/Writeback to decode delay
    iewToRenameDelay     = 1 # Issue/Execute/Writeback to rename delay

    commitToFetchDelay   = 1 # Commit to fetch delay
    commitToDecodeDelay  = 1 # Commit to decode delay
    commitToRenameDelay  = 1 # Commit to rename delay
    commitToIEWDelay     = 1 # Commit to Issue/Execute/Writeback delay

############################################################
## Tamanho das estruturas do pipeline. Afetam a quantidade
## de instruções que podem ser armazenadas nos buffers.
############################################################

    fetchBufferSize  =  64 # Fetch buffer size in bytes
    fetchQueueSize   =  32 # Fetch queue size in micro-ops per thread
    numIQEntries     =  24 # Number of instruction queue entries
    numROBEntries    =  96 # Number of reorder buffer entries
    LQEntries        =  16 # Number of load queue entries
    SQEntries        =  12 # Number of store queue entries

    numPhysIntRegs   =  96 # Number of physical integer registers
    numPhysFloatRegs =  96 # Number of physical floating point registers

    numRobs          =  1 # Number of Reorder Buffers;

############################################################
## Largura das estruturas do pipeline. Afetam a quantidade
## de instruções processadas por ciclo em cada estágio.
############################################################

    fetchWidth    =  2 # Fetch width
    decodeWidth   =  2 # Decode width
    renameWidth   =  2 # Rename width
    dispatchWidth =  2 # Dispatch width
    issueWidth    =  2 # Issue width
    wbWidth       =  2 # Writeback width
    commitWidth   =  2 # Commit width
    squashWidth   = 16 # Squash width

    fuPool        = MyFUPool() # Functional Unit pool

############################################################
## Outros parâmetros. Sugestão: não mexer.
############################################################

    LSQDepCheckShift = 4 # Number of places to shift addr before check
    LSQCheckLoads = True # Should dependency violations be checked for
                         # loads & stores or just stores
    store_set_clear_period = 250000 # Number of load/store insts before
                                    # the dep predictor should be invalidated
    LFSTSize = 1024 # Last fetched store table size
    SSITSize = 1024 # Store set ID table size

    # most ISAs don't use condition-code regs # so default is 0
    _defaultNumPhysCCRegs = 0

    # For x86, each CC reg is used to hold only a subset of the flags, so we
    # need 4-5 times the number of CC regs as physical integer regs to be
    # sure we don't run out.  In typical real machines, CC regs are not
    # explicitly renamed (it's a side effect of int reg renaming),
    # so they should never be the bottleneck here.
    _defaultNumPhysCCRegs = numPhysIntRegs * 5
    numPhysCCRegs = _defaultNumPhysCCRegs # Number of physical cc registers

    activity = 0 # Initial count

    cacheStorePorts = 1 # Cache Store Ports

    trapLatency = 10 # Trap latency
    fetchTrapLatency = 1 # Fetch trap latency

    backComSize = 32 # Time buffer size for backwards communication
    forwardComSize = 32 # Time buffer size for forward communication

    smtNumFetchingThreads = 1 # SMT Number of Fetching Threads
    smtFetchPolicy = 'SingleThread' # SMT Fetch policy
    smtLSQPolicy = 'Partitioned' # SMT LSQ Sharing Policy
    smtLSQThreshold = 100 # SMT LSQ Threshold Sharing Parameter
    smtIQPolicy = 'Partitioned' # SMT IQ Sharing Policy
    smtIQThreshold = 100 # SMT IQ Threshold Sharing Parameter
    smtROBPolicy = 'Partitioned' # SMT ROB Sharing Policy
    smtROBThreshold = 100 # SMT ROB Threshold Sharing Parameter
    smtCommitPolicy = 'RoundRobin' # SMT Commit Policy

    needsTSO = True # Enable TSO Memory model

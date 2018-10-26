from m5.objects import AddrRange
from m5.objects import DDR3_1600_8x8
from m5.objects import SrcClockDomain
from m5.objects import System
from m5.objects import SystemXBar
from m5.objects import VoltageDomain

from basic_caches import BasicL1ICache, BasicL1DCache

from m5.defines import buildEnv
from m5.objects import FUDesc
from m5.objects import OpDesc

class BaseSystem(System):
    def __init__(self, options=None):
        super(BaseSystem, self).__init__()

        self.clk_domain = SrcClockDomain()
        self.clk_domain.voltage_domain = VoltageDomain()
        self.clk_domain.clock = '2.0GHz'

    def setMemoryMode(self, mode):
        self.mem_mode = 'timing'
        self.mem_ranges = [AddrRange('512MB')]

    def addCPU(self, CPU):
        self.cpu = CPU

    def addL1L2L3(self, L1DLatency, L2Cache, L3Cache):

        # Comm between L1-L2
        self.l2bus  = SystemXBar()
        # Comm betweem L2-L3
        self.l3bus  = SystemXBar()
        # Comm between L3-MainMem
        self.membus = SystemXBar()

        self.l2cache = L2Cache
        self.l3cache = L3Cache

        self.l2cache.cpu_side = self.l2bus.master
        self.l2cache.mem_side = self.l3bus.slave

        self.l3cache.cpu_side = self.l3bus.master
        self.l3cache.mem_side = self.membus.slave

        for core in self.cpu:
            core.icache  = BasicL1ICache()
            core.dcache  = BasicL1DCache(L1DLatency)

            core.icache.cpu_side = core.icache_port
            core.icache.mem_side = self.l2bus.slave
            core.dcache.cpu_side = core.dcache_port
            core.dcache.mem_side = self.l2bus.slave

    def completeSetup(self):
        self.system_port = self.membus.slave

        self.mem_ctrl = DDR3_1600_8x8()
        self.mem_ctrl.range = self.mem_ranges[0]
        self.mem_ctrl.port = self.membus.master

        return self

    def setupInterrupts(self, cpu):

        cpu.createInterruptController()
        if buildEnv['TARGET_ISA'] == 'x86':
            cpu.interrupts[0].pio = self.membus.master
            cpu.interrupts[0].int_master = self.membus.slave
            cpu.interrupts[0].int_slave = self.membus.master

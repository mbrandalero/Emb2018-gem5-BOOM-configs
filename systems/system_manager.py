from m5.util         import addToPath

# CPUs
#from ooo_1w import OoO1WCPU
#from ooo_2w import OoO2WCPU
from ooo_4w import OoO4WCPU

# System
from base_system     import BaseSystem

# Caches
from basic_caches    import BasicL1ICache, BasicL1DCache
from basic_caches    import BasicL2Cache
from basic_caches    import BasicL3Cache

# Memory bus
from m5.objects      import SystemXBar

class SystemManager:

    available_cpus = {
#        "OoO-1W" : OoO1WCPU()}
#        "OoO-2W" : OoO2WCPU(),
        "OoO-4W" : OoO4WCPU()}

    def getSystem(self, args):
        cpu_name    = args.cpu
        #num_cpu     = args.num_cpus

        sys = BaseSystem(args)

        l2  = BasicL2Cache(args)
        l3  = BasicL3Cache(args)

        cpus = []

        sys.addCPU(self.available_cpus[cpu_name])

        sys.setMemoryMode("timing")
        sys.addL1L2L3(2, l2, l3)

        sys.completeSetup()

        for core in sys.cpu:
            sys.setupInterrupts(core)

        return sys

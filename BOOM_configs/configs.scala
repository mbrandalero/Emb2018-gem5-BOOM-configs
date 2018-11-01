/** APPEND the following lines to the end of configs.scala */

class WithEmb20184WBoom extends Config((site, here, up) => {
  // Top-Level
  case XLen => 64
  // Use this boot ROM for SimDTM.
  case BootROMParams => BootROMParams(contentFileName = "./rocket-chip/bootrom/bootrom.img")
  // Core Parameters
  case BoomTilesKey => up(BoomTilesKey, site) map { r => r.copy(
     core = r.core.copy(
        fetchWidth = 4,
        decodeWidth = 4,
        numRobEntries = 128,
        issueParams = Seq(
           IssueParams(issueWidth=1, numEntries= 8, iqType=IQT_MEM.litValue),
           IssueParams(issueWidth=4, numEntries= 8, iqType=IQT_INT.litValue),
           IssueParams(issueWidth=1, numEntries= 8, iqType=IQT_FP.litValue)),
        numIntPhysRegisters = 128,
        numFpPhysRegisters = 128,
        numLsuEntries = 64,
        maxBrCount = 16,
        btb = BoomBTBParameters(nSets=512, nWays=4, nRAS=8, tagSz=13),
        enableBranchPredictor = true,
        tage = Some(TageParameters()),
        nPerfCounters = 29,
        fpu = Some(freechips.rocketchip.tile.FPUParams(sfmaLatency=4, dfmaLatency=4, divSqrt=true))),
     btb = Some(BTBParams(nEntries = 0, updatesOutOfOrder = true)),
     dcache = Some(DCacheParams(rowBits = site(SystemBusKey).beatBits, nSets=64, nWays=8, nMSHRs=4, nTLBEntries=16)),
     icache = Some(ICacheParams(fetchBytes = 4*4, rowBits = site(SystemBusKey).beatBits, nSets=64, nWays=8))
     )}
  // Set TL network to 128bits wide
  case SystemBusKey => up(SystemBusKey, site).copy(beatBytes = 16)
})
class WithEmb20182WBoom extends Config((site, here, up) => {
  // Top-Level
  case XLen => 64
  // Use this boot ROM for SimDTM.
  case BootROMParams => BootROMParams(contentFileName = "./rocket-chip/bootrom/bootrom.img")
  // Core Parameters
  case BoomTilesKey => up(BoomTilesKey, site) map { r => r.copy(
     core = r.core.copy(
        fetchWidth = 2,
        decodeWidth = 2,
        numRobEntries = 96,
        issueParams = Seq(
           IssueParams(issueWidth=1, numEntries= 8, iqType=IQT_MEM.litValue),
           IssueParams(issueWidth=2, numEntries= 8, iqType=IQT_INT.litValue),
           IssueParams(issueWidth=1, numEntries= 8, iqType=IQT_FP.litValue)),
        numIntPhysRegisters = 96,
        numFpPhysRegisters = 96,
        numLsuEntries = 32,
        maxBrCount = 8,
        btb = BoomBTBParameters(nSets=512, nWays=4, nRAS=8, tagSz=13),
        enableBranchPredictor = true,
        tage = Some(TageParameters()),
        nPerfCounters = 29,
        fpu = Some(freechips.rocketchip.tile.FPUParams(sfmaLatency=4, dfmaLatency=4, divSqrt=true))),
     btb = Some(BTBParams(nEntries = 0, updatesOutOfOrder = true)),
     dcache = Some(DCacheParams(rowBits = site(SystemBusKey).beatBits, nSets=64, nWays=8, nMSHRs=4, nTLBEntries=16)),
     icache = Some(ICacheParams(rowBits = site(SystemBusKey).beatBits, nSets=64, nWays=8, fetchBytes = 8))
     )}
  // Set TL network to 64 bits wide
  case SystemBusKey => up(SystemBusKey, site).copy(beatBytes = 8)
})
class WithEmb20181WBoom extends Config((site, here, up) => {
  // Top-Level
  case XLen => 64
  // Use this boot ROM for SimDTM.
  case BootROMParams => BootROMParams(contentFileName = "./rocket-chip/bootrom/bootrom.img")
  // Core Parameters
  case BoomTilesKey => up(BoomTilesKey, site) map { r => r.copy(
     core = r.core.copy(
        fetchWidth = 2,
        decodeWidth = 1,
        numRobEntries = 64,
        issueParams = Seq(
           IssueParams(issueWidth=1, numEntries= 8, iqType=IQT_MEM.litValue),
           IssueParams(issueWidth=1, numEntries= 4, iqType=IQT_INT.litValue),
           IssueParams(issueWidth=1, numEntries= 4, iqType=IQT_FP.litValue)),
        numIntPhysRegisters = 64,
        numFpPhysRegisters = 64,
        numLsuEntries = 16,
        maxBrCount = 8,
        btb = BoomBTBParameters(nSets=512, nWays=4, nRAS=8, tagSz=13),
        enableBranchPredictor = true,
        tage = Some(TageParameters()),
        nPerfCounters = 29,
        fpu = Some(freechips.rocketchip.tile.FPUParams(sfmaLatency=4, dfmaLatency=4, divSqrt=true))),
     btb = Some(BTBParams(nEntries = 0, updatesOutOfOrder = true)),
     dcache = Some(DCacheParams(rowBits = site(SystemBusKey).beatBits, nSets=64, nWays=8, nMSHRs=4, nTLBEntries=16)),
     icache = Some(ICacheParams(rowBits = site(SystemBusKey).beatBits, nSets=64, nWays=8, fetchBytes = 8))
     )}
  // Set TL network to 64 bits wide
  case SystemBusKey => up(SystemBusKey, site).copy(beatBytes = 8)
})

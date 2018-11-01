/** Append the following lines to Configs.scala */

class Emb20184WBoom extends Config(new WithEmb20184WBoom ++ new WithNBoomCores(1) ++ new WithoutTLMonitors ++ new freechips.rocketchip.system.BaseConfig)
class Emb20182WBoom extends Config(new WithEmb20182WBoom ++ new WithNBoomCores(1) ++ new WithoutTLMonitors ++ new freechips.rocketchip.system.BaseConfig)
class Emb20181WBoom extends Config(new WithEmb20181WBoom ++ new WithNBoomCores(1) ++ new WithoutTLMonitors ++ new freechips.rocketchip.system.BaseConfig)a

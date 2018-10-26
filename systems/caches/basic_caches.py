from m5.objects import Cache

class BasicL1ICache(Cache):

    size = '32kB'
    assoc = 8
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 16

    def __init__(self, options=None):
        super(BasicL1ICache, self).__init__()        
        pass

class BasicL1DCache(Cache):

    size = '32kB'
    assoc = 8
    tag_latency = 1
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 16

    def __init__(self, latency):
        super(BasicL1DCache, self).__init__()
        
        self.data_latency = latency
        pass

class BasicL2Cache(Cache):

    size = '256kB'
    assoc = 8
    tag_latency = 8
    data_latency = 12
    response_latency = 4
    mshrs = 16
    tgts_per_mshr = 16

    def __init__(self, options=None):
        super(BasicL2Cache, self).__init__()
        pass


class BasicL3Cache(Cache):

    size = '2MB'
    assoc = 16
    tag_latency = 12
    data_latency = 36
    response_latency = 4
    mshrs = 16
    tgts_per_mshr = 16

    def __init__(self, options=None):
        super(BasicL3Cache, self).__init__()
        pass

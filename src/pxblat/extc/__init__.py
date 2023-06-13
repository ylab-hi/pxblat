from pxblat._extc.cppbinding import *  # type: ignore


def set_state(self, d):
    self.hostName = d[0]
    self.portName = d[1]
    self.tType = d[2]
    self.qType = d[3]
    self.dots = d[4]
    self.nohead = d[5]
    self.minScore = d[6]
    self.minIdentity = d[7]
    self.outputFormat = d[8]
    self.maxIntron = d[9]
    self.genome = d[10]
    self.genomeDataDir = d[11]
    self.isDynamic = d[12]
    self.SeqDir = d[13]
    self.inName = d[14]
    self.outName = d[15]
    self.inSeq = d[16]


ClientOption.__setstate__ = set_state  # type: ignore

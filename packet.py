import bitstring


class Packet:

    def __init__(self, contentBuffer = False):
        self.stream = bitstring.BitStream()
        if contentBuffer:
            self.stream.append(bitstring.pack("bytes:{0}".format(len(contentBuffer)), contentBuffer))
            self.stream.pos = 9 * 8
        else:
            self.writeInt8(0xFB)
            self.writeInt32(0) #for length

    def readInt32(self):
        return self.stream.read('int:32')

    def readByte(self):
        return self.stream.read('int:8')

    def writeInt32(self, v):
        self.append(v, 'int:32')

    def writeInt8(self, v):
        self.append(v, 'uint:8')

    def writeBytes(self, data):
        self.writeInt32(len(data))
        self.stream.append(bitstring.pack("bytes:{0}".format(len(data)), data))

    def packetId(self):
        return bitstring.Bits(self.stream[5*8:9*8])._readuintbe(32, 0)
        #int.from_bytes(self.stream.bytes[5:9], 'big')

    def finalizePacket(self):
        self.writeInt8(0xFE)
        self.writeLength()

    def writeLength(self):
        self.stream.overwrite(bitstring.pack('int:32', self.stream.length // 8), 1 * 8)

    def append(self, v, fmt='uint:8'):
        self.stream.append(bitstring.pack(fmt, v))
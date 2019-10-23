import hashlib
import struct

class Tcp:
  def __init__(self, data=""):
    self.seq = 0
    self.ack = 0
    self.syn_flag = False
    self.ack_flag = False
    self.fin_flag = False
    self.rst_flag = False
    self.data = bytes(data, 'utf8')
    self.md5 = bytes(hashlib.md5(data.encode('utf8')).hexdigest(), 'ascii')

  def byte_pack(self):
      return struct.pack("ii????ss", self.seq, self.ack, self.syn_flag, self.ack_flag,
                      self.fin_flag, self.rst_flag, self.data, self.md5)

  def byte_unpack(self, byte_data):
      data = struct.unpack("ii????ss",byte_data)
      
      self.seq      = data[0]
      self.ack      = data[1]
      self.syn_flag = data[2]
      self.ack_flag = data[3]
      self.fin_flag = data[4]
      self.rst_flag = data[5]
      self.data     = data[6]
      self.md5      = data[7]

  def encrypt_validation(self):
      data_hash = hashlib.md5(str.encode(self.data)).hexdigest()
      return data_hash == md5

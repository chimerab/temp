import socket
import struct
import os


host = socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
s.bind(("192.168.100.10",0))
s.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)
# .ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

buf = s.recvfrom(65565)
print buf
src_ip = "%d.%d.%d.%d"%struct.unpack('BBBB', buf[0][12:16])
dest_ip = "%d.%d.%d.%d"%struct.unpack('BBBB', buf[0][16:20])
print src_ip,dest_ip

# s.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)



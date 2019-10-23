#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct
import socket
import random
from tcpHeader import Tcp
from helpers import reset_connection

# Cria o servidor udp na porta 5005
sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sckt.bind(("0.0.0.0", 5005))

while True:
    # O servidor recebe o ack e o endereço do cliente
    data, addr = sckt.recvfrom(1024)
    tcp_header = Tcp()
    tcp_header.byte_unpack(data)

    if not tcp_header.syn_flag:
        reset_connection(tcp_header, addr, sckt)
        print("Conexao Reiniciada: missing syn_flag")
        continue

    print(f"Message: {tcp_header.seq}, from: {addr}")

    # Sequencial Aleatorio do servidor
    seq = random.randint(1, 1024)

    # Header de resposta
    tcp_header.ack = tcp_header.seq + 1
    tcp_header.seq = seq
    tcp_header.ack_flag = True
        
    sckt.sendto(tcp_header.byte_pack(), addr)

    # Espera novamente pela resposta do cliente
    data, addr = sckt.recvfrom(1024)
    tcp_header.byte_unpack(data)

    if not tcp_header.ack == seq+1:
        reset_connection(tcp_header, addr, sckt)
        print("Conexao Reiniciada: ack don't match seq")
        continue
    
    if not tcp_header.ack_flag:
        reset_connection(tcp_header, addr, sckt)
        print("Conexao Reiniciada: missing ack flag")
        continue
    
    if not tcp_header.encrypt_validation:
        reset_connection(tcp_header, addr, sckt)
        print("Conexao Reiniciada: encrypt data don't match md5 attribute") 
        continue

    tcp_header.fin_flag = True
    sckt.sendto(tcp_header.byte_pack(), addr)
    print(f"Conexao estabelecida cliente: {addr}")
        

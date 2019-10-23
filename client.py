#!/usr/bin/env python
# -*- coding: utf-8 -*-
import struct
import socket
import random
from tcpHeader import Tcp
from helpers import *

# Define a conexao udp
sckt        = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_info = ('server-container', 5005)

# O for e utilizado para controlar o timeout da requisicao
for i in range(10):
    # Sequencial aleatorio do header
    seq = random.randint(80, 1024)

    # Criacao do header para o handshake
    tcp_header          = Tcp()
    tcp_header.syn_flag = True
    tcp_header.seq      = seq

    # Envio do header em formato binario
    sckt.sendto(tcp_header.byte_pack(), server_info)

    # Espera a resposta do servidor para poder validar o syn
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
    
    if not tcp_header.syn_flag:
        reset_connection(tcp_header, addr, sckt)
        print("Conexao Reiniciada: missing syn flag") 
        continue

    # Retorna o ack como seq recebido do servido mais um  
    seq = tcp_header.ack
    tcp_header.ack = tcp_header.seq + 1
    tcp_header.seq = seq
    tcp_header.syn_flag = False
    
    sckt.sendto(tcp_header.byte_pack(), server_info)

    data, addr = sckt.recvfrom(1024)
    tcp_header.byte_unpack(data)

    if tcp_header.rst_flag:
        continue
    
    print("conexao estabelecida")

    if tcp_header.fin_flag:
        break
else:
    print("Numero de requisicoes excedidas")
        
    
    

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
from tcpHeader import Tcp

def reset_connection(tcp_header, addr, sckt):
    tcp_header.rst_flag = True
    tcp_header.syn_flag = False
    tcp_header.ack_flag = False
    sckt.sendto(tcp_header.byte_pack(), addr)

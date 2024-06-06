### Solve template

```python
from pwn import *
import pdb

context.binary = elf = ELF('math-door')
glibc = ELF('libc.so.6', checksec=False)

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

if __name__ == '__main__':
    main()
```

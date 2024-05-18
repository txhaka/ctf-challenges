### consultar versión de libc y offsets comunes

```bash
libcdb file libc.so.6
```

### patchear el binario con la versión de libc del challenge para probarlo en local

```bash
pwninit --libc libc.so.6 --bin restaurant --no-template
```

### automatizar comandos de gdb

se puede crear un archivo script.gdb tal que así:

```bash
start
b *0x0000000000400ecd
c
```

y luego ejecutarlo de esta forma:

```bash
gdb-pwndbg restaurant -x script.gdb
```

### ignorar la señal de SIGALRM

en gdb (o en las opciones de gdbscript en pwntools), poner lo siguiente:

```bash
handle SIGALRM ignore
```

### salir del proceso con pwntools

usar r.close()


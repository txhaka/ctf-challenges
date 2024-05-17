### consultar versión de libc y offsets comunes

```bash
libcdb file libc.so.6
```

### patchear el binario con la versión de libc del challenge para probarlo en local

```bash
pwninit --libc libc.so.6 --bin restaurant --no-template
```

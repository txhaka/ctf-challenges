- capacidad máxima de tcachebins es 7?
- glibc leak gracias a un use after free, no se pone a NULL lo que se libera
- bypass del canary de la misma forma que en bad grades, poniendo un "." porque hay un scanf en el buffer overflow
- se envía la flag por stdin

### funciones lambda para ahorrarnos escribir de más

```python
rl   = lambda     : r.recvline()
sl   = lambda x   : r.sendline(x)
ru   = lambda x   : r.recvuntil(x)
sla  = lambda x,y : r.sendlineafter(x,y)
```

### referencias

https://github.com/hackthebox/uni-ctf-2023/tree/main/uni-ctf-2023/pwn/%5BMedium%5D%20Zombienator

https://7rocky.github.io/ctf/htb-challenges/pwn/zombienator/

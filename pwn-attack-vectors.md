### Bypass stack canary:

- Leak the canary (using another vulnerability)
- Brute-force the canary (forking processes)
- Saltarse el canary (por ejemplo, sobreescribiendo la variable i en un loop y leer después del canary)

![image](https://github.com/txhaka/ctf-directo/assets/154754392/1db636d2-f0fe-4e3f-985e-e5bbb03dfbc6)


### Bypass NX:

- ROP + leak libc address via GOT and PLT + ret2libc (pop_rdi + bin_sh + system)


### Bypass PIE:

- Leak memory address from the memory of the program
- Brtueforce overwriting only the page offset (2 last bytes)
- Bruteforce (fork processes)

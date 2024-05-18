### Common Bugs

- Signedness mixups, jae is unsigned comparison, jge is signed comparison
- Integer overflows
- Off-by-one errors (overwrite other data on the stack)

### Bypass stack canary:

- Leak the canary (using another vulnerability)
- Brute-force the canary (forking processes)
- Saltarse el canary (por ejemplo, sobreescribiendo la variable i en un loop y leer después del canary)

![image](https://github.com/txhaka/ctf-directo/assets/154754392/1db636d2-f0fe-4e3f-985e-e5bbb03dfbc6)


### Bypass NX:

- ROP + leak libc address via GOT and PLT + ret2libc (pop_rdi + bin_sh + system)


### Bypass PIE:

- Leak memory address from the memory of the program
- Bruteforce overwriting only the page offset (1 byte, fourth-less significant byte, pages are 0x1000 aligned thus 0x000 - 0x999)
- Bruteforce (fork processes)

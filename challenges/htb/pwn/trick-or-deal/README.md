![image](https://github.com/txhaka/ctf-directo/assets/154754392/d071a004-d0d4-4695-b627-9d86058b20df)

Use after free vulnerability, overwriting function pointer.

storage global variable:

![image](https://github.com/txhaka/ctf-directo/assets/154754392/a312e9c1-ed7a-4f63-b379-d747b0fd97ee)

this option (steal) frees the variable but don't set the ptr to null (use-after-free)

![image](https://github.com/txhaka/ctf-directo/assets/154754392/d071a004-d0d4-4695-b627-9d86058b20df)

and there is this function:

![image](https://github.com/txhaka/ctf-directo/assets/154754392/c38bec5c-2d07-443a-9925-10b1e62fef75)

Strategy: abuse use-after-free and overwrite the three last nibbles of the function ptr of printStorage with the offset of unlock_storage.

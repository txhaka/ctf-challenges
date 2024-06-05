Heap-based challenge where there is an off-by-one vulnerability here:

![image](https://github.com/txhaka/ctf-directo/assets/154754392/9b9c6755-8e8a-437b-a7b4-6a6d5a613636)

When a chunk is edited, strlen is used to determine the size of the chunk and be able to modify it. However, strlen only stops counting when
it encounters a NULL byte, which only happens after reading the size of the next chunk.

Essentially, it allows us to overwrite the next chunk's size.

To leak libc address, we need to insert a chunk into the unsortedbin and then edit it and insert only one byte. This way, we can get the leak 
with the show options.

We also manipulate the size and play with the metadata of freed chunks and insert the free_hook in the tcachebin. Then, overwrite it with system
and free a chunk that contains the string "/bin/sh\00".

Hemos usado una variable global cercana a las entradas del GOT. Nos deja meter el index, que es un entero, pero al
momento de indexar la variable (talis), se convierte a long.

Pasándole un -4, podemos apuntar a la entrada del GOT de exit(), que es la siguiente función que se invoca.
La sobreescribimos con el valor de read_flag, de forma que cuando se invoque exit(), obtenemos la flag.

### obstáculos

- ha sido necesario alinear el stack con un gadget ret en la cadena rop del final (ret_addr + pop_rdi + ...)
- la dirección leakeada tenía un salto de línea, por lo que r.recvline() solo contenía el primer byte + el salto de línea. la forma de solucionarlo ha sido
con un r.recv(6)

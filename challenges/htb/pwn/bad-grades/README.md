Se puede bypassear el canary sin sobreescribirlo gracias a un comportamiento extraño de scanf cuando
se le pasa un "."

No hay explicación 100% racional, porque habría que indagar en el código fuente, pero este post por
lo menos introduce el concepto.

https://rehex.ninja/posts/scanf-and-hateful-dot/


### Comportamiento extraño

Cuando se pasa un ".", se puede seguir rellenando el array de Grade[i], y además no cambiamos el valor
existente (bypass de canary).

Sin embargo, si se le pasa una letra, y scanf espera un double (con %lf), no cambia el valor, pero ya
no deja seguir rellenando el array de Grade[i], por lo que bypasseamos el canary, pero no logramos
poder sobreescribir el return address.


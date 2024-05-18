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


### Pasar valores hexadecimales a double

Ya que el input pasa a scanf, y éste último lo interpreta como float, necesitamos pasarle el equivalente en float a nuestra dirección hexadecimal. Para ello,
creamos una función to float que obtiene el equivalente en float a un valor hexadecimal:

```python
def tofloat(valor):
    return (struct.unpack("<d", p64(valor))[0])
```

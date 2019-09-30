
import math

impar = lambda n : n % 2 != 0
positivo = lambda n : n > 0
menor_abs = lambda n1, n2 : abs(n1) < abs(n2)
polar = lambda x, y : ( math.sqrt(x^2 + y^2), math.atan2(y, x) )

def ex4_5(f, g, h):
    return lambda x, y, z : h(f(x, y), g(y, z))

def quantificador_universal(lista, f):
    return not False in [f(e) for e in lista]

print(impar(3))
print(impar(4))
print(positivo(3))
print(positivo(0))
print(menor_abs(2, 3))
print(menor_abs(-4, 3))
print(polar(2, 3))

print(ex4_5(lambda a, b: a+b, lambda a, b: a*b, lambda a, b: a<b)(1, 2, 3)) 

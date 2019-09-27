import numpy as np
import sys

functionx = lambda x : np.cos(x) + x**3

#a, b y tramos serán parámetros que se digitan al ejecutar
a = float(sys.argv[1])
b = float(sys.argv[2])
tramos = int(sys.argv[3])

tamtramos = (b-a)/tramos #Tamtramos representa el tamaño de cada tramo

area = 0 #Se inicia la variable área
a1 = a #a1 será el primer punto del intervalo
b1 = a + tamtramos #b1 será el punto final del primer trapecio

for x in range(tramos):#El proceso se realizará el numero de tramos que se haya digitado 
    #Formula para hallar el área de cada trapecio, cada área calculada en cada iteración se acumula en la variable área
    area = area + ((tamtramos)*(functionx(b1)+functionx(a1))/2) 
    #print("area ", x, ": ", area)
    a1 = b1 #a para la siguiente iteración será lo que en esta fue b
    b1 = a1 + tamtramos #b para la siguiente iteración será lo que es a más el tamaño de cada tramo
    
print("El area es: ", area)
import numpy as np
import sys #Se importa para colocar los parámetros a la hora de ejecutar
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank() #Rank es el id de cada proceso 
proc = comm.Get_size() #proc es el numero de procesos

functionx = lambda x : np.cos(x) + x**3

#a, b y tramos serán parámetros que se digitan al ejecutar
a = float(sys.argv[1])
b = float(sys.argv[2])
tramos = int(sys.argv[3])

tamtramos = (b-a)/tramos #tamtramos representa el tamaño de cada tramo
eachpro = int(tramos/proc) #Eachpro representa los tramos que cada proceso debe hacer

area = 0 #Se inicia en 0 la variable área para cada proceso

a1 = a + rank * eachpro * tamtramos #a1 representa el punto inicial del rango de cada proceso
b1 = a1 + tamtramos #b1 representa el punto final de el primer trapecio de cada rango

for x in range(eachpro): #cada proceso halla el área de cuantos trapecios le corresponden
    area = area + ((tamtramos)*(functionx(b1)+functionx(a1))/2)#Formula para hallar el area de un trapecio
    #print("rank ", rank, " tramo ", x, " area : ", area, "a: ", a1, "b: ", b1)
    a1 = b1 #Para el siguiente intervalo, a vendría siendo lo que es b
    b1 = a1 + tamtramos #Para el siguiente intervalo, b vendría siendo b más el tamaño de cada tramo

alocal = 0 #Se inicia una variable en 0 que va a representar el area local de cada proceso
suma = area #Se inicia una variable suma que es igual al area. 

if(rank == 0):
    print("El area que calcula del rank  0 es ", suma) #suma es lo que calculó el rank 0
    for x in range (1,proc): #Hace un recorrido por todos los procesos. Inicia en 1 porque no se cuenta a él mismo
        alocal = comm.recv(source=x, tag=11) #Recibe lo que le envía cada proceso y lo guarda en alocal
        print("El area que calcula del rank  ", x, "es ", alocal)
        suma += alocal #En una variable se van acumulando los resultados de las áreas calculadas por cada proceso

    if(eachpro*proc != tramos): #Si faltaron tramos por calcular su área
        #Se calcula el área de un último trapecio cuyo punto a es el punto b del último proceso y punto b es el punto final
        area2 = ((b-eachpro*proc)*(functionx(b)+functionx(eachpro*proc))/2)
        #print("el area 2 es: ", area2, " con a ", eachpro*proc, " y b ", b)
        suma += area2 #Se suma el area de los trapecios que faltaban a la variable suma
    print("Area: ", suma)
else: 
    comm.send(area, dest=0, tag=11)#Cada proceso le envía al rank 0 el valor del área hallada
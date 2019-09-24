import numpy as np
import sys
from mpi4py import MPI
from mpi4py.MPI import ANY_SOURCE

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
procesos = comm.Get_size()

functionx = lambda x : np.cos(x) + x**3

a = 0
b = 10
tramos = 10

tamtramos = (b-a)/tramos
eachpro = tramos/procesos

def trape(a, b, tramos):
    h = (b - a) / tramos
    x = a
    cont = 0
    suma = functionx(x)
    for i in range(0, int(tramos-1), 1):
        x = x + h
        suma = suma + 2 * functionx(x)
        cont = cont + 1
    suma = suma + functionx(b)
    area = h * (suma / 2)
    print("De ", a, " a ", b, " el area es ", area)
    return area

suma = np.zeros(1)
inte = np.zeros(1)

eacha = a + rank*eachpro*tamtramos
eachb = eacha + eachpro*tamtramos

inte[0]= trape(eacha, eachb, eachpro)
area = inte[0]
if (rank == 0):
    for x in range (1,procesos):
        comm.Recv(suma, ANY_SOURCE)
        area = area + suma[0]
else:
    comm.Send(inte, dest = 0)

if rank == 0:
    print("Area: ", area)

#mpiexec -n 4 python3 integralParalelo.py 1 10 100
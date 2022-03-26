"""
nombres =Angel Gino Loja Manchen0
fecha = 25/1/2022
Tarea en clases

"""

class Estudiante:

    def __init__(self,nombre, nota1, nota2, notaextra):
        self.nombre =nombre
        self.nota1 = nota1
        self.nota2 = nota2
        self.notaextra= notaextra

    def notapromedio(self):
        self.nota= (self.nota1 + self.nota2)/2


    def sumatotal(self,estudiante1,notraextra1):
        if self.notaextra<=notraextra1:
            self.notaextra=notraextra1
            estudiante1.notaextra= notraextra1+1

            print("Registro de la nota extra es ingresado correctamente")
        else:
            print ("Registro de la nota extra no se realizo")

    def aprueba(self,estudiante1):
        if estudiante1.notaextra <= 10:
            print('estudiante ha aprobado')
        else: print('registro de la nota extra no se realizo')

    def __str__(self):
        return "Estudiante:" + self.nombre


class Curso:
    def __init__(self, capacidad):
        self.maquinasdisponibles=[]
        self.maquinasdisponibles=capacidad
        self.estudiante1=None

    def ingresar_estudiante (self, estudiante):
        if estudiante.nota1<=10:
            self.estudiante1=estudiante
        else:
            print ("El estudiante no se ha ingresado")

e=Estudiante("Gino", 4,7,3)
e2=Estudiante("Jair", 6,9,4)
e2.sumatotal(e,1)

#capacidad del curso 10
c=Curso(10)
c.ingresar_estudiante(e)
c.ingresar_estudiante(e2)

print (c.estudiante1)
print("Nota del estudiante e2 es:")
print(e2.notaextra)

print("Nota del estudiante e1 es:")
print(e.notaextra)

print("El promedio es:")
e.notapromedio()
print (e.nota)

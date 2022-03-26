"""
Realizar un programa que permita registrar estudiantes cuyos datos se conoce
(Codigo del estudiante, Nombre del estudiante, notas de los tres parciales )en curso,
del curso se conoce (Numero de estudiantes que pueden ingresar en el curso maximo 25
estudiantes, y el nivel del curso) en asignatura determinada, de la asignatura se conoce
(Id de la matria y su nonbre) verificar si el estudiante aprueba la materia, tomando en
cuenta que para aprobar una materia debe ser la suma de sus notas mayor o igual a 24 puntos,
si el estudiante tiene 28 puntos indicar que es un estudiante excelente. A demas deberá mostrar
el promedio de todo el curso.

Subir el desarrollo del programa en .py
"""




class Asignaturas:
    def __init__(self):
        self.materias ={
        '25 Programacion': 0,
        '26 Ingles': 0,
        '27 Sistemas Operativos': 0,
        '27 Calculo': 0,
        '28 Gestion de Proyecto': 0,
        '29 Comunicacion O,E': 0,
        '30 Arquitectura I': 0,
        }

    def cambiarAsig(self):
        can = int(input('Ingrese el numero de materias'))
        self.materias = {}
        print(self.materias)
        while True:
            if len(self.materias) != can:
                Ma = input('Ingrese el nombre de la Asignura: ')
                id = input('Ingrese el ID de la Asignura: ')
                self.materias[str(id)+' '+Ma] = 0

            else:
                break



class Curso():
    """docstring for Curso."""

    def __init__(self):

        self.lista = {}
        self.asignaturas = Asignaturas()

    def ingresar(self,can):
        self.lista = {}
        print()
        print('Ingresar Estudiantes')
        if can < 26:
            while True:
                if len(self.lista) != can:
                    alum = input('Nombre del Alumno: ')
                    id = input('id del Alumno: ')
                    self.lista[str(id)+' '+alum] = self.notas()
                else:
                    break
        else: print('Solo puede ingresar 25 alumnos como maximo')

        return self.lista


    def notas(self):
        i = 0
        lis = []
        while True:
            i += 1
            a = int(input(f'nota parcial {i}: '))
            lis.append(a)
            if len(lis)==3:
                break

        return lis

    def materia(self):

        e, lista = self.mostrar()
        if e == 8:
            self.asignaturas.cambiarAsig()
            e, lista = self.mostrar()
            nu = int(input("ingrese el numero de estudiantes: "))
            self.asignaturas.materias[lista[e-1]] = self.ingresar(nu)

        elif e <= len(lista) and e > 0:
            nu = int(input("ingrese el numero de estudiantes: "))
            self.asignaturas.materias[lista[e-1]] = self.ingresar(nu)
        else:
            print('El numero ingresado esta fuera del rango: ')

    def mostrar(self):
        n = 0
        print('escoja la Materia para ingresar los alumnos y sus notas: ')
        for i in self.asignaturas.materias.keys():
            n += 1
            print(str(n)+'.',i )

        print('8. Asignar nuevas asignaturas: ')
        lista = list(self.asignaturas.materias)
        e = int(input("escriba el numero: "))
        print(len(lista))

        return e,lista

    def resumen(self):
        n = 0
        a = list(self.lista)
        self.lista
        prom  = 0
        for i in self.lista.values():
            if sum(i) >= 24:
                if sum(i) == 28:
                    print(a[n], ' Aprobado y exonerado con: ',sum(i) )
                else:
                    print(a[n], 'Aprobado con: ',sum(i))

            else:
                print(a[n], 'Reprobrado con: ',sum(i))
            n+=1
            prom = prom+sum(i)

        prom = prom/len(a)
        print('promedio general de la asignatura: ', prom)
        self.promedioGeneral()

    def promedioGeneral(self):
        va = 0
        l = []
        for i in self.asignaturas.materias.values():
            #print(i)
            if i != 0:
                for j in i.values():
                    num = list(i)
                    va = sum(j)
                l.append(va)


        va = sum(l)/len(l)
        print('El promedio general de todo el curso es: ', va)


#cur1 = Curso()
#cur1.materia()
# try:
#     cur1.resumen()
# except:
#     pass
binaries=[('C:/Users/Usuario/Desktop/PROYECTO_FINAL/prueba2_0.py', '.')
]
to_remove = ["_AES", "_ARC4", "_DES", "_DES3", "_SHA256", "_counter"]
for b in binaries:
    found = any(

        f'{crypto}.cp37-win_amd64.pyd' in b[1]
        for crypto in to_remove

    )
    if found:
        print(f"Removing {b[1]}")
        a.binaries.remove(b)




datas=[('C:/Users/Usuario/Desktop/PROYECTO_FINAL/prueba2_0.py', '.'),
 ('C:/Users/Usuario/Desktop/PROYECTO_FINAL/prueba3_0.py', '.'),
 ('C:/Users/Usuario/Desktop/PROYECTO_FINAL/pruebaModelo.py', '.'),
('C:/Users/Usuario/Desktop/PROYECTO_FINAL/mediapipe', 'mediapipe/'),
('C:/Users/Usuario/Desktop/PROYECTO_FINAL/img', 'img/')
]
for d in datas:
    if 'C:/Users/Usuario/Desktop/PROYECTO_FINAL/prueba2_0.py' in d[0]:
        datas.remove(d)
        break

for i in datas:
    print(i)
#print(datas)
# Python3 code to demonstrate working of
# Check if any element in list satisfies a condition
# Using any()

# initializing list
test_list = [4, 5, 8, 9, 10]

# printing list
print("The original list : " + str(test_list))

# Check if any element in list satisfies a condition
# Using any()
res = any(ele > 10 for ele in test_list)

# Printing result
print("Does any element satisfy specified condition ? : " + str(res))

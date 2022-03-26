
class Asignaturas:


    def __init__(self):
        self.materias ={
        #codigo asigantura
        '4455 Programacion': 0,
        '6655 Sistemas Operativos': 0,
        '8732 Calculo': 0
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




class nota:
    def __init__(self,nota1,nota2,nota3):
        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3

    def mostrarNotas(self):
        print(
        'las notas del estudiantes son las siguientes: ',
        self.nota1,
        self.nota3,
        self.nota4
        )


class Curso():
    """docstring for Curso."""

    def __init__(self):

        self.lista = {}
        self.asignaturas = Asignaturas()

    def ingresar(self,can):
        self.lista = {}
        print()
        print('Ingresar Estudiantes')
        if can < 20:
            while True:
                if len(self.lista) != can:
                    alum = input('Nombre del Alumno: ')
                    ape = input('apellido del Alumno: ')
                    id = input('id del Alumno: ')
                    resi = input('residencia del Alumno: ')
                    telef = input('Telefono del Alumno: ')
                    self.lista[str(id)+' '+alum+' '+ape] = self.notas()
                    estu = estudiante(alum,ape,id,resi,telef)
                    notas = nota(self.lista[str(id)+' '+alum+' '+ape][0],self.lista[str(id)+' '+alum+' '+ape][1],self.lista[str(id)+' '+alum+' '+ape][2])
                    print(notas.nota1)
                else:
                    break
        else: print('Solo puede ingresar 20 alumnos como maximo')

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

        if e == 4:

            self.asignaturas.cambiarAsig()
            e, lista = self.mostrar()
            nu = int(input("ingrese el numero de estudiantes: "))
            self.asignaturas.materias[lista[e-1]] = self.ingresar(nu)

        elif e <= len(lista) and e > 0:
            self.direc = e
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

        print('4. Asignar nuevas asignaturas: ')
        lista = list(self.asignaturas.materias)
        e = int(input("escriba el numero: "))
        #print(len(lista))

        return e,lista



    def resumen(self):
        n = 0
        a = list(self.lista)
        self.lista
        prom  = 0
        self.listarepro = []
        for i in self.lista.values():
            if sum(i) >= 24:
                if sum(i) == 28:
                    print(a[n], ' Aprobado y exonerado con: ',sum(i) )
                else:
                    print(a[n], 'Aprobado con: ',sum(i))

            else:
                print(a[n], 'Reprobrado con: ',sum(i))
                self.listarepro.append(a[n])
            n+=1
            prom = prom+sum(i)

        prom = prom/len(a)
        print('promedio general de la asignatura: ', prom)

        print()
        lista = list(self.asignaturas.materias)
        print('Nomina de estudiante en la asignatura: ',lista[self.direc-1] )
        for i in self.lista:
            print(i)
        print()
        print('Nomina de estudiantes Reprobados y eliminados' )
        for j in self.listarepro:
            print(i)

        #self.promedioGeneral()



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


class estudiante:


    def __init__(self,nom,ap,cod,resi,telef):
        self.nom = nom
        self.ape = ap
        self.codi = cod
        self.resi = resi
        self.telef = telef


    def mostrarInfo(self):
        print(
        'Mi nombre es: ',
        self.nom,
        self.ape,
        ' y con codigo: ',
        self.codi
        )




cur1 = Curso()
cur1.materia()
try:
    cur1.resumen()
except:
    print('A ocurrido un error durante la ejecucion \nvuelva a intentarlo')

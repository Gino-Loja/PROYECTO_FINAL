
class estudiante:


    def __init__(self,nombre,apellido,codigo,residencia,telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.codigo = codigo
        self.residencia = residencia
        self.telefono = telefono


class Notas:
    def __init__(self, estudiante, nota1, nota2, nota3):

        self.nota1 = nota1
        self.nota2 = nota2
        self.nota3 = nota3

        self.promedioNotas([self.nota1, self.nota2, self.nota3],estudiante)


    #recibe una liista como argumento
    def promedioNotas(self, notas,estudiante):

        suma = 0
        #calculo del promedio
        for i in notas:
            suma = suma + i

        self.promedio =  [estudiante.nombre+" "+estudiante.apellido,notas,suma]

class asignatura:
    def __init__(self,nombre, codigo):
        self.nombre = nombre
        self.codigo = codigo
        self.li = []
    def ingresarEstudiante(self, estudiante):
        self.li.append(estudiante.promedio)
        self.datos = {self.codigo+" "+self.nombre: self.li}


    def imprimirLista(self):
        reprobados = []
        print('Listado de esrudiantes matriculados en la asignatura: ', self.nombre)
        for i in self.datos:

            for j in self.datos[i]:
                print(j)
                if j[2] >= 24:
                    if j[2] == 28:
                        print( j[0], ' Aprobado y exonerado con: ', j[2] )
                    else:
                        print(j[0] , ' Aprobado con: ', j[2] )

                else:
                    print(j[0] , ' Reprobado con: ', j[2] )
                    reprobados.append(j[0])
                print()

        print('Listado de estudiantes  eliminados por reprobar: ')
        for z in reprobados:
            print(z)
estudiante1 = estudiante('Juan','Lopez', 2890, 'Orellana', 59028019)
estudiante2 = estudiante('Jose','Valverde', 2270, 'Quito', 59024545)

asignatura = asignatura('Matematica', '0020')

estudiante1_notas1 = Notas(estudiante1,8, 7, 6)
estudiante2_notas2 = Notas(estudiante2,8, 9, 10)


asignatura.ingresarEstudiante(estudiante1_notas1)
asignatura.ingresarEstudiante(estudiante2_notas2)


asignatura.imprimirLista()
print('Finalizacion de la ejecucion')

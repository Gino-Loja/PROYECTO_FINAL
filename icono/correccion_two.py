
class Notas:
    def __init__(self, nota1, nota2, nota3):

        self.listaNotas = []
        self.nota1 = nota1
        self.listaNotas.append(self.nota1)
        self.nota2 = nota2
        self.listaNotas.append(self.nota2)
        self.nota3 = nota3
        self.listaNotas.append(self.nota3)




    #recibe una liista como argumento
    def promedioNotas(self,estudiante):

        promedio = 0
        #calculo del promedio
        for i in self.listaNotas:
            promedio = promedio + i
        lista = [estudiante,promedio]
        return lista

class asignatura:
    def __init__(self,nombre, codigo):
        self.nombre = nombre
        self.codigo = codigo
        self.listaEstudiantes = []
        self.estudiantesEliminados = []


    def guardarDatosEstudiante(self, dato):
        self.listaEstudiantes.append(dato)



    def mostrarEstudiantes(self):

        print('Listado de esrudiantes matriculados en la asignatura: ', self.nombre)
        for i in self.listaEstudiantes:
            print(i[0])

        print()
        print('Resultados de los promedios: ')
        self.estudiantesEliminados = []
        for x in self.listaEstudiantes:
            for y in x:
                if type(y) != str:

                    if y >= 24:
                        if  y == 28:
                            print( nombre, ' Aprobado y exonerado con: ', y )
                        else:
                            print(nombre , ' Aprobado con: ', y )

                    else:
                        print(nombre , ' Reprobado con: ', y )
                        self.estudiantesEliminados.append(x[0])
                else : nombre = y
        print()


        print('Listado de estudiantes  eliminados con nota menor a 24: ')
        for j in self.estudiantesEliminados:
            print(j)

class estudiante:


    def __init__(self,nombre,apellido,codigo,residencia,telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.codigo = codigo
        self.residencia = residencia
        self.telefono = telefono

asignatura = asignatura('Matematica', '0020')
estudiante1 = estudiante('Juan','Lopez', 2890, 'Orellana', 59028019)
estudiante2 = estudiante('Jose','Valverde', 2270, 'Quito', 59024545)



notas1 = Notas(8, 7, 6)
notas2 = Notas(8, 9, 10)
datoEstudiante1 = notas1.promedioNotas(estudiante1.nombre)
datoEstudiante2 = notas2.promedioNotas(estudiante2.nombre)

asignatura.guardarDatosEstudiante(datoEstudiante1)
asignatura.guardarDatosEstudiante(datoEstudiante2)


asignatura.mostrarEstudiantes()
print('Finalizacion de la ejecucion')


"""
Nombre = Angel GIno Loja Mancheno
PRUEBA DEL TERCER PARCIAL



n esta sección deberá subir el programa desarrollado en python que permita:

1. Mostrar un empleado.

2. Ingresar un empleado.

3. Calcular el valor de un prestamo. Un prestamo se optiene de multiplicar el valor del interes por el numero de cuotas.

Utilizar un Case para resolver el ejercicio. Subir el documento realizado en Python es decir el Evaluacion.py
"""

#clase empleado
class Empleado:
    def __init__(self,nom,ap,cod,resi):
        self.nom = nom
        self.ape = ap
        self.codi = cod
        self.resi = resi


    def mostrarInfo(self):
        print(
        'Mi nombre es: ',
        self.nom,
        self.ape,
        ' y con codigo: ',
        self.codi
        )

class Banco:
    def __init__(self):

        self.listaUsuarios =  {}
        self.lista = []



    def prestamo(self):
        nom = input('Ingrese su Nombre : ')
        ap = input('Ingrese su apellido : ')
        resi = input('Lugar de residencia: ')
        cod = input('Ingrese su codigo: ')


        can = float(input('Ingrese la Cantidad de dinero que necesita: ') )
        print(
        ' 1. 1 año\n',
        '2. 2 años\n',
        '3. 3 años'
        )
        plazo = float(input('Escoja el plazo a pagar: ') )
        print('El interes es del 5%')
        if plazo > 3 or plazo < 0:
            print('No existe tal plazo')
        else:
            empleado = Empleado(nom,ap,cod,resi)

            nuevo = plazo*12
            interes = can * 0.05
            prestamo = nuevo * interes
            print('El interes es: ', interes, ' Mensual ' , ' por ', nuevo, ' cuotas')
            totalPagar = prestamo + can
            self.lista.append(empleado.nom)

            #self.listaUsuarios[nom] = totalPagar
            self.registrar(empleado.nom,totalPagar)


    def mostrarUsuarios(self):
        lista = list(self.listaUsuarios.values())
        lista2 = list(self.listaUsuarios.keys())
        print()
        for i in range(len(lista)):
            print(lista2[i], ' debe ', lista[i],' dolares ')



    def registrar(self,nombre,total):
        self.listaUsuarios[nombre] = total

c = Banco()
#c.prestamo()

#c.mostrarUsuarios()

dic =  {'j' : 1, 'b' : 2, 'nm' : 3 , 'n' : 4}
keys= dic.keys()

for i in keys:
    print(i)

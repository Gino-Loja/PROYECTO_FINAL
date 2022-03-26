

"""
En esta sección deberá subir el programa desarrollado en python que permita:

1.Ingresar una lista de 10 computadoras

2. Mostrar la lista de computadoras que sean ingresadas por el usuario.

2. Eliminar un computadora que sea de la marca HP

3.Calcular el descuento de PC, el descuento será solo al comprador que
adquiera una PC cuyo valor sea mayor a $500.

5.Mostrar la lista de computadoras de marca INTEL

6.Mensaje de salida.
COMPUTADORA (Id_computadora, marca, modelo, precio)

CLIENTE(Id, Nombre, Apellido, Descripción )

DESCUENTO(COSTO*15%)
"""




class computadora:
    def __init__(self):
        self.lista = []

    def guardarLista(self,id,marca ,modelo,precio):

        self.lista = [id, marca, modelo, precio]

        return self.lista


class CLIENTE:
    def __init__(self, nombre, apellido, descripcion ):


        self.nombre = nombre
        self.apellido = apellido
        self.descripcion = descripcion



class DESCUENTO:

    def __init__(self):
        self.descuento = 0.15
        self.lista = []

    def ingresarCliente(self):

        nombre = input("ingrese el nombre: ")
        apellido = input("ingrese el apellido: ")
        descripcion = input("ingrese la descripcion: ")

        self.cliente = CLIENTE(nombre ,apellido,descripcion)




    def ingresarArticulos(self):
        numComputadoras = int(input('Cuantas computadoras desea Ingresar: '))
        if numComputadoras <= 10 and numComputadoras >=0:
            while True:
                if len(self.lista) != numComputadoras:

                    id = input("ingrese el id de la computadora: ")
                    marca = input("ingrese la marca: ")
                    modelo = input("ingrese el modelo: ")
                    precio = int(input("ingrese precio: "))

                    compu = computadora()
                    self.lista.append(compu.guardarLista(id,marca ,modelo,precio))
                    print(self.lista)



                else: break
        else:
            print("No puede registrar esa cantidad")
            return

        self.mostrarListacomputadoras()
        self.escojeCompu()

    def mostrarListacomputadoras(self):
        print()
        print("Lista de computadoras registradas en el Sistema: ")
        num = 0
        lis = []
        for i in self.lista:
            num = num+1
            print(str(num)+'._ ',end = '')

            for j in i:
                print(j,end = ' ')

            if i[1].lower() == 'intel':
                lis.append(i)

            print()
        print()

        if len(lis)>0:
            print("Lista de computadoras de marca Intel: ")
            for x in lis:
                for y in x:
                    print(y,end = ' ')


            print()
    def escojeCompu(self):
        print()
        id = int(input("escoja la computadora para Realizar la compra: "))
        print("Llene los siguientes Datos: ")
        self.ingresarCliente()
        if self.lista[id][3] > 500:
            print("Al ser una compra mayor de $500 recibe un descuento del 15%")

            descuento = self.calculoDescuento(self.lista[id][3])
            print(f'el cliente: {self.cliente.nombre} {self.cliente.apellido} ha realizado la compra de: ')
            print(f'{self.lista[id]}')
            print(f'El valor a pagar es de: {self.lista[id][3]-descuento}')

        else:
            print(f'el cliente: {self.cliente.nombre} {self.cliente.apellido} ha realizado la compra de: ')
            print(f'{self.lista[id]}')
            print(f'El valor a pagar es de: {self.lista[id][3]}')


        if self.lista[id][1].lower() == 'hp':
            print(f'el computador numero {id} ha sido de la lista por tener el modelo hp ')

    def calculoDescuento(self,precio):
        descuento = precio * self.descuento
        return descuento




des = DESCUENTO()
des.ingresarArticulos()


"""
En esta sección deberá subir el programa desarrollado en python que permita:

1.Ingresar una lista de 10 computadoras

2. Mostrar la lista de computadoras que sean ingresadas por el usuario.

2. Eliminar un computadora que sea de la marca HP

3.Calcular el descuento de PC, el descuento será solo al comprador que
adquiera una PC cuyo valor sea mayor a $500.

5.Mostrar la lista de computadoras de marca INTEL

6.Mensaje de salida.
COMPUTADORA (Id_cputadora, marca, modelo, precio)

CLIENTE(Id, Nombre, Apellido, Descripción )

DESCUENTO(COSTO*15%)
"""







class computador:
    def __init__(self):
        self.listaDeComputadoras =[
        [2323,'intel','wewshws',600],
        [23,'hp','wewshws',200],
        [2300,'azuss','wewshws',300],
        [2334,'intel','kkkk',700]

        ]
    def ingresarCompu(self,id,marca ,modelo,precio):
        self.listaDeComputadoras.append([id,marca ,modelo,precio])


class descuento():
    def __init__(self):
        self.des = 0.15


    def descuentoPrecio(self,precio):
        descuento = precio * self.des
        return precio - descuento


class cliente:
    def __init__(self,nombre, apellido, descripcion):

        self.nombre = nombre
        self.apellido = apellido
        self.descripcion = descripcion

    def ingresarCompra(self, art):
        pass




comp = computador()
descuen = descuento()
num = 0
lis = []





for m in comp.listaDeComputadoras:

    if m[1].lower() == 'hp':
        print(f'el computador numero {m[1]} ha sido de la lista por tener el modelo hp ')
        valor =  m
        comp.listaDeComputadoras.remove(valor)



for i in comp.listaDeComputadoras:
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

escojer = int(input('Escoja la computadora a comprar'))

print('Asigne los siguientes Datos para finalizar la compra: ')
nom = input("ingrese su nombre: ")
ape = input("ingrese su apellido: ")
descri = input("ingrese su descripcion: ")
clien = cliente(nom, ape, descri)



if comp.listaDeComputadoras[escojer-1][3]>500:
    descuento = descuen.descuentoPrecio(comp.listaDeComputadoras[escojer-1][3])
    print(f'el cliente: {clien.nombre} {clien.apellido} compro: {comp.listaDeComputadoras[escojer-1]}')
    print(f'El valor a pagar es de: {descuento}')

else:
    print(f'el cliente: {clien.nombre} {clien.apellido} compro: {comp.listaDeComputadoras[escojer-1]}')
    print(f'El valor a pagar es de: {comp.listaDeComputadoras[escojer-1][3]}')

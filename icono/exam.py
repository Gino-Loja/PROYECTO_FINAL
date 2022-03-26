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

class computador:


    def __init__(self,id_computadora, marca, modelo, precio):
        self.id = id_computadora
        self.marca = marca
        self.modelo = modelo
        self.precio = precio
        self.per = [self.id, self.marca, self.modelo, self.precio]


class cliente:
    def __init__(self,nombre,apellido,descri):
        self.nombre = nombre
        self.apellido = apellido
        self.descri = descri


    def descuento(self,compu):
        if compu[3] > 500:
            des = compu[3]*0.15
            descuento = compu[3]-des
            print('compras mayores de 500 recibe un descuento del 15%')
            print(f'{self.nombre} ha comprado: {compu[1]} {compu[2]} tiene que pagar: {descuento}')
        else:
            print('compras mayores de 500 recibe un descuento del 15%')
            print(f'{self.nombre} ha comprado: {compu[1]} {compu[2]} tiene que pagar: {compu[3]}')
print('Lista de computadoras registradas')
lista = []
computador0 = computador(2322,'hp','jjjj',600).per
lista.append(computador0)
computador1 = computador(23,'azuz','jjjj',900).per
lista.append(computador1)
computador2 = computador(232,'intel','jjjj',400).per
lista.append(computador2)
computador3 = computador(222,'inside','jjjj',400).per
lista.append(computador3)
computador4 = computador(22,'xiami','jjjj',200).per
lista.append(computador4)
computador5 = computador(99,'alt','jjjj',300).per
lista.append(computador5)
con = 0

cliente = cliente('Juan','Villa', 'ninguna')

print(f'1.{computador0} \n2.{computador1}\n3.{computador2}\n4.{computador3} \n5.{computador4} \n6.{computador5}')

cliente.descuento(computador1)
print('Lista de computadoras eliminadps con marca intel')
for i in lista:

    if i[1]=='intel':
        lista.pop(con)

    con = con +1

for z in lista:
    print(z)

import psycopg2
from dataBase.conexionDB import conexion


class DB:

    def __init__(self):
        self.conexion = conexion
        self.db = self.conexion.cursor()

    def guardar(self,datos):
        print(datos)
        try:
            insertar = "INSERT INTO estudiantes(nombre,codigo , correo) VALUES (%s, %s,%s);"
            self.db.execute(insertar, [datos[0],datos[1],datos[2]])
            insertar1 = "INSERT INTO pao(codigo_es,pao_) VALUES (%s,%s);"
            self.db.execute(insertar1, [datos[1],datos[4]])
            insertar2 = "INSERT INTO carrera(codigo_car,carrera_) VALUES (%s,%s);"
            self.db.execute(insertar2, [datos[1],datos[3]])
            self.conexion.commit()
            print('datos guardados con exito')
            return True
        except  :
            self.conexion.commit()
            return False

    def cerrarConexion(self):
        self.conexion.close()

    def consulta(self, nom):
        listaDatos = []
        cod1 = "select codigo,correo from estudiantes where nombre = %s"
        self.db.execute(cod1,[nom])
        c = self.db.fetchall()
        listaDatos.append(c[0][0])
        listaDatos.append(c[0][1])
        cod2 = "select carrera_ from carrera where codigo_car = %s"

        self.db.execute(cod2,[c[0][0]])
        b = self.db.fetchall()
        listaDatos.append(b[0][0])
        cod3 = "select pao_ from pao where codigo_es = %s"
        self.db.execute(cod3,[c[0][0]])
        a = self.db.fetchall()
        listaDatos.append(a[0][0])

        return listaDatos



    def saludar(self):
        print('hola')

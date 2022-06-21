import psycopg2
from dataBase.conexionDB import conexion


class DB:

    def __init__(self):
        self.db = conexion.cursor()

    def guardar(self,datos):
        insertar = "INSERT INTO estudiantes(codigo, nombre, correo) VALUES (%s, %s,%s);"
        self.db.execute(insertar, [datos[0],datos[1],datos[2]])
        insertar1 = "INSERT INTO pao(codigo,pao_) VALUES (%s,%s);"
        self.db.execute(insertar1, [datos[0],datos[3]])
        insertar2 = "INSERT INTO carrera(codigo,carrera_) VALUES (%s,%s);"
        self.db.execute(insertar2, [datos[0],datos[4]])
        self.db.commit()

    def cerrarConexion(self):
        self.db.close()
    def saludar(self):
        print('hola')

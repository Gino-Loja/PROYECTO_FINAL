
import psycopg2 as pg

try:
    conexion = pg.connect(
    database = "sistema_RF",
    user = "gino",
    password = "hola",
    host = "localhost",
    port = 5432
    )
    print('conexion exitosa')
except Exception as e:
    print("fallo al conectarse con la base de datos",e)

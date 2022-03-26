
import cv2
import numpy as np
import os


class modelo:

    #Importamos las fotos tomadas anteriormente

    def __init__(self,nombre):
        self.nombre = nombre
        self.path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.direccion = f'{self.path_desktop}/Fotos2/{self.nombre }'

        self.lista = os.listdir(self.direccion)
        self.etiquetas = []
        self.rostros = []
        self.cont = 0



    def reco(self):

        for nameDir in self.lista:
            nombre = self.direccion + '/' + nameDir #leer las fotos de los rostros

            for fileName in os.listdir(nombre):

                self.etiquetas.append(self.cont) #asignamos las etiquetas
                self.rostros.append(cv2.imread(nombre + '/' + fileName, 0) )

            self.cont = self.cont + 1

        #----Creamos el modelo-----
        return self.rostros,np.array(self.etiquetas),self.nombre
        #reconocimiento = cv2.face.LBPHFaceRecognizer_create()
        #----Entrenamos el modelo----
        #reconocimiento.train(self.rostros, np.array(self.etiquetas))
        #----Guardamos el modelo----
        #reconocimiento.write(f'{self.path_desktop}/Fotos2/DatosModelos/Modelo{self.nombre }.xml')
        #print("Modelo creado")

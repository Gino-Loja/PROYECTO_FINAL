
import cv2
import os
import mediapipe as mp


class Reconocer:
    """docstring fs Reconocer."""

    def __init__(self,nombre,camara = 0):

        #----importamos los nombres de las carpetas----
        self.camara = camara
        self.nombre = nombre
        self.path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.direccion  = f'{self.path_desktop}/Fotos2/{self.nombre[4]}'
        self.etiquetas = os.listdir(self.direccion)
        print("Nombres: ", self.etiquetas)

        #---- Llamar el modelo entrenado----
        self.modelo = cv2.face.LBPHFaceRecognizer_create()
        #Leer el modelo
        self.modelo.read(f'{self.path_desktop}/Fotos2/DatosModelos/Modelo{self.nombre[4] }.xml')
        #----Declaracion del detector----
        self.detector = mp.solutions.face_detection #Detector
        self.dibujo = mp.solutions.drawing_utils #funcion de Dibujo
        self.cap = None
        self.si = self.encenderCamara()




        #----Realizar la VideoCaptura----
    def encenderCamara(self):
        if self.cap == None:
            self.cap = cv2.VideoCapture(int(self.camara) + cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            #print('no existe la camara')
            return False
        else: return True

    def inicioReconocer(self):
        #----Inicializamos los parametros de la deteccion----
        if self.si:
            with self.detector.FaceDetection(min_detection_confidence=0.5) as rostros:
                #Inicializamos While True

                    #Lectura de VideoCaptura
                ret, frame = self.cap.read()

                copia = frame.copy()


                #Eliminar el error de espejo
                frame = cv2.flip(copia, 1)

                #Eliminar el erro de color
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                copia2 = rgb.copy()

                #Deteccion de rostros
                resultado = rostros.process(copia2)

                #Filtro de seguridad

                if resultado.detections is not None:
                    for rostro in resultado.detections:
                        #dibujo.draw_detection(frame, rostro)
                        #print(rostro)

                        #Extraemos el ancho y el alto de la ventana
                        al, an, _ = frame.shape

                        #Extraer x inicial & y inicial
                        xi = rostro.location_data.relative_bounding_box.xmin
                        yi = rostro.location_data.relative_bounding_box.ymin

                        #Extraer el ancho y el alto
                        ancho = rostro.location_data.relative_bounding_box.width
                        alto = rostro.location_data.relative_bounding_box.height

                        #Coversion a pixeles
                        xi = int(xi * an)
                        yi = int(yi * al)
                        ancho = int(ancho * an)
                        alto = int(alto * al)

                        #Hallamos xfinal y yfinal
                        xf = xi + ancho
                        yf = yi + alto

                        #Extraccion de pixeles
                        cara = copia2[yi:yf, xi:xf]

                        #Redimencionar las fotos
                        try:

                            cara = cv2.resize(cara, (150,200), interpolation=cv2.INTER_CUBIC)
                            cara = cv2.cvtColor(cara, cv2.COLOR_BGRA2GRAY)

                           #Realizar la prediccion
                            prediccion = self.modelo.predict(cara)

                            #Mostrar los resultados en pantalla
                            #si existe un rostro desconocido le agregara la etiqueta desconocido
                            #porque esta fuera del valor de confianza
                            #print(prediccion[1])
                            if prediccion[1] > 60:

                                cv2.putText(frame, 'desconocido', (xi, yi - 5), 1, 1.3, (255,0,0), 1, cv2.LINE_AA)
                                cv2.rectangle(frame, (xi, yi), (xf, yf), (0,0,255), 2)

                            else:
                                #mostramos si el rostro tiene o no mascarilla
                                if prediccion[0] == 0:
                                    cv2.putText(frame, '{}'.format(self.etiquetas[0]), (xi, yi - 5), 1, 1.3, (255,0,0), 1, cv2.LINE_AA)
                                    cv2.rectangle(frame, (xi, yi), (xf, yf), (255,0,0), 2)

                                elif prediccion[0] == 1:
                                    cv2.putText(frame, '{}'.format(self.etiquetas[1]), (xi, yi - 5), 1, 1.3, (0,0,255), 1, cv2.LINE_AA)
                                    cv2.rectangle(frame, (xi, yi), (xf, yf), (0,0,255), 2)

                                #cv2.rectangle(frame, (477, 324) ,(623, 470), (0,0,255), 2)
                                #cv2.putText(frame, 'que es ', (xi+50, yi), 1, 1.3, (0,0,255), 1, cv2.LINE_AA)
                                cv2.putText(frame, self.nombre[0], (xf+2, yi+10), 1, 1.3, (0,0,255), 1, cv2.LINE_AA)
                                cv2.putText(frame, self.nombre[1], (xf+2, yi+30), 1, 1.3, (0,0,255), 1, cv2.LINE_AA)
                                cv2.putText(frame, self.nombre[2], (xf+2, yi+60), 1, 1.2, (0,0,255), 1, cv2.LINE_AA)
                                cv2.putText(frame, self.nombre[3], (xf+2, yi+90), 1, 1.2, (0,0,255), 1, cv2.LINE_AA)


                                #print((xi, yi), (xf, yf))
                        except cv2.error as e:
                            pass
                                #print(frame.shape)
                                #print('Invalid frame!')
                                #cara = cv2.resize(cara, (al,an), interpolation=cv2.INTER_CUBIC)

                                #self.cap.release()
                                #print(self.cap)

                                #return False, False

                            #aquii esta
                            #cara = cv2.resize(cara, (150,200), interpolation=cv2.INTER_CUBIC)
                            #cara = cv2.cvtColor(cara, cv2.COLOR_BGRA2GRAY)

                           #Realizar la prediccion
                            #prediccion = self.modelo.predict(cara)

                            #Mostrar los resultados en pantalla
                            #si existe un rostro desconocido le agregara la etiqueta desconocido
                            #porque esta fuera del valor de confianza
                            #if prediccion[1] > 70:

                                #cv2.putText(frame, 'desconocido', (xi, yi - 5), 1, 1.3, (255,0,0), 1, cv2.LINE_AA)
                                #cv2.rectangle(frame, (xi, yi), (xf, yf), (0,0,255), 2)

                            #else:
                                #mostramos si el rostro tiene o no mascarilla
                                #if prediccion[0] == 0:
                                    #cv2.putText(frame, '{}'.format(self.etiquetas[0]), (xi, yi - 5), 1, 1.3, (255,0,0), 1, cv2.LINE_AA)
                                    #cv2.rectangle(frame, (xi, yi), (xf, yf), (255,0,0), 2)

                                #elif prediccion[0] == 1:
                                    #cv2.putText(frame, '{}'.format(self.etiquetas[1]), (xi, yi - 5), 1, 1.3, (0,0,255), 1, cv2.LINE_AA)
                                    #cv2.rectangle(frame, (xi, yi), (xf, yf), (0,0,255), 2)

                    #Mostrar los fotogramas

                return frame, self.cap
        else:
            return 1, self.cap.isOpened()
        #cerramos todo el ciclo

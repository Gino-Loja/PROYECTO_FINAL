import cv2
import mediapipe as mp
import os


class DataBase:
    def __init__(self,nombre,sin,camara = 0):
        self.camara = camara
        self.nombre = nombre+sin
        self.path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.direccion = f'{self.path_desktop}/Fotos2/{nombre}'
        self.direccion2 = f'{self.path_desktop}/Fotos2/DatosModelos'
        self.carpeta = self.direccion + '/' + self.nombre
        self.cont = 0
        self.detector = mp.solutions.face_detection #Detector
        self.dibujo = mp.solutions.drawing_utils #funcion de Dibujo
        self.cap = None
        self.si = self.encenderCamara()
        if self.si:
            self.Crearcarpeta()


    def Crearcarpeta(self):

        if (not os.path.exists(self.carpeta)):
            #print("Carpeta Principal creada ")
            os.makedirs(self.carpeta)
        if (not os.path.exists(self.direccion2)):
            os.makedirs(self.direccion2)
            #print("Carpeta Modelos creada ")


    def encenderCamara(self):
        if self.cap == None:
            self.cap = cv2.VideoCapture(self.camara +cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            #print('no existe la camara')
            return False
        else: return True

    def VideoCaptura(self):

        if self.si:
            with self.detector.FaceDetection(min_detection_confidence=0.75) as rostros:

                #Inicializamos While True

                #Lectura de VideoCaptura
                ret, frame = self.cap.read()

                #Eliminar el error de espejo
                frame = cv2.flip(frame, 1)
                #Eliminar el erro de color
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #Deteccion de rostros
                resultado = rostros.process(rgb)
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
                        cara = frame[yi:yf, xi:xf]

                        cv2.rectangle(frame, (xi, yi), (xf, yf), (255,0,0), 2)
                        cv2.putText(frame, 'Escaneando Rostro', (xi, yi+alto+20 ), 1, 1.3, (255,0,0), 1, cv2.LINE_AA)

                        #Redimencionar las fotos
                        try:
                            cara = cv2.resize(cara, (150,200), interpolation=cv2.INTER_CUBIC)

                            #Almacenar nuestras imagenes
                            cv2.imwrite(self.carpeta + "/rostro_{}.jpg".format(self.cont), cara)
                            self.cont = self.cont + 1
                            #print(self.cont)
                        except:
                            pass
                else:
                    #cv2.putText(frame,'OpenCV',(240,300),1, 5,( 0,255,0),2,cv2.LINE_AA)
                    cv2.putText(frame,' Rostro no encontrado',(90,300), 1, 2,( 0,0,255),2,cv2.LINE_AA)

                #Mostrar los fotogramas
                #cv2.imshow("Reconocimiento facial con reconocimiento de Tapabocas", frame)
                #Leyendo una tecla del teclado
                #t = cv2.waitKey(1)
                #if t == 27 or self.cont > 10: #codigo assci de esc

                    #pass
                    #self.cap.release()
                    #cv2.destroyAllWindows()
                    #print(self.cap,ret)


                return frame, self.cont, self.cap

        else: return 1,0,self.cap.isOpened()
    #Inicializamos nuestro contador

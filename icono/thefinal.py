from tkinter import *
import time
import os
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageTk
import tkinter.messagebox
import sys

#sys.path.append("E:/mediapipe/mp_env/Lib/site-packages")

class DataBase:
    def __init__(self,nombre,sin):

        self.nombre = nombre+sin
        self.path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.direccion = f'{self.path_desktop}/Fotos2/{nombre}'
        self.direccion2 = f'{self.path_desktop}/Fotos2/DatosModelos'
        self.carpeta = self.direccion + '/' + self.nombre
        self.cont = 0
        self.detector = mp.solutions.face_detection #Detector
        self.dibujo = mp.solutions.drawing_utils #funcion de Dibujo
        self.cap = None
        self.Crearcarpeta()

    def Crearcarpeta(self):

        if (not os.path.exists(self.carpeta)):
            print("Carpeta Principal creada ")
            os.makedirs(self.carpeta)
        if (not os.path.exists(self.direccion2)):
            os.makedirs(self.direccion2)
            print("Carpeta Modelos creada ")


    def encenderCamara(self):
        if self.cap == None:
            self.cap = cv2.VideoCapture(0 +cv2.CAP_DSHOW)

    def VideoCaptura(self):
        self.encenderCamara()

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
                        print(self.cont)
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


            return frame, self.cont,self.cap
    #Inicializamos nuestro contador
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
class Reconocer:
    """docstring fs Reconocer."""

    def __init__(self,nombre):

        #----importamos los nombres de las carpetas----
        self.nombre = nombre
        self.path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.direccion  = f'{self.path_desktop}/Fotos2/{self.nombre}'
        self.etiquetas = os.listdir(self.direccion)
        print("Nombres: ", self.etiquetas)

        #---- Llamar el modelo entrenado----
        self.modelo = cv2.face.LBPHFaceRecognizer_create()
        #Leer el modelo
        self.modelo.read(f'{self.path_desktop}/Fotos2/DatosModelos/Modelo{self.nombre }.xml')
        #----Declaracion del detector----
        self.detector = mp.solutions.face_detection #Detector
        self.dibujo = mp.solutions.drawing_utils #funcion de Dibujo
        self.cap = None


        #----Realizar la VideoCaptura----
    def encenderCamara(self):
        if self.cap == None:
            self.cap = cv2.VideoCapture(0 +cv2.CAP_DSHOW)
    def inicioReconocer(self):
        self.encenderCamara()

        #----Inicializamos los parametros de la deteccion----
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
                        print(prediccion[1])
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
        #cerramos todo el ciclo


class Ventana:

    def __init__(self,ini):

        self.ven = ini
        self.path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.var = None
        self.captura = None
        self.variable = None
        self.cambio = True
        self.ven.title('Reconocimiento Facial')  # esta linea se agrego luego
        #self.ven.iconbitmap(r'icono\favicon.ico')
        self.botones()
        self.ven.mainloop()

    def botones(self):
        if self.captura != None:

            self.captura.release()
            self.prueba.destroy()

        self.ven.geometry('520x350')
        self.cero = Frame(self.ven,bg="sky blue")
        self.cero.place( relwidth = 1, relheight = 1)
        self.cambio = True
        #self.cero.place(relwidth=1, relheight=1)

        self.menuPrincipal()

        btn3_mostarr = Button(self.cero,font = 'Fixedsys',text="Menu",bg= "yellow",command = lambda:self.cambiarTamanio()).grid(
        row=0,
        column=0)

        txt = Label(self.cero,text= 'SISTEMA DE RECOCIMIENTO FACIAL Y DETECCION DE MASCARILLAS',
        bg="sky blue",
        font = 'Fixedsys').grid(
        row=0,
        column=1,
        padx=10,
        pady=10)
        self.listaOpciones()
        self.imagen= PhotoImage(file=r"imagen10.png")
        Label(self.ven,image=self.imagen).place(x=150,y=80)

    def menuPrincipal(self):

        self.frameMenu = Frame(self.ven,bg = 'steel blue',width = 0,height = 300 )
        self.frameMenu.place(x = 0 , y = 35)
        #self.cero.config(bg="blue violet")
        btn1_mostrar = Button(self.frameMenu, text="Agregar Usuario",bg= "yellow",font = 'Fixedsys',
        command = lambda:self.asignarNombre()).place(
        x = 5,
        y = 10,
        )

        #############################################
        direccion = f'{self.path_desktop}/Fotos2'
        btn2_eliminar = Button(self.frameMenu, text="Reconocer",bg= "yellow",font = 'Fixedsys',
        command = lambda:self.reconocerNombre() if os.path.exists(direccion) else
        tkinter.messagebox.showinfo("Mensaje:","¡No existe ningun Usuario!")
        ).place(
        x = 5,
        y = 40)

    def cambiarTamanio(self):

        if self.cambio:

            for i in range(0,150,4):
                self.frameMenu.update()
                time.sleep(0.01)
                self.frameMenu.config(width = i)
            self.cambio = False
        else :
            for z in range(150,0,-4):
                time.sleep(0.01)

                self.frameMenu.update()
                self.frameMenu.config(width = z)

            self.cambio = True
        i = 0
        z = 0
        #self.cambio = True
    #funcion agregar Usuario
    def agregar(self,nombre,mascarilla):
        #self.var = False
        self.ven.geometry('650x540')
        self.barraMenu.destroy()
        self.variable = None
        Video = DataBase(nombre,mascarilla)
        self.objeto = Video
        self.botonPrueba()
    # elemetos de la interfaz
    def listaOpciones(self):


        self.barraMenu = Menu(self.ven)
        self.ven.config(menu = self.barraMenu,height = 300)
        #a.config(bg = "purple"
        menuAyuda = Menu(self.barraMenu,font = 'Arial 12 bold',tearoff=0)
        menuAyuda.add_command(label="Salir",command=lambda:self.ven.destroy())
        menuProject = Menu(self.barraMenu,tearoff=0)
        menuProject.add_command(label="Inicio",command=lambda:self.botones())
        self.barraMenu.add_cascade(label="Ayuda",menu=menuAyuda)
        self.barraMenu.add_cascade(label="Project",menu=menuProject)

    def scrolbar(self):

        direccion = f'{self.path_desktop}/Fotos2'
        lista = os.listdir(direccion)
        scrollbar = Scrollbar(self.tercer)
        scrollbar.grid(row=3,
        column=2,
        sticky='NS')
        self.listbox = Listbox(self.tercer, yscrollcommand=scrollbar.set,font = 'Fixedsys')
        for i in lista:
            if i != 'DatosModelos':
                self.listbox.insert("end", str(i))
        self.listbox.grid(row=3,
        column=1)

        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>', self.seleccionar)

    def seleccionar(self,eve):
        if len(self.listbox.curselection())!=0:

            self.list = self.listbox.get(self.listbox.curselection()[0])
            s = str(self.listbox.get(self.listbox.curselection()[0]))
            if  (self.nombre1.get()) != "" :
                self.nombre1.delete("0","end")
            self.nombre1.insert(0,s)

    def barraProgreso(self,frame,maximum,x,y):
        from tkinter import ttk
        s = ttk.Style()
        s.theme_use('classic')

        s.configure(
            "custom.Horizontal.TProgressbar",
            troughcolor='#5A504E',
            background='yellow',
            darkcolor="yellow",
            lightcolor="yellow",
            bordercolor="black",
            )
        self.mpb = ttk.Progressbar(frame,orient ="horizontal",
        style="custom.Horizontal.TProgressbar",
        length = 200, mode ="determinate")
        self.textobar = Label(frame,text = "",bg = 'sky blue',font = 'Fixedsys' )
        self.textobar.grid(column = x, row = y )

        self.mpb.grid(column = x, row =y+1 )

        self.mpb["maximum"] = maximum
        self.mpb["value"]  = 0

    #funciones para guardar nombres
    def asignarNombre(self):
        self.ven.geometry('300x300')
        self.frameMenu.destroy()
        con = '_sin_tapabocas'
        self.primer = Frame(self.ven,bg="sky blue")
        self.primer.place(relwidth=1, relheight=1)
        #self.variable = None
        self.nombre = Entry(self.primer,font = 'Fixedsys')
        self.nombre.grid(
        row=1,
        column=2,
        pady=15)
        ###################
        self.txt = Label(self.primer,text = 'nombre: ',bg="sky blue",font = 'Fixedsys')
        self.txt.grid(
        row=1,
        column=1,
        padx=15,
        pady=15
        )
        #result = self.nombre.get()
        self.btn1_mostrar = Button(self.primer,bg = 'yellow' ,text="Guardar",font = 'Fixedsys',
        command = lambda:self.agregar(self.nombre.get(),con) if (self.usuarioExistente(self.nombre.get(),True) == False)
        else 1)
        self.btn1_mostrar.grid(
        row=2,
        column=2,
        sticky = 'E'
        )

    def usuarioExistente(self,nombre,valor):
        direccion  = f'{self.path_desktop}/Fotos2'
        if not os.path.exists(direccion):
            return False


        print(nombre)
        etiquetas = os.listdir(direccion)
        if valor:
            if nombre in etiquetas:
                tkinter.messagebox.showinfo("Mensaje:","¡El usuario ya existe!")
                return True
            elif nombre == '':
                tkinter.messagebox.showinfo("Mensaje:","¡Primero ingresa un nombre!")
                return True
            else:
                return False
        else:
            if nombre in etiquetas:
                return False
            else:
                tkinter.messagebox.showinfo("Mensaje:","¡No existe el Usuario!")




    def UsuarioMascarilla(self,nombre):
        #self.primer.destroy()
        con = '_con_tapabocas'
        self.ven.geometry('470x300')
        self.segundo = Frame(self.ven,bg="sky blue")
        self.segundo.place(relwidth=1, relheight=1)

        btn_tomarMas = Button(self.segundo, text="tomar fotos",bg = 'yellow',font = 'Fixedsys',
        command = lambda:self.agregar(nombre, con))
        btn_tomarMas.grid(
        row=1,
        column=1,
        padx=5,
        pady=5)

        txt = Label(self.segundo,bg="sky blue", text= 'coloquese la mascarilla y cuando este listo presione el boton',
        font = 'Fixedsys').grid(
        row=2,
        column=1,
        padx=5,
        pady=5)
        #self.var = False

    def reconocerNombre(self):

        self.cero.destroy()
        self.frameMenu.destroy()
        self.ven.geometry('380x300')
        self.tercer = Frame(self.ven,bg="sky blue")
        self.tercer.place(relwidth=1, relheight=1)
        #self.list = ''
        self.scrolbar()
        #self.listbox.bind('<<ListboxSelect>>', self.seleccionar)
        #textExample.insert(0, "Default Text")
        self.nombre1 = Entry(self.tercer,font = 'Fixedsys')
        self.nombre1.grid(
        row=1,
        column=3,

        pady=25)
        #result = self.nombre.get()

        btn1_mostrar = Button(self.tercer, text=" Reconocer",bg = 'yellow',font = 'Fixedsys',
        command = lambda:self.reconocerxfat32(self.nombre1.get()) if
        (self.usuarioExistente(self.nombre1.get(),False) == False)
        else 1)
        btn1_mostrar.grid(
        row=2,
        column=3,
        padx=5,
        pady=5,
        sticky = 'E')

        text3 = Label(  self.tercer,text = 'Nombre:',bg = "sky blue",font = 'Fixedsys').grid(
        row=1,
        column=1,
        padx=5,
        pady=5,
        sticky = 'E')

        text2 = Label(  self.tercer,text = 'Lista de Usuarios',bg = "sky blue",font = 'Fixedsys').grid(
        row=2,
        column=1,
        padx=5,
        pady=5)

    def reconocerxfat32(self ,nombre):#self.variable  = True
        self.barraMenu.destroy()
        self.variable = True
        recon = Reconocer(nombre)
        self.objeto = recon
        self.botonPrueba()
        self.ven.geometry('720x500')
    # (muestra el Frame de la camera) = funcion(show_vid)
    def botonPrueba(self):

        self.prueba = Frame(self.ven,bg="sky blue")
        self.prueba.place(relwidth=1, relheight=1)
        self.lmain = Label(master=self.prueba)
        self.lmain.grid(column=0, rowspan=4, padx=5, pady=5)
        #self.lmain.pack()
        self.barraProgreso(self.prueba,250,0,8)
        self.show_vid()
        #self.barraProgreso()
        if self.variable:
            btn = Button(self.prueba,text = 'salir',bg= "yellow",font = 'Fixedsys', command = lambda:self.botones())
            btn.grid(
            row=1,
            column=2,
            padx=10,
            pady=10)



        #self.UsuarioMascarilla('sdsdsdsd')
    # guardar Modelos
    def guardarModelos(self): # self.var = None

        self.btn_4.destroy()
        self.prueba.destroy()
        self.txt.grid_forget()
        self.btn1_mostrar.destroy()
        self.nombre.grid_forget()
        self.ven.geometry('300x300')
        modelo = modelo(self.nombre.get())
        self.barraProgreso(self.prueba2,7,0,1)
        rostro, array,nombre = modelo.reco()
        reconocimiento = cv2.face.LBPHFaceRecognizer_create()
        self.prueba2.place(x = 50, y = 50)

        for i in range(1,8):
            c = "{0:.0f}".format(((i/7)*100))
            self.textobar['text'] = 'Guardando datos '+c+'%'
            self.mpb["value"] = i

            #self.prueba2.grid_columnconfigure(0, weight=1)
            self.prueba2.update()
            if i == 4 :
                #----Entrenamos el modelo----
                reconocimiento.train(rostro, array)
                #----Guardamos el modelo----
                reconocimiento.write(f'{self.path_desktop}/Fotos2/DatosModelos/Modelo{nombre}.xml')
                print("Modelo creado")
                #tkinter.messagebox.showinfo("Mensaje:", "Modelo creado")
            else:
                time.sleep(0.3)
        self.botones()
        self.var = None
    # Activar frame dentro de la ventana
    def show_vid(self):
        #cap = cv2.VideoCapture(0)
        #frame = op.oooo()
        #self.lista.append(con)
        if self.variable != True:
            frame,con,cap = self.objeto.VideoCaptura()
            if con != 250:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
                self.lmain.after(20, self.show_vid)
                self.prueba.update_idletasks()
                self.mpb["value"]  = con
                self.textobar['text']= 'Tomando Fotos...'
                self.captura = cap


            else:

                cap.release()
                self.prueba.destroy()
                if self.var == None:
                    self.ven.geometry('350x300')
                    self.UsuarioMascarilla(self.nombre.get())


                else:
                    self.segundo.destroy()
                    self.prueba2 = Frame(self.ven,bg = 'sky blue')
                    self.prueba2.place(relwidth=1, relheight=1)
                    self.ven.geometry('300x300')
                    self.btn_4 = Button(self.prueba2,bg = 'yellow', text="listo",font = 'Fixedsys'
                    ,command = lambda:self.guardarModelos())
                    self.btn_4.grid(
                    column = 0,
                    row = 0,
                    padx = 25,
                    pady = 25)
                self.var = False


                    #print(len(self.lista))
        else:
            self.mpb.destroy()
            self.textobar.destroy()
            frame,cap  = self.objeto.inicioReconocer()
            if cap != False :
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
                self.lmain.after(20, self.show_vid)
                self.captura = cap

            else:
                print('a ocurrido un  errorwwwwwwwwwwwwwwwww')
                self.captura.release()
                self.prueba.destroy()
            #print(self.captura, cap.isOpened())
            #if cap.isOpened() == False :
                #print('a ocurrido un  errorwwwwwwwwwwwwwwwww')
                #self.captura.release()
                #self.prueba.destroy()


Ventana = Ventana(Tk())




































#Ventana = Ventana(Tk())

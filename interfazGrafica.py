from tkinter import *
import customtkinter
import time
import os
import cv2
import sys
import mediapipe as mp
from PIL import Image, ImageTk
import captura_fotos as pb
import reconocimiento_fotos as pb3
import pruebaModelo as pM
import tkinter.messagebox

import dataBase as db

print(
    '(;'
    "\n"
    'creado por gino'
)


class ReconocerMultiple:
    def __init__(self,camara = 0):

        #----importamos los nombres de las carpetas----
        self.camara = camara
        self.detector = mp.solutions.face_detection #Detector
        self.dibujo = mp.solutions.drawing_utils #funcion de Dibujo
        self.cap = None


    def encenderCamara(self):
        if self.cap == None:
            self.cap = cv2.VideoCapture(self.camara +cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            #print('no existe la camara')
            return False
        else: return True

    def inicioReconocer(self,lista,lista2,lista3):
        self.si = self.encenderCamara()
        self.lista = lista3
        self.lisdire = lista2
        self.lis = lista
        n = 0
        l = []
        #----Inicializamos los parametros de la deteccion----
        if self.si:
            with self.detector.FaceDetection(min_detection_confidence=0.8) as rostros:

                ret, frame = self.cap.read()
                copia = frame.copy()

                #Eliminar el error de espejo
                frame = cv2.flip(copia, 1)

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                copia2 = rgb.copy()
                resultado = rostros.process(copia2)

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

                        try:

                            cara = cv2.resize(cara, (150,200), interpolation=cv2.INTER_CUBIC)
                            cara = cv2.cvtColor(cara, cv2.COLOR_BGRA2GRAY)

                            for i in range(len(self.lista)):

                                prediccion = self.lis[i].predict(cara)

                                if prediccion[1] < 60:
                                    #print('----------------',prediccion[1],self.lista[i])
                                    l.append(self.lista[i]) if self.lista[i] not in  l else 1

                                    if prediccion[0] == 0:
                                        cv2.putText(frame, '{}'.format(os.listdir(self.lisdire[i])[0]), (xi, yi - 5), 1, 1.3, (255,0,0), 1, cv2.LINE_AA)
                                        cv2.rectangle(frame, (xi, yi), (xf, yf), (255,0,0), 2)


                                    elif prediccion[0] == 1:
                                        cv2.putText(frame, '{}'.format(os.listdir(self.lisdire[i])[1]), (xi, yi - 5), 1, 1.3, (0,0,255), 1, cv2.LINE_AA)
                                        cv2.rectangle(frame, (xi, yi), (xf, yf), (0,0,255), 2)

                                else:
                                    if len(l) > len(self.lista)-1:#:
                                        l.pop(i)

                                    n +=1
                                    #print(n)


                            if n == len(self.lista):
                                cv2.putText(frame, 'desconocido', (xi, yi - 5), 1, 1.3, (255,0,0), 1, cv2.LINE_AA)
                                cv2.rectangle(frame, (xi, yi), (xf, yf), (0,0,255), 2)
                            n = 0

                        except cv2.error as e:
                            pass


                else:

                    l = []
                return frame,self.cap
        else: return 1, self.cap.isOpened()

class Ventana:

    ANCHO = 710
    ALTO = 690
    TL = 14
    PATHIMAGES = os.path.dirname(os.path.realpath(__file__))+"\\img\\"
    image_size = 25
    def __init__(self,ini):

        self.ven = ini
        self.path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.var = None
        self.captura = None
        self.variable = None
        #self.cambio = True
        self.CAMBIO = False
        self.camaraCambio = IntVar()
        self.switch = IntVar()
        self.mini = IntVar()
        self.FRAME2 = BooleanVar()
        self.FRAME3 = BooleanVar()
        self.reconocimientoMultiple = ReconocerMultiple()
        #self.ven.resizable(0, 0)
        self.ven.geometry(f"{self.ANCHO}x{self.ALTO}")
        self.listaframe = []
        self.listaDatos = []
        customtkinter.set_appearance_mode("dark")
        #customtkinter.deactivate_automatic_dpi_awareness()
        self.img_dir = self.resource_path("img")
        #self.etiqueta = Label(self.ven)
        self.ven.bind('<Configure>',lambda a : self.maximizar(a))
        self.ven.title('Reconocimiento Facial')  # esta linea se agrego luego\
        self.guardarDB = db.DB()
        self.ven.columnconfigure(1, weight=1)
        self.ven.rowconfigure(0, weight=1)
        #self.ven.iconbitmap(r'icono\favicon.ico')
        self.botones()
        self.switch_2.select()
        #self.ven.mainloop()

    def controlSalir(self):
        self.ven.protocol('WM_DELETE_WINDOW',
         lambda:tkinter.messagebox.showinfo("Mensaje:","¡No puedes cerrar la ventana!"))

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def cambiarCamara(self):
        self.seis = Frame(self.ven,bg="sky blue")
        self.seis.place(relwidth = 1, relheight = 1)

        R1 = Radiobutton(self.seis,text_font = (self.TL), text="Camara interna",font = 'Fixedsys',
        bg="sky blue",
        activebackground ="sky blue",
        variable=self.camaraCambio,
        value=0)
        R1.grid( padx = 200,row = 0,column = 0,pady = 50)

        R2 = Radiobutton(self.seis, text_font = (self.TL),text="Camara externa",
        bg="sky blue",
        activebackground ="sky blue",
        variable=self.camaraCambio,
        value=1)
        R2.grid(row = 1,column = 0)

    def botones(self):
        #self.ven.bind("<self.state()>",print('sasasas'))
        if self.captura != None:

            self.captura.release()
            self.prueba.destroy()
        #self.etiqueta.destroy()
        #[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]
        if self.FRAME2.get() == True:
            self.primer.destroy()
        if self.FRAME3.get() == True:
            self.tercer.destroy()

        self.FRAME3.set(False)
        self.FRAME2.set(False)
        #[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]
        self.menuPrincipal()
        self.ven.protocol('WM_DELETE_WINDOW',lambda: self.ven.destroy())
        #self.ven.geometry('520x350')

        self.cero = customtkinter.CTkFrame(self.ven)
        self.cero.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.cero.rowconfigure((0,1,2), weight=1)
        self.cero.columnconfigure((0,1), weight=1)

        frameHijo = customtkinter.CTkFrame(self.cero)
        frameHijo.grid(column = 1, row = 1, sticky="nswe",padx=20)
        frameHijo.rowconfigure((0,1,2), weight=1)
        frameHijo.columnconfigure((0), weight=1)

        txt = customtkinter.CTkLabel(self.cero,text_font = (self.TL),
        text= 'SISTEMA DE RECOCIMIENTO\n FACIAL Y DETECCION DE MASCARILLAS'
        ).grid(
        row=0,
        column=0,
        columnspan = 2,
        sticky="n",
        padx=5,
        pady=10)
        #settings_image = PhotoImage(self.PATHIMAGES+"chevron-left-16.png")
        self.settings_image1 = ImageTk.PhotoImage(Image.open(self.PATHIMAGES+"device-camera-video-24.png").resize((self.image_size, self.image_size)))


        txt2 = customtkinter.CTkLabel(frameHijo, text_font = (self.TL),
        text = "Habilitar camara:").grid(column = 0,
        padx=5,
        pady=10,
        row = 0)
        imge = customtkinter.CTkLabel(frameHijo, image = self.settings_image1 )
        imge.grid(column = 1,
        padx=5,
        pady=10,
        row = 0)

        radiobutton_1 = customtkinter.CTkRadioButton(master=frameHijo, text_font = (self.TL),text="Interna",
        variable= self.camaraCambio, value=0)
        radiobutton_2 = customtkinter.CTkRadioButton(master=frameHijo,text_font = (self.TL), text="Externa",
        variable= self.camaraCambio, value=1)
        radiobutton_1.grid(column = 0, row = 1,
        padx=5,
        pady=15)
        radiobutton_2.grid(column = 0, row = 2,padx=5,
        pady=15)







        #self.listaOpciones()
        im = self.img_dir+"\imagen1.png"

    def maximizar(self,a):


        if self.ven.state() != "zoomed":
            self.listaframe.append(a)
            c = len(self.listaframe)
            if c %  2 == 0:
                self.mini.set(c)


        if self.mini.get() %  2 == 0:

            if self.ven.state() == "zoomed":
                self.ven.geometry(f"{self.ANCHO}x{self.ALTO}")

                self.listaframe = []


        if len(self.listaframe) > 101:
            self.listaframe = []


    def change_mode(self):

        WIDTH = self.ven.winfo_width()
        HEIGHT = self.ven.winfo_height()
        X_POS = self.ven.winfo_x()
        Y_POS = self.ven.winfo_y()

        current_state = self.ven.state()
        print(current_state)
        self.ven.state('normal')

        self.ven.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, X_POS, Y_POS))

        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

        if current_state == 'zoomed':
            self.ven.state("zoomed")
        self.listaframe = []

    def menuPrincipal(self):

        self.frameMenu = customtkinter.CTkFrame(self.ven,
        corner_radius=15)

        self.frameMenu.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        self.listaframe.append(self.frameMenu)

        #self.cero.config(bg="blue violet")
        textMenu = customtkinter.CTkLabel(master=self.frameMenu,
        text_font = (self.TL),text = 'Menu',
        fg_color=("white", "gray1"))
        textMenu.place(
        relx=0.5, rely=0.2,
        anchor = CENTER
        )

        btn1_mostrar = customtkinter.CTkButton(self.frameMenu,text_font = (self.TL),
        text="Agregar Usuario",
        fg_color=("gray75", "gray30"),
        command = lambda:self.asignarNombre())
        btn1_mostrar.place(
        relx=0.5, rely=0.4,
        anchor = CENTER

        )
        #j
        #############################################
        direccion = f'{self.path_desktop}/Fotos2'
        btn2_eliminar = customtkinter.CTkButton(self.frameMenu,text_font = (self.TL),
        text="Reconocer",
        fg_color=("gray75", "gray30"),
        command = lambda:self.reconocerNombre() if os.path.exists(direccion) else
        tkinter.messagebox.showinfo("Mensaje:","¡No existe ningun Usuario!")
        )
        btn2_eliminar.place(
        relx=0.5, rely=0.6,
        anchor = CENTER)

        self.switch_2 = customtkinter.CTkSwitch(master=self.frameMenu,

                                                text="Dark Mode",text_font = (self.TL),
                                                command=self.change_mode)
        self.switch_2.place(
        relx=0.5, rely=0.93,
        anchor = CENTER
        )
        self.switch_2.select() if self.switch.get() == 1 else self.switch_2.deselect()


    def agregar(self,nombre,mascarilla):
        #self.var = False

        self.variable = None
        #Video = pb.DataBase(nombre,mascarilla,self.camaraCambio.get())
        if len(self.listaDatos)>1:
            a = self.guardarDB.guardar(list(map(lambda x : x.get(),self.listaDatos)))
            if not a :
                tkinter.messagebox.showinfo("Mensaje:","¡Tu codigo o correo ya existen en la base de datos!")
                return
            else:

                Video = pb.DataBase(nombre,mascarilla,self.camaraCambio.get())
                self.objeto = Video
                self.botonPrueba()
                self.controlSalir()
                self.listaDatos = []

        else:
            Video = pb.DataBase(nombre,mascarilla,self.camaraCambio.get())
            self.objeto = Video
            self.botonPrueba()

    def listaOpciones(self):


        self.barraMenu = Menu(self.ven,background='blue',fg='blue')
        self.ven.config(menu = self.barraMenu,height = 300)
        #a.config(bg = "purple"
        menuAyuda = Menu(self.barraMenu,tearoff=0)
        menuAyuda.add_command(label="Salir",command=lambda:self.ven.destroy())
        menuAyuda.add_command(label="Cambiar camara..", command = lambda:self.cambiarCamara())
        menuAyuda.add_command(label="Version 1.0")

        menuProject = Menu(self.barraMenu,tearoff=0)
        menuProject.add_command(label="Inicio",command=lambda:self.botones())
        self.barraMenu.add_cascade(label="Ayuda",menu=menuAyuda)
        self.barraMenu.add_cascade(label="Volver",menu=menuProject)

    def scrolbar(self,frame):
        self.lista1 = []
        direccion = f'{self.path_desktop}/Fotos2'
        lista = os.listdir(direccion)
        scrollbar = Scrollbar(frame)
        scrollbar.grid(row=2,
        column=0,
        sticky='sne'
        ,pady = 15)
        self.listbox = Listbox(frame,font=(13), yscrollcommand=scrollbar.set,height = 5)
        for i in lista:
            if i != 'DatosModelos':
                self.listbox.insert("end", str(i))
        self.listbox.grid(row=2,
        column=0,
        sticky = 'wnse',
        padx = 15,
        pady = 15)
        scrollbar.config(command=self.listbox.yview)
        self.listbox.bind('<<ListboxSelect>>', self.seleccionar)#, font=('Aerial 13')
        if self.switch_2.get() == 1: self.listbox.configure(background="gray22", foreground="white")

    def seleccionar(self,eve):

        if len(self.listbox.curselection())!=0:

            self.list = self.listbox.get(self.listbox.curselection()[0])
            self.s = str(self.listbox.get(self.listbox.curselection()[0]))
            if self.n:
                if  (self.nombre1.get()) != "" :
                    self.nombre1.delete("0","end")
                self.nombre1.insert(0,self.s)
            else:
                if len(self.lista1)<5:
                    self.lista1.append(self.s) if self.s not in self.lista1 else 1
                    self.etiqueta['text'] =''
                    for i in self.lista1:self.etiqueta['text'] =i+'\n'+self.etiqueta['text']#self.etiqueta['text'] +'\n'+self.s
                    #print(self.etiqueta['text'],self.lista1)
                else:
                    tkinter.messagebox.showinfo("Mensaje:","¡No se puede agregar mas usuarios!")

    def barraProgreso(self,frame):

        self.mpb = customtkinter.CTkProgressBar(frame,width = 250,height = 13)
        self.textobar = customtkinter.CTkLabel(frame, text_font = (self.TL),text = "" )
        #self.textobar.grid(column = x, row = y )
        # if pos:
        self.mpb.grid(column = 0, row =2 ,pady = 15,sticky="we",padx = 25)
        self.textobar.grid(column = 0, row = 1 )
        # else:
        #     self.mpb.place(x = x, y = y )
        #     self.textobar.place(x = x+20, y = y-22 )

        #self.mpb.set()
        #self.mpb["value"]  = 0

    #funciones para guardar nombres
    #==============
    #self.FRAME2 = self.primer
    #=============
    def asignarNombre(self):
        self.captura  = None
        self.ven.protocol('WM_DELETE_WINDOW',lambda: self.ven.destroy())
        #print(self.switch_2.get(),'fe w')
        self.switch.set(self.switch_2.get())
        self.cero.destroy()
        self.frameMenu.destroy()

        self.FRAME2.set(True)

        con = '_sin_mascarilla'

        self.primer = customtkinter.CTkFrame(self.ven)
        self.primer.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.primer.rowconfigure((0,1,2,3,4,5), weight=1)
        self.primer.columnconfigure(1, weight=1)

        #self.variable = None
        self.nombre = customtkinter.CTkEntry(self.primer,width=200,text_font = (self.TL))
        self.nombre.grid(
        row=0,
        column=1,
        padx=15,
        pady=15,
        sticky="we")

        self.listaDatos.append(self.nombre)
        self.codigo = customtkinter.CTkEntry(self.primer,text_font = (self.TL),width=200)
        self.codigo.grid(
        row=1,
        column=1,
        padx=15,
        pady=15,
        sticky="we")
        self.listaDatos.append(self.codigo)

        self.correo = customtkinter.CTkEntry(self.primer,text_font = (self.TL),width=200)
        self.correo.grid(
        row=2,
        column=1,
        padx=15,
        pady=15,
        sticky="we")
        self.listaDatos.append(self.correo)
        self.carr = customtkinter.CTkEntry(self.primer,width=200,text_font = (self.TL))
        self.carr.grid(
        row=3,
        column=1,
        padx=15,
        pady=15,
        sticky="we")
        self.listaDatos.append(self.carr)
        self.pao = customtkinter.CTkEntry(self.primer,text_font = (self.TL),width=50)
        self.pao.grid(
        row=4,
        column=1,
        padx=15,
        pady=15,
        sticky="w")
        self.listaDatos.append(self.pao)
        ###################
        self.txt = customtkinter.CTkLabel(self.primer,text_font = (self.TL),text = 'Nombre: ',width = 55)
        self.txt.grid(
        row=0,
        column=0,
        padx=15,
        pady=15,
        sticky="we")

        txt2 = customtkinter.CTkLabel(self.primer,text_font = (self.TL),text = 'Codigo: ',width = 55)
        txt2.grid(
        row=1,
        column=0,
        padx=15,
        pady=15,
        sticky="we")

        txt3 = customtkinter.CTkLabel(self.primer,text_font = (self.TL),text = 'Correo: ',width = 55)
        txt3.grid(
        row=2,
        column=0,
        padx=15,
        pady=15,
        sticky="we")

        txt4 = customtkinter.CTkLabel(self.primer,text_font = (self.TL),text = 'Carrera: ',width = 55)
        txt4.grid(
        row=3,
        column=0,
        padx=15,
        pady=15,
        sticky="we")

        txt5 = customtkinter.CTkLabel(self.primer,text_font = (self.TL),text = 'Pao ',width = 55)
        txt5.grid(
        row=4,
        column=0,
        padx=15,
        pady=15,
        sticky="we")


        #result = self.nombre.get()

        self.btn1_mostrar = customtkinter.CTkButton(self.primer,text_font = (self.TL),
        text="Guardar",

        command = lambda:self.agregar(self.nombre.get(),con) if (self.usuarioExistente(self.listaDatos,True) == False)
        else 1)
        self.btn1_mostrar.grid(
        row=5,
        column=1,
        padx=15,
        pady=15,
        sticky="e")


        settings_image = ImageTk.PhotoImage(Image.open(self.PATHIMAGES+"chevron-left-16.png").resize((self.image_size, self.image_size)))
        #bell_image = ImageTk.PhotoImage(Image.open(PATH + "/test_images/bell.png").resize((image_size, image_size)))

        self.inicio_ = customtkinter.CTkButton(self.primer,image = settings_image ,text_font = (self.TL),
        text="Inicio",
        command = lambda:self.botones())
        self.inicio_.grid(
        row=5,
        column=0,
        padx=15,
        pady=15,
        sticky="n")

    def usuarioExistente(self,nombre,valor):

        direccion  = f'{self.path_desktop}/Fotos2'
        if not os.path.exists(direccion):
            return False


        #print(nombre)

        etiquetas = os.listdir(direccion)
        if valor:
            if nombre[0].get() in etiquetas:
                tkinter.messagebox.showinfo("Mensaje:","¡El usuario ya existe!")
                return True
            elif nombre[0].get() == '':
                tkinter.messagebox.showinfo("Mensaje:","¡Primero ingresa un nombre!")
                return True
            elif len(list(filter(lambda x: x.get() == '',nombre ))) >= 1:
                tkinter.messagebox.showinfo("Mensaje:","¡Llena todos los campos!")
                return True

            else:
                return False
        else:
            if nombre in etiquetas:
                self.dataUser = self.guardarDB.consulta(nombre)
                self.dataUser.append(nombre)

                return False

            else:
                tkinter.messagebox.showinfo("Mensaje:","¡No existe el Usuario!")

    def UsuarioMascarilla(self,nombre):
        #self.primer.destroy()
        con = '_con_mascarilla'
        #self.ven.geometry('500x300')
        self.segundo = customtkinter.CTkFrame(self.ven)

        self.segundo.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.segundo.rowconfigure((0,1), weight=1)
        self.segundo.columnconfigure(0, weight=1)
        btn_tomarMas = customtkinter.CTkButton(master = self.segundo,
        text="tomar fotos",
        text_font = (self.TL),
        width=150,
        command = lambda:self.agregar(nombre, con))
        btn_tomarMas.grid(
        row=0,
        column=0,
        padx=15,
        pady=15,
        )

        txt = customtkinter.CTkLabel(self.segundo,
        text_font = (self.TL),
        text= 'Coloquese la mascarilla y cuando este listo presione el boton'
        ).grid(
        row=1,
        column=0,
        sticky="n",
        padx=15,
        pady=15)
        #self.var = False

    def reconocerNombre(self):
        self.captura  = None
        self.switch.set(self.switch_2.get())
        self.cero.destroy()
        self.frameMenu.destroy()
        self.FRAME3.set(True)
        self.tercer = customtkinter.CTkFrame(self.ven)
        self.tercer.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.tercer.rowconfigure((0,1,2), weight=1)
        self.tercer.columnconfigure((0,1), weight=1)
        self.n = True
        #self.list = ''
        self.scrolbar(self.tercer)
        #self.listbox.bind('<<ListboxSelect>>', self.seleccionar)
        #textExample.insert(0, "Default Text")
        self.nombre1 = customtkinter.CTkEntry(self.tercer,text_font = (self.TL),)
        self.nombre1.grid(
        row=0,
        column=1,
        pady=15,
        padx = 15,
        sticky = 'ew')
        #result = self.nombre.get()
        btn1_mostrar = customtkinter.CTkButton(self.tercer,
        text_font = (self.TL),
        text=" Reconocer",
        command = lambda:self.reconocerxfat32(pb3.Reconocer(self.dataUser,self.camaraCambio.get())) if
        (self.usuarioExistente(self.nombre1.get(),False) == False)
        else 1)
        btn1_mostrar.grid(
        row=1,
        column=1,
        pady=15,
        padx = 15,
        sticky = 'e')

        text3 = customtkinter.CTkLabel(  self.tercer,text_font = (self.TL),
        text = 'Nombre:').grid(
        row=0,
        column=0,
        pady=15,
        padx = 15
        )

        text2 = customtkinter.CTkLabel(  self.tercer,text_font = (self.TL),
        text = 'Lista de Usuarios').grid(
        row=1,
        column=0,
        pady=15,
        padx = 15
        )# scrolbar
        inicio_ = customtkinter.CTkButton(self.tercer,text_font = (self.TL),
        text="Inicio",
        command = lambda:self.botones())
        inicio_.grid(
        row=2,
        column=1,
        padx=15,
        pady=15,
        sticky="s"
        )

    def reconocerxfat32(self,clase):#self.variable  = True

        self.variable = True
        self.CAMBIO = False
        #recon = pb3.Reconocer(nombre)
        self.objeto = clase
        #self.ven.geometry('720x500')
        self.botonPrueba()
    # (muestra el Frame de la camera) = funcion(show_vid)
    def botonPrueba(self):
        #self.cero.destroy()#cambio aquii
        self.prueba = customtkinter.CTkFrame(self.ven)
        self.prueba.grid(
        column=1,row=0,
         padx=15,
         pady=15,
         sticky="nswe"
        )
        self.prueba.rowconfigure((0), weight=1)
        self.prueba.columnconfigure((0), weight=1)
        self.lmain = customtkinter.CTkLabel(master=self.prueba)
        self.lmain.grid(column=0, row=0, sticky="nswe", padx=15, pady=15)

        if self.variable:
            self.btnsalir = customtkinter.CTkButton(self.prueba,text_font = (self.TL),text = 'salir', command = lambda:self.botones())
            self.btnsalir.grid(
            row=1,
            column=0,
            padx=10,
            pady=10)

        self.barraProgreso(self.prueba)

        self.show_vid()
        #self.barraProgreso(self.prueba)




        #self.UsuarioMascarilla('sdsdsdsd')
    # guardar Modelos
    def guardarModelos(self): # self.var = None
        self.captura  = None
        self.prueba2 = customtkinter.CTkFrame(self.ven)
        self.prueba2.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.prueba2.rowconfigure((1,2), weight=1)
        self.prueba2.columnconfigure(0, weight=1)

        self.controlSalir()
        #self.btn_4.destroy()
        #self.prueba.destroy()
        self.txt.grid_forget()
        self.btn1_mostrar.destroy()
        self.nombre.grid_forget()
        #self.ven.geometry('300x300')
        modelo = pM.modelo(self.nombre.get())
        self.barraProgreso(self.prueba2)
        #self.mpb.grid(column = 0, row =0, pady = 15)
        rostro, array,nombre = modelo.reco()
        reconocimiento = cv2.face.LBPHFaceRecognizer_create()
        #self.prueba2.place(x = 50, y = 50)
        for i in range(1,8):
            c = "{0:.0f}".format(((i/7)*100))
            self.textobar['text'] = 'Guardando datos '+c+'%'
            #self.mpb["value"] = i
            self.mpb.set(0.145*i)

            #self.prueba2.grid_columnconfigure(0, weight=1)
            self.prueba2.update()
            if i == 4 :
                #----Entrenamos el modelo----
                reconocimiento.train(rostro, array)
                #----Guardamos el modelo----
                reconocimiento.write(f'{self.path_desktop}/Fotos2/DatosModelos/Modelo{nombre}.xml')
                #print("Modelo creado")
                #tkinter.messagebox.showinfo("Mensaje:", "Modelo creado")
            else:
                time.sleep(0.3)


        self.botones()
        self.var = None
    # Activar frame dentro de la ventana

    """
    funciones de reconocimiento_multiple:
    """
    def reconocerMultiple(self):
        self.cero.destroy()
        self.frameMenu.destroy()
        #self.ven.geometry('380x320')
        self.cuarto = Frame(self.ven,bg="sky blue")
        self.cuarto.place(relwidth=1, relheight=1)

        self.n = False
        self.etiqueta = Label(self.cuarto,font = 'Fixedsys',justify = 'center',width = 15,height = 6)
        self.etiqueta.grid(
        row=1,
        column=3,
        pady=10)

        self.scrolbar(self.cuarto)

        btn1_mostrar = Button(self.cuarto, text=" Reconocer",bg = 'yellow',activebackground ="yellow",font = 'Fixedsys',
        command = lambda:self.cargarPersonas(self.lista1))
        btn1_mostrar.grid(
        row=2,
        column=3,
        padx=5,
        pady=5,
        sticky = 'E')

        text3 = Label(  self.cuarto,text = 'Nombres:',bg = "sky blue",font = 'Fixedsys').grid(
        row=1,
        column=1,
        padx=5,
        pady=5,
        sticky = 'NE')

        btn1_borrar = Button(self.cuarto, text="Borrar",bg = 'yellow',font = 'Fixedsys',
        command = lambda: self.etiqueta.config(text='') or self.lista1.clear())
        btn1_borrar.grid(
        row=1,
        column=4,
        padx=5,
        pady=5,
        sticky = 'S')

    def cargarPersonas(self,lista):
        self.controlSalir()
        info = []
        lis = []
        lisdire = [0]*len(lista)
        self.cuarto.destroy()
        self.quinto = Frame(self.ven,bg="sky blue")
        self.quinto.place( relwidth = 1, relheight = 1)
        self.barraProgreso(self.quinto)

        self.textobar['text'] = 'Cargando Datos'

        for i in range(len(lista)):

            self.mpb["value"]  = i+1

            m = cv2.face.LBPHFaceRecognizer_create()
            m.read(f'{self.path_desktop}/Fotos2/DatosModelos/Modelo{lista[i]}.xml')
            self.quinto.update()
            info.append(m)
            #print(info[i],m)
            lisdire[i]  = f'{self.path_desktop}/Fotos2/{lista[i]}'
            #self.etiquetas = os.listdir(self.direccion)
            #print(os.listdir(lisdire[i])[0])
            del m

        #info,lisdire
        #ReconocerMultiple(info,lisdire,lista,self.camaraCambio.get())
        self.reconocimientoMultiple.camara = self.camaraCambio.get()
        self.reconocerxfat32(lambda:self.reconocimientoMultiple.inicioReconocer(info,lisdire,lista))
    """
    -----------------------------------
    """
    def show_vid(self):

        if self.variable != True:
            frame,con,cap = self.objeto.VideoCaptura()
            if cap  != False:
                if con != 250:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.lmain.imgtk = imgtk
                    self.lmain.configure(image=imgtk,width=620,height=680 )
                    self.lmain.after(20, self.show_vid)
                    self.prueba.update_idletasks()
                    self.mpb.set(0.004*con)
                    self.textobar['text']= 'Tomando Fotos...'
                    self.captura = cap


                else:

                    cap.release()
                    self.prueba.destroy()
                    if self.var == None:
                        #self.ven.geometry('350x300')
                        self.UsuarioMascarilla(self.nombre.get())
                        self.var = False

                    else:
                        self.segundo.destroy()
                        self.guardarModelos()




                        #print(len(self.lista))
            else:
                self.mpb.destroy()

                c = tkinter.messagebox.showerror("Error", "Camara no habilitada")
                if c == 'ok':
                    self.botones()

        else:
            if self.CAMBIO != True:

                self.mpb.destroy()
                self.textobar.destroy()
                self.CAMBIO = True
            frame,cap  = self.objeto.inicioReconocer()
            #print(frame)
            if cap != False :
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)

                imgtk = ImageTk.PhotoImage(image=img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
                self.lmain.after(20, self.show_vid)
                self.captura = cap

            else:
                #print('a ocurrido un  errorwwwwwwwwwwwwwwwww',cap)
                c = tkinter.messagebox.showerror("Error", "Camara no habilitada")

                if c == 'ok':
                    #self.btnsalir.destroy()
                    self.botones()

if __name__ == "__main__":
    Ventana = Ventana(customtkinter.CTk())
    Ventana.ven.mainloop()

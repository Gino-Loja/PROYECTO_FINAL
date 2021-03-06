from tkinter import *
import time
import os
import cv2
import sys
import mediapipe as mp
from PIL import Image, ImageTk
import prueba2_0 as pb
import prueba3_0 as pb3
import pruebaModelo as pM
import tkinter.messagebox

print(


    '(;'

)


class ReconocerMultiple:
    def __init__(self,lista,lista2,lista3,camara = 0):

        #----importamos los nombres de las carpetas----
        self.camara = camara
        self.detector = mp.solutions.face_detection #Detector
        self.dibujo = mp.solutions.drawing_utils #funcion de Dibujo
        self.lista = lista3
        self.lisdire = lista2
        self.lis = lista
        self.cap = None
        self.si = self.encenderCamara()

    def encenderCamara(self):
        if self.cap == None:
            self.cap = cv2.VideoCapture(self.camara +cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            #print('no existe la camara')
            return False
        else: return True

    def inicioReconocer(self):

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



 # root is your root window

class Ventana:

    def __init__(self,ini):

        self.ven = ini
        self.path_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        self.var = None
        self.captura = None
        self.variable = None
        self.cambio = True
        self.camaraCambio = IntVar()
        self.ven.resizable(0, 0)

        self.img_dir = self.resource_path("img")
        #self.etiqueta = Label(self.ven)
        self.ven.title('Reconocimiento Facial')  # esta linea se agrego luego
        #self.ven.iconbitmap(r'icono\favicon.ico')
        self.botones()
        self.ven.mainloop()


    def controlSalir(self):
        self.ven.protocol('WM_DELETE_WINDOW',
         lambda:tkinter.messagebox.showinfo("Mensaje:","??No puedes cerrar la ventana!"))

    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def cambiarCamara(self):
        self.seis = Frame(self.ven,bg="sky blue")
        self.seis.place(relwidth = 1, relheight = 1)

        R1 = Radiobutton(self.seis, text="Camara interna",font = 'Fixedsys',
        bg="sky blue",
        activebackground ="sky blue",
        variable=self.camaraCambio,
        value=0)
        R1.grid( padx = 200,row = 0,column = 0,pady = 50)

        R2 = Radiobutton(self.seis, text="Camara externa",font = 'Fixedsys',
        bg="sky blue",
        activebackground ="sky blue",
        variable=self.camaraCambio,
        value=1)
        R2.grid(row = 1,column = 0)

    #def cambiarValor(self):
        #print(self.camaraCambio.get())

    def botones(self):
        if self.captura != None:

            self.captura.release()
            self.prueba.destroy()
        #self.etiqueta.destroy()
        self.ven.protocol('WM_DELETE_WINDOW',lambda: self.ven.destroy())
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
        im = self.img_dir+"\imagen1.png"

        self.imagen= PhotoImage(file = im)
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
        tkinter.messagebox.showinfo("Mensaje:","??No existe ningun Usuario!")
        ).place(
        x = 5,
        y = 45)

        btn3_mostrarMultiple = Button(self.frameMenu, text="Reconocimiento \nMultiple",bg= "yellow",font = 'Fixedsys',
        command = lambda:self.reconocerMultiple() if os.path.exists(direccion) else
        tkinter.messagebox.showinfo("Mensaje:","??No existe ningun Usuario!")).place(
        x = 5,
        y = 80,
        )

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
        self.controlSalir()
        self.ven.geometry('650x540')
        self.barraMenu.destroy()
        self.variable = None
        Video = pb.DataBase(nombre,mascarilla,self.camaraCambio.get())
        self.objeto = Video
        self.botonPrueba()
    # elemetos de la interfaz
    def listaOpciones(self):


        self.barraMenu = Menu(self.ven)
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
        scrollbar.grid(row=3,
        column=2,
        sticky='NS')
        self.listbox = Listbox(frame, yscrollcommand=scrollbar.set,font = 'Fixedsys')
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
                    tkinter.messagebox.showinfo("Mensaje:","??No se puede agregar mas usuarios!")

    def barraProgreso(self,frame,maximum,x,y,pos):
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
        #self.textobar.grid(column = x, row = y )
        if pos:
            self.mpb.grid(column = x, row =y+1 )
            self.textobar.grid(column = x, row = y )
        else:
            self.mpb.place(x = x, y = y )
            self.textobar.place(x = x+20, y = y-22 )

        self.mpb["maximum"] = maximum
        self.mpb["value"]  = 0

    #funciones para guardar nombres
    def asignarNombre(self):
        self.ven.geometry('300x300')
        self.frameMenu.destroy()
        con = '_sin_mascarilla'
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
        self.btn1_mostrar = Button(self.primer,bg = 'yellow' ,activebackground ="yellow",text="Guardar",font = 'Fixedsys',
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


        #print(nombre)
        etiquetas = os.listdir(direccion)
        if valor:
            if nombre in etiquetas:
                tkinter.messagebox.showinfo("Mensaje:","??El usuario ya existe!")
                return True
            elif nombre == '':
                tkinter.messagebox.showinfo("Mensaje:","??Primero ingresa un nombre!")
                return True
            else:
                return False
        else:
            if nombre in etiquetas:
                return False
            else:
                tkinter.messagebox.showinfo("Mensaje:","??No existe el Usuario!")

    def UsuarioMascarilla(self,nombre):
        #self.primer.destroy()
        con = '_con_mascarilla'
        self.ven.geometry('500x300')
        self.segundo = Frame(self.ven,bg="sky blue")
        self.segundo.place(relwidth=1, relheight=1)

        btn_tomarMas = Button(self.segundo, text="tomar fotos",bg = 'yellow',font = 'Fixedsys',
        command = lambda:self.agregar(nombre, con))
        btn_tomarMas.grid(
        row=1,
        column=1,
        padx=5,
        pady=5)

        txt = Label(self.segundo,bg="sky blue", text= 'Coloquese la mascarilla y cuando este listo presione el boton',
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
        self.n = True
        #self.list = ''
        self.scrolbar(self.tercer)
        #self.listbox.bind('<<ListboxSelect>>', self.seleccionar)
        #textExample.insert(0, "Default Text")
        self.nombre1 = Entry(self.tercer,font = 'Fixedsys')
        self.nombre1.grid(
        row=1,
        column=3,

        pady=25)
        #result = self.nombre.get()

        btn1_mostrar = Button(self.tercer, text=" Reconocer",bg = 'yellow',font = 'Fixedsys',activebackground ="yellow",
        command = lambda:self.reconocerxfat32(pb3.Reconocer(self.nombre1.get(),self.camaraCambio.get())) if
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
        pady=5)# scrolbar

    def reconocerxfat32(self,clase):#self.variable  = True
        self.barraMenu.destroy()
        self.variable = True
        #recon = pb3.Reconocer(nombre)
        self.objeto = clase
        self.ven.geometry('720x500')
        self.botonPrueba()

    # (muestra el Frame de la camera) = funcion(show_vid)
    def botonPrueba(self):
        self.cero.destroy()#cambio aquii
        self.prueba = Frame(self.ven,bg="sky blue")
        self.prueba.place(relwidth=1, relheight=1)
        self.lmain = Label(master=self.prueba)
        self.lmain.grid(column=0, rowspan=4, padx=5, pady=5)

        #self.lmain.pack()
        if self.variable:
            self.btnsalir = Button(self.prueba,text = 'salir',bg= "yellow",font = 'Fixedsys', command = lambda:self.botones())
            self.btnsalir.grid(
            row=1,
            column=2,
            padx=10,
            pady=10)
        self.barraProgreso(self.prueba,250,0,8,True)
        self.show_vid()
        #self.barraProgreso()




        #self.UsuarioMascarilla('sdsdsdsd')
    # guardar Modelos
    def guardarModelos(self): # self.var = None
        self.controlSalir()
        self.btn_4.destroy()
        self.prueba.destroy()
        self.txt.grid_forget()
        self.btn1_mostrar.destroy()
        self.nombre.grid_forget()
        self.ven.geometry('300x300')
        modelo = pM.modelo(self.nombre.get())
        self.barraProgreso(self.prueba2,7,0,1,True)
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
                #print("Modelo creado")
                #tkinter.messagebox.showinfo("Mensaje:", "Modelo creado")
            else:
                time.sleep(0.3)
        self.botones()
        self.var = None
    # Activar frame dentro de la ventana
    def reconocerMultiple(self):
        self.cero.destroy()
        self.frameMenu.destroy()
        self.ven.geometry('380x320')
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
        self.barraProgreso(self.quinto,len(lista),70,70,False)

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
        self.reconocerxfat32(ReconocerMultiple(info,lisdire,lista,self.camaraCambio.get()))

    def show_vid(self):
        #cap = cv2.VideoCapture(0)
        #frame = op.oooo()
        #self.lista.append(con)
        if self.variable != True:
            frame,con,cap = self.objeto.VideoCaptura()
            if cap  != False:
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
                        padx = 120,
                        pady = 70)
                    self.var = False


                        #print(len(self.lista))
            else:
                self.mpb.destroy()

                c = tkinter.messagebox.showerror("Error", "Camara no habilitada")
                if c == 'ok':
                    self.botones()





        else:
            self.mpb.destroy()
            self.textobar.destroy()
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




                #del frame,cap
                #self.captura.release()
                #self.prueba.destroy()
            #print(self.captura, cap.isOpened())
            #if cap.isOpened() == False :
                #print('a ocurrido un  errorwwwwwwwwwwwwwwwww')
                #self.captura.release()
                #self.prueba.destroy()








































Ventana = Ventana(Tk())

import tkinter as tk
from tkinter import Tk, PhotoImage, Label
from tkinter import filedialog
import sys #Para finalizar el programa llamando a la función exit
from tkinter import filedialog  as fd #Ventanas de dialogo
from tkinter import messagebox as mb
from tkinter import *
from PIL import Image, ImageTk, ImageFilter, ImageOps
import numpy as np
class Aplication:
    def __init__(self):
        self.ventana1 = tk.Tk()
        self.ventana1.config(bg="#A8A8D3")
        self.ventana1.title("Proyecto segmentación de TRIPS")
        self.ventana1.geometry("800x500")
        self.menu()
        
        # Configura la imagen de fondo
        self.background_image = PhotoImage(file="fondo3.gif")
        self.background_label = Label(self.ventana1, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        #BIENVENIDA
        Label(text = "BIENVENIDO A SEGMI-TRIPS", fg="black", font = ("Verdana", 18), bg="#8DC06D").place(x=195, y=0)
        
        # Crear un label que pueda cambiar de posición en donde se le pueda poner una imagen
        self.image_label = Label(self.ventana1, bg="white")
        self.image_label.place(x=250, y=100)

        #B O T O N E S
        self.botones()

        self.ventana1.mainloop()

    def menu(self):
        menubar1 = tk.Menu(self.ventana1)
        self.ventana1.config(menu=menubar1)
        opc1 = tk.Menu(menubar1, tearoff=0)
        opc1.add_command(label="Salir", command=self.salir)
        opc1.add_command(label="Guardar Imagen", command=self.guardar)
        opc1.add_command(label="Seleccionar Imagen", command=self.seleccionar)
        menubar1.add_cascade(label="File", menu=opc1) 

    def salir(self):
        sys.exit(0)

    def guardar(self):
        nomArchivo = fd.asksaveasfilename(initialdir= "C:/Users/USER/OneDrive/Escritorio/AImages", title= "Guardar como", defaultextension=".png")
        if nomArchivo!='':
            self.image.save(nomArchivo)
            mb.showinfo("Información", "La imagen ha sido guardada correctamente.")

    def seleccionar(self):
        nomArchivo = fd.askopenfilename(initialdir= "C:/Users/USER/OneDrive/Escritorio/AImages", title= "Seleccionar Archivo", filetypes= (("Image files", "*.png; *.jpg; *.gif"),("todos los archivos", "*.*")))
        if nomArchivo!='':
            self.image = Image.open(nomArchivo)
            self.image = self.image.resize((270, 250))#Normalizamos la imagen
            self.photo = ImageTk.PhotoImage(self.image)
            self.image_label.configure(image=self.photo)
        
            # Habilitar botones
            self.gray_button.configure(state="normal")
            self.exp_button.configure(state="normal")
            self.max_button.configure(state="normal")
            self.kirsch_button.configure(state="normal")


    def botones(self):
        self.gray_button = Button(self.ventana1, text="Escala de grises", width=2, height=2, bg="#E5DBF7", fg="black",font=("Helvetica", 10, "bold"), command=self.gray_scale, state="disabled")
        self.gray_button.place(x= 110, y= 380, width=120)

        self.exp_button = Button(self.ventana1, text="Ecualización Expo", width=2, height=2, bg="#E5DBF7", fg="black",font=("Helvetica", 10, "bold"), command=self.hist_contrast, state="disabled")
        self.exp_button.place(x= 250, y= 380, width=120)

        self.max_button = Button(self.ventana1, text="Filtro Max", width=2, height=2, bg="#E5DBF7", fg="black",font=("Helvetica", 10, "bold"), command=self.max_filter, state="disabled")
        self.max_button.place(x= 390, y= 380, width=120)

        self.kirsch_button = Button(self.ventana1, text="Kirsch", width=2, height=2, bg="#E5DBF7", fg="black",font=("Helvetica", 10, "bold"), command=self.kirsch_operator, state="disabled")
        self.kirsch_button.place(x= 550, y= 380, width=120)

    def gray_scale(self):
        # Convertir imagen a escala de grises y actualizar etiqueta
        self.image = self.image.convert("L")
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.photo)

    def hist_contrast(self): #Se ecualiza
        # Mejora de contraste por histograma y actualizar etiqueta
        self.image = ImageOps.equalize(self.image)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.photo) 

    def max_filter(self):
        # Filtro máximo y actualizar etiqueta
        self.image = self.image.filter(ImageFilter.MaxFilter(3))
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.photo)

    def kirsch_operator(self):
        # Operador de compás de Kirsch y actualizar etiqueta
        #kirsch_kernel = ImageFilter.Kernel((3, 3), [-3, -3, 5, -3, 0, 5, -3, -3, 5])
        #self.image = self.image.filter(kirsch_kernel)
        #self.photo = ImageTk.PhotoImage(self.image)
        #self.image_label.configure(image=self.photo)  

        self.image = self.image.convert("L")
        #Convertir la imagen a un arreglo de numpy
        self.image_array = np.array(self.image)

        #Crear las máscaras de kirsch
        self.masks =[    np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]], dtype=float),
            np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]], dtype=float),
            np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]], dtype=float),
            np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]], dtype=float),
            np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]], dtype=float),
            np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]], dtype=float),
            np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]], dtype=float),
            np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]], dtype=float)
        ]

        #Crear las matrices las matrices resultado para cada grado de Kirsch
        self.results= []
        for i in range(8):
            self.results.append(np.zeros_like(self.image_array))

        #Aplicar el operador de Kirsch para cada grado

        for i in range(8):
            mask = self.masks[i]
            for r in range(1, self.image_array.shape[0]-1):
                for c in range(1, self.image_array.shape[1]-1):
                    sub_image = self.image_array[r-1:r+2, c-1:c+2]
                    result = np.sum(sub_image * mask)
                    self.results[i][r, c] = np.sqrt(result ** 2)
        
        #Unir las matrices resultado para obtener la imagen final
        self.final_image_array = np.max(self.results, axis=0)
        #self.final_image = self.image.fromarray(self.final_image_array.astype(np.uint8))
        self.final_image = Image.fromarray(self.final_image_array.astype(np.uint8))

        #Mostrar las imagenes resultantes
        self.final_image.show()
        for i in range(8):
            result_image = Image.fromarray(self.results[i].astype(np.uint8))
            result_image.show()
         

aplication = Aplication()
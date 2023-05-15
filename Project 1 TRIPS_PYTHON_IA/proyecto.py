import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageOps

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Proyecto segmentación de TRIPS")
        self.master.geometry("500x800")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Cargar el fondo
        self.background_image = ImageTk.PhotoImage(Image.open("fondo3.gif"))
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.lower()

        # Botones para abrir, cerrar y guardar una imagen
        self.open_button = tk.Button(self, text="Abrir", command=self.open_image)
        self.open_button.place(x=100, y=100, width=50, height=30)
        #self.open_button.pack(side="left")

        self.save_button = tk.Button(self, text="Guardar", command=self.save_image)
        self.save_button.place(x=200, y=200, width=90)
        #self.save_button.pack(side="left")

        self.close_button = tk.Button(self, text="Cerrar", command=self.close_image, state="disabled")
        self.close_button.place(x=30, y=30, width=50, height=30)
        #self.close_button.pack(side="left")

        # Botones para las diferentes operaciones
        self.gray_button = tk.Button(self, text="Escala de grises", command=self.gray_scale, state="disabled")
        self.gray_button.place(x=10, y=80, width=50, height=30)
        #self.gray_button.pack(side="left")

        self.rgb_button = tk.Button(self, text="Canales RGB", command=self.rgb_channels, state="disabled")
        self.gray_button.place(x=20, y=70, width=50, height=30)
        #self.rgb_button.pack(side="left")

        self.hist_button = tk.Button(self, text="Contraste por histograma", command=self.hist_contrast, state="disabled")
        self.gray_button.place(x=30, y=60, width=50, height=30)
        #self.hist_button.pack(side="left")

        self.exp_button = tk.Button(self, text="Ecualizacion exponencial", command=self.exp_equalization, state="disabled")
        self.gray_button.place(x=40, y=50, width=50, height=30)
        #self.exp_button.pack(side="left")

        self.max_button = tk.Button(self, text="Filtro maximo", command=self.max_filter, state="disabled")
        self.gray_button.place(x=50, y=40, width=50, height=30)
        #self.max_button.pack(side="left")

        self.kirsch_button = tk.Button(self, text="Operador de compas de Kirsch", command=self.kirsch_operator, state="disabled")
        self.gray_button.place(x=60, y=30, width=50, height=30)
        #self.kirsch_button.pack(side="left")

        # Etiqueta para mostrar la imagen
        self.image_label = tk.Label(self)
        self.image_label.pack()

    def open_image(self):
        # Abrir imagen y actualizar la etiqueta
        self.filepath = filedialog.askopenfilename()
        self.image = Image.open(self.filepath)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.photo)

        # Habilitar botones
        self.gray_button.configure(state="normal")
        self.rgb_button.configure(state="normal")
        self.hist_button.configure(state="normal")
        self.exp_button.configure(state="normal")
        self.max_button.configure(state="normal")
        self.kirsch_button.configure(state="normal")
        self.close_button.configure(state="normal")

    def save_image(self):
        # Guardar imagen
        save_filepath = filedialog.asksaveasfilename(defaultextension=".png")
        self.image.save(save_filepath)

    def close_image(self):
        # Cerrar imagen y actualizar la etiqueta
        self.image = None
        self.photo = None
        self.image_label.configure(image=self.photo)

        # Deshabilitar botones
        self.gray_button.configure(state="disabled")
        self.rgb_button.configure(state="disabled")
        self.hist_button.configure(state="disabled")
        self.exp_button.configure(state="disabled")
        self.max_button.configure(state="disabled")
        self.kirsch_button.configure(state="disabled")
        self.close_button.configure(state="disabled")

    def gray_scale(self):
        # Convertir imagen a escala de grises y actualizar etiqueta
        self.image = self.image.convert("L")
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.photo)

    def rgb_channels(self):
        # Dividir imagen en canales RGB y mostrarlos en una nueva ventana
        r, g, b = self.image.split()
        r.show()
        g.show()
        b.show()

    def hist_contrast(self):
        # Mejora de contraste por histograma y actualizar etiqueta
        self.image = ImageOps.equalize(self.image)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.photo)

    def exp_equalization(self):
        # Ecualizacion exponencial y actualizar etiqueta
        self.image = ImageOps.equalize(self.image, mask=None, exp=0.5)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.photo)

    def max_filter(self):
        # Filtro máximo y actualizar etiqueta
        self.image = self.image.filter(ImageFilter.MaxFilter(3))
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.photo)

    def kirsch_operator(self):
        # Operador de compás de Kirsch y actualizar etiqueta
        kirsch_kernel = ImageFilter.Kernel((3, 3), [-3, -3, 5, -3, 0, 5, -3, -3, 5])
        self.image = self.image.filter(kirsch_kernel)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.configure(image=self.photo)


root = tk.Tk()
app = Application(master=root)
app.mainloop()


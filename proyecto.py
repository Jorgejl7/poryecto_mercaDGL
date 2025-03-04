import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import pandas as pd
import datetime
from pyzbar.pyzbar import decode

def cargar_imagen(entry_codigo, lbl_imagen_destino, entry_nombre):
    file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    mostrar_imagen(file_path, entry_codigo, lbl_imagen_destino, entry_nombre)

def capturar_imagen(entry_codigo, lbl_imagen_destino, entry_nombre):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "No se pudo abrir la cámara.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        barcode = decode(frame)
        for b in barcode:
            codigo_barras = b.data.decode("utf-8")
            cap.release()
            cv2.destroyAllWindows()
            entry_codigo.delete(0, tk.END)
            entry_codigo.insert(0, codigo_barras)
            file_path = "captura.jpg"
            cv2.imwrite(file_path, frame)
            mostrar_imagen(file_path, entry_codigo, lbl_imagen_destino, entry_nombre)
            return
        
        cv2.imshow("Escanea el código de barras", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def mostrar_imagen(file_path, entry_codigo, lbl_imagen_destino, entry_nombre):
    img = Image.open(file_path)
    img = img.resize((250, 150))
    img_tk = ImageTk.PhotoImage(img)
    lbl_imagen_destino.config(image=img_tk)
    lbl_imagen_destino.image = img_tk
    
    img_cv = cv2.imread(file_path)
    img_cv = cv2.resize(img_cv, (400, 300))
    barcode = decode(img_cv)
    if barcode:
        codigo = barcode[0].data.decode("utf-8")
        entry_codigo.delete(0, tk.END)
        entry_codigo.insert(0, codigo)
        entry_nombre.focus()

def guardar_datos(lista, entrys, lbl_imagen):
    try:
        nombre = entrys[0].get()
        cantidad = int(entrys[1].get())
        precio = float(entrys[2].get())
        codigo = entrys[3].get()
    except ValueError:
        messagebox.showwarning("Advertencia", "Cantidad debe ser entero y precio un número válido.")
        return

    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not (nombre and cantidad and precio and codigo):
        messagebox.showwarning("Advertencia", "Completa todos los campos.")
        return

    lista.append([nombre, cantidad, f"Q{precio}", fecha, codigo])
    messagebox.showinfo("Éxito", "Registro guardado correctamente.")
    for e in entrys:
        e.delete(0, tk.END)
    lbl_imagen.config(image="")
    entrys[0].focus()

def exportar_excel(lista):
    if not lista:
        messagebox.showwarning("Advertencia", "No hay datos para exportar.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
    if not file_path:
        return

    df = pd.DataFrame(lista, columns=["Nombre", "Cantidad", "Precio", "Fecha", "Código de Barras"])
    df.to_excel(file_path, index=False)
    messagebox.showinfo("Éxito", f"Datos exportados a {file_path}")

def on_codigo_ingresado(event, entry_codigo, entry_nombre):
    codigo = entry_codigo.get().strip()
    if codigo:
        entry_nombre.focus()

def crear_interfaz_registro(titulo, lista):
    ventana = tk.Toplevel(root)
    ventana.title(titulo)
    ventana.geometry("400x500")
    ventana.configure(bg="#e6f7ff")
    
    frame = tk.Frame(ventana, bg="#e6f7ff")
    frame.pack(expand=True)
    
    entrys = []
    etiquetas = ["Nombre Producto:", "Cantidad:", "Precio (Q):", "Código de Barras:"]
    for i, text in enumerate(etiquetas):
        tk.Label(frame, text=text, bg="#e6f7ff").grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(frame)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entrys.append(entry)
    
    entrys[3].bind("<Return>", lambda event: on_codigo_ingresado(event, entrys[3], entrys[0]))
    
    lbl_imagen = tk.Label(frame, bg="#e6f7ff")
    lbl_imagen.grid(row=5, column=0, columnspan=2, pady=10)
    
    tk.Button(frame, text="Seleccionar Imagen", command=lambda: cargar_imagen(entrys[3], lbl_imagen, entrys[0])).grid(row=6, column=0, padx=5, pady=10)
    tk.Button(frame, text="Capturar desde Cámara", command=lambda: capturar_imagen(entrys[3], lbl_imagen, entrys[0])).grid(row=6, column=1, padx=5, pady=10)
    tk.Button(frame, text="Guardar", command=lambda: guardar_datos(lista, entrys, lbl_imagen)).grid(row=7, column=0, padx=5, pady=10)
    tk.Button(frame, text="Exportar a Excel", command=lambda: exportar_excel(lista)).grid(row=7, column=1, padx=5, pady=10)
    tk.Button(frame, text="Cerrar", command=ventana.destroy).grid(row=8, column=0, columnspan=2, pady=10)

def abrir_registro_productos():
    crear_interfaz_registro("Registro de Productos MercaDGL", productos)

def abrir_registro_ventas():
    crear_interfaz_registro("Registro de Ventas MercaDGL", ventas)

root = tk.Tk()
root.title("MercaDGL")
root.geometry("400x500")
root.configure(bg="#e6f7ff")

productos = []
ventas = []

frame_main = tk.Frame(root, bg="#e6f7ff")
frame_main.pack(expand=True)

tk.Button(frame_main, text="Registro de Productos", command=abrir_registro_productos).pack(pady=10)
tk.Button(frame_main, text="Registro de Ventas", command=abrir_registro_ventas).pack(pady=10)

root.mainloop()

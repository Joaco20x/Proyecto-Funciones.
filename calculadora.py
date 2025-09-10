import tkinter as tk
from tkinter import messagebox
import sympy as sp
import matplotlib.pyplot as plt

def analizis():
    texto=entrada.get()
    x=entrada2.get()
    try:
        valor=texto.count("x")
        if valor==0:
            raise SyntaxError
        if " " in x:
            raise ValueError
        solox()
        funcion= sp.sympify(texto)
    except ValueError:
        messagebox.showerror("Error", "El x a evaluar no puede contener espacios")
    except SyntaxError:
        messagebox.showerror("Error","Funcion debe contener solo como incognita x")
    except sp.SympifyError:
        messagebox.showerror("Error", "Función no válida")
    print(texto,x)

def graficar():
    texto = entrada.get()
    try:
        x_pri = sp.Symbol("x")
        funcion = sp.sympify(texto)
        x = [i/10 for i in range(0,100)]        # genera un rango en el grafico eje x
        f = sp.lambdify(x_pri, funcion)         # toma la forma simbolica y la convierte en una funcion
        y = [f(val) for val in x]               # rango del grafico en el eje y

        plt.plot(x, y)                  # coordenadas x e y
        plt.title(f"f(x) = {texto}")    # muestra el titulo del grafico
        plt.xlabel("x")                 # muestra titulo eje x 
        plt.ylabel("f(x)")              # titulo en eje y
        plt.grid(True)                  # activa las rejillas del grafico 
        plt.show()                      # muestra el grafico
    except Exception:
        messagebox.showerror("Error", f"No se pudo graficar la función")


def solox():
    global texto
    texto=entrada.get()
    cadena=""
    apropiado="x"
    for l in texto:
        if l.isalpha():
            cadena+=l
            if cadena=="sin" or cadena=="cos" or cadena=="tan":
                cadena=""
    for c in cadena:
        if c!=apropiado:
            raise SyntaxError
root=tk.Tk()
root.title("Analizador de funciones")
text=tk.StringVar()
root.geometry("350x350")
text.set("Ingrese aqui su funcion")
tk.Label(root,textvariable=text, font=("Arial",16)).pack()

entrada= tk.Entry(root)
entrada.pack()

text2=tk.StringVar()
text2.set("x a evualar (opcional)")
tk.Label(root,textvariable=text2, font=("Arial",16)).pack()
entrada2= tk.Entry(root)
entrada2.pack()

tk.Button(root,text="Analizar funcion", width=13,height=1,command=analizis).pack()
tk.Button(root,text="Graficar funcion", width=13,height=1,command=graficar).pack()



root.mainloop() #esto mantendra viva la venta hasta cerrarla

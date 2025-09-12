#-------------------Librerias----------------------------------
import tkinter as tk
from tkinter import messagebox
import math 
import sympy as sp
import matplotlib.pyplot as plt

#--------------------Analizis-----------------------------------
def analizis():
    texto=entrada.get()
    x=entrada2.get()
    print(len(x))
    try:
        valor=texto.count("x")
        if valor==0:
            raise SyntaxError
        if len(x) !=0:
            print("dentro")
            if " " in x:
                print("dentro deentro")
                raise ValueError

        solox()
        dominio()
        recorrido()
        funcion= sp.sympify(texto)
    except ValueError:
        messagebox.showerror("Error", "El x a evaluar no puede contener espacios")
    except SyntaxError:
        messagebox.showerror("Error","Funcion debe contener solo como incognita x")
    except sp.SympifyError:
        messagebox.showerror("Error", "Función no válida")
    print(texto,x)

#---------------------------Dominio--------------------------------
def dominio():
    dominio_final=sp.S.Reals #Empezando diciendo que el dominio final seran todos los reales
    texto=entrada.get()
    x=sp.Symbol("x")
    cadena=""
    division=texto.find("/")
    #Para verificar denominador
    if division!=-1:
        l=texto.index("/")+1
        denom=texto[l:]
        denominador=sp.sympify(denom)
        valores_prohibidos = sp.solveset(denominador, x, sp.S.Reals) #Nos da todos los valores que hagan que el denominador sea cero
        dominio_final= dominio_final - valores_prohibidos #Les restamos los valores prohibidos del denominador
    #Para verificar raiz cuadrada
    if texto.find("sqrt(")!=-1:    
        radicandos = []       # Lista donde guardaremos todas las raíces
        ra = ""
        capturando = False
        i = 0
        dominio_raizes=[]
        while i < len(texto):
            # Detectar inicio de sqrt
            if texto[i:i+5] == "sqrt(":
                capturando = True
                i += 5  #Se salta sqrt( para capturar el radicando
                ra = ""
                continue
            #Empezamos a capturar el radicando
            if capturando:
                if texto[i] == ")": #Verificamos si termino el radicando
                    capturando = False
                    radicandos.append(ra)   # Guardamos el radicando
                else:
                    ra += texto[i]          # Acumulamos caracteres dentro de la raíz
            i += 1
        for r in radicandos:
            radi= sp.sympify(r)
            dominio_raiz=sp.solveset(radi>=0,x,sp.S.Reals)
            dominio_raizes.append(dominio_raiz)
        if len(dominio_raizes)> 1:
            dominio_final_raiz=dominio_raizes[0]
            for d in dominio_raizes[1:]:
                dominio_final=dominio_final.intersect(d)
        else:
            dominio_final=dominio_final.intersect(dominio_raiz)
    
    print("Dominio de la funcion: ", dominio_final)
    messagebox.showinfo("Dominio", f"Dominio de la función: {dominio_final}")
    return dominio_final

#-------------------------Recorrido---------------------------
def recorrido():
    return

#-----------------------------Grafica-----------------------------------
def graficar():
    texto = entrada.get()
    try:
        x_pri = sp.Symbol("x")         
        funcion = sp.sympify(texto)
        print(f"f(x) = {funcion}")
        valor=entrada2.get()
        
        if valor != "":
            num=float(valor) #Convertimos el valor ingresado por el usuario a un flotante
            funcion_sustituida=funcion.subs(x_pri,num) #Se sustituyen todos los x por el numero ingresado por el usuario
            print(f"Sustituimos x por: {num}")
            resultado=sp.N(funcion_sustituida) #Se calcula el resultado
            print(f"Resultado de la funcion: {resultado}")
        
        f = sp.lambdify(x_pri, funcion)         # toma la forma simbolica y la convierte en una funcion
        x = [i/10 for i in range(0,100)]        # genera un rango en el grafico eje x
        y = [f(val) for val in x]               # rango del grafico en el eje y
        
        plt.plot(x, y) 
        plt.scatter(num, resultado, color="red", label=f"Punto ({num}, {resultado})") #Graficamos el punto  y desimos su ubicacion
        plt.title(f"f(x) = {texto}")    # muestra el titulo del grafico
        plt.xlabel("x")                 # muestra titulo eje x 
        plt.ylabel("f(x)")              # titulo en eje y
        plt.grid(True)                  # activa las rejillas del grafico 
        plt.legend()
        plt.show()    
    except Exception:
        messagebox.showerror("Error", f"No se pudo graficar la función")

#---------------------------Solox---------------------------------------
def solox():
    global texto
    texto=entrada.get()
    cadena=""
    apropiado="x"
    for l in texto:
        if l.isalpha():
            cadena+=l
            if cadena=="sin" or cadena=="cos" or cadena=="tan" or cadena=="sqrt":
                cadena=""
    for c in cadena:
        if c!=apropiado:
            raise SyntaxError

#--------------------Variables--------------------------------------------------
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

#---------------------Librerias---------------------------------
import tkinter as tk
from tkinter import messagebox
import sympy as sp
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#---------------------Intersecciones-----------------------------
def interseccion():
    try:
        texto = entrada.get()
        x = sp.Symbol("x")
        funcion = sp.sympify(texto)

        # --- interseccion con eje Y ---
        try:
            inter_y = funcion.subs(x, 0)
            if inter_y.is_real:
                punto_y = (0, inter_y)
            else:          
                punto_y = None
        except:
            punto_y = None

        # --- intersecciones con eje X ---
        inter_x = sp.solveset(funcion, x, sp.S.Reals)

        # resultados
        mensaje = ""
        if punto_y:
            mensaje += f"Interseccion con Y: {punto_y}\n"
        else:
            mensaje += "No hay interseccion con Y\n"
            inter_y= "No hay intersecciones con Y"

        if inter_x:
            mensaje += f"Intersecciones con X: {list(inter_x)}"
        else:
            mensaje += "No hay intersecciones con X"
            inter_x= "No hay intersecciones con X"
        print(mensaje)

        return inter_x, punto_y
    except Exception as e:
        messagebox.showerror("Error", f"No se pueden calcular las intersecciones.\nDetalles: {e}")

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
        dominios=dominio()
        recorridos= recorrido()
        inter_x,inter_y= interseccion()
        texto_resultados.insert("end", f"Dominio: {dominios}\n")
        texto_resultados.insert("end", f"Recorrido: {recorridos}\n")
        texto_resultados.insert("end", f"Intersecciones X: {inter_x}, Y: {inter_y}\n")
        texto_resultados.insert("end","-----------------------------------------------------------------------------------------")
        funcion= sp.sympify(texto)

    except ValueError:
        messagebox.showerror("Error", "El x a evaluar no puede contener espacios")
    except SyntaxError:
        messagebox.showerror("Error","Funcion debe contener solo como incognita x")
    except sp.SympifyError:
        messagebox.showerror("Error", "Funcion no válida")
    print(texto,x)

#---------------------------Dominio--------------------------------
def dominio():
    dominio_final=sp.S.Reals 
    texto=entrada.get()
    x=sp.Symbol("x")
    cadena=""
    division=texto.find("/")
    
    #verifica denominador
    if division!=-1:
        l=texto.index("/")+1
        denom=texto[l:]
        denominador=sp.sympify(denom)
        valores_prohibidos = sp.solveset(denominador, x, sp.S.Reals) #todos los valores que hagan que el denominador sea cero
        dominio_final= dominio_final - valores_prohibidos #resta los valores prohibidos del denominador
    
    #verifica raiz cuadrada
    if texto.find("sqrt(")!=-1:    
        radicandos = [] #Lista de todas las raices
        ra = ""
        capturando = False
        i = 0
        dominio_raizes=[]
        while i < len(texto):
            
            # Detectar inicio de sqrt
            if texto[i:i+5] == "sqrt(":
                capturando = True
                i += 5  #Se salta sqrt
                ra = ""
                continue
            
            #capturar el radicando
            if capturando:
                if texto[i] == ")": #termino el radicando
                    capturando = False
                    radicandos.append(ra)#se guarda 
                else:
                    ra += texto[i]#cumula caracteres dentro de la raiz
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
    return dominio_final

#-------------------------Recorrido---------------------------
def recorrido():
    try:
        texto = entrada.get()
        x = sp.Symbol("x")
        funcion = sp.sympify(texto)

        #el dominio 
        dominio_final = dominio()  

        #rango recorrido con sympy
        rango = sp.calculus.util.function_range(funcion, x, dominio_final)

        print("Recorrido de la función:", rango)

        return rango
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo calcular el recorrido.\nDetalles: {e}")

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
        x = [i/10 for i in range(-100,101)]        # genera un rango en el grafico eje x
        y = [f(val) for val in x]               # rango del grafico en el eje y
    
       
        ax.plot(x, y, label=f"f(x) = {texto}")
        ax.scatter(num, resultado, color="red", label=f"Punto ({num}, {resultado})") #Graficamos el punto  y desimos su ubicacion
        ax.set_title(f"f(x) = {texto}")    # muestra el titulo del grafico
        ax.set_xlabel("x")                 # muestra titulo eje x 
        ax.set_ylabel("f(x)")              # titulo en eje y
        ax.grid(True)                  # activa las rejillas del grafico 
        ax.legend()
            

        canvas.draw()
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

#----------------------------------Desarrollo---------------------------------------------------
def paso_a_paso():
    texto = entrada.get().strip()
    valor_str = entrada2.get().strip()

    if texto == "":
        messagebox.showerror("Error", "No hay funcion.")
        return

    if valor_str == "":
        messagebox.showinfo("Info", "No has ingresado un valor.")
        return

    x = sp.Symbol("x")
    try:
        # parsear la funcion simbolica
        funcion = sp.sympify(texto)
        valor = sp.sympify(valor_str)

        pasos = []
        pasos.append(f"f(x) = {funcion}")
        pasos.append(f"f({valor}) = {funcion.subs(x, valor)}")

        # evaluacion numerica paso a paso
        current = funcion.subs(x, valor)
        current = sp.N(current)
        pasos.append(f"f({valor}) = {current}")

        texto_mostrar = "\n".join(pasos)
        texto_mostrar += f"\n\nPar ordenado: ({valor}, {current})"
        texto_resultados.insert("end", f"Solucion paso a paso \n")
        texto_resultados.insert("end", f"{texto_mostrar}\n")
        texto_resultados.insert("end","-----------------------------------------------------------------------------------------")
    except sp.SympifyError:
        messagebox.showerror("Error", "Funcion no valida (no se pudo interpretar).")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo realizar el desarrollo paso a paso.\nDetalles: {e}")

root = tk.Tk()
root.title("Analizador de funciones")
root.geometry("1280x720")
root.configure(bg="#1b3c42")

# ------------------- Entradas y botones -------------------
text = tk.StringVar(value="Ingrese aqui su funcion")
tk.Label(root, textvariable=text, font=("Arial", 16, "bold"),
         bg="#1b3c42", fg="white").pack(pady=5)

entrada = tk.Entry(root, width=40, font=("Arial", 14))
entrada.pack(pady=5)



text2 = tk.StringVar(value="x a evaluar (opcional)")
tk.Label(root, textvariable=text2, font=("Arial", 16, "bold"),
         bg="#1b3c42", fg="white").pack(pady=5)

entrada2 = tk.Entry(root, width=40, font=("Arial", 14))
entrada2.pack(pady=5)

tk.Button(root, text="Analizar funcion", width=20, height=1, command=analizis, font=("Arial", 10, "bold"), fg="white", bg="black").pack(pady=5)
tk.Button(root, text="Graficar funcion", width=20, height=1, command=graficar, font=("Arial", 10, "bold"), fg="white", bg="black").pack(pady=5)
tk.Button(root, text="Desarrollo paso a paso", width=20, height=1, command=paso_a_paso, font=("Arial", 10, "bold"), fg="white", bg="black").pack(pady=5)

# ------------------- Contenedor principal -------------------
# --------- Sección de cuadrados ---------
frame_contenedor = tk.Frame(root, bg="#1b3c42")
frame_contenedor.pack(pady=20, fill="both", expand=True)

# Cuadro del gráfico
cuadro_grafico = tk.Frame(frame_contenedor, width=600, height=400, bg="white")
cuadro_grafico.pack(side="left", padx=20, pady=20)


fig, ax = plt.subplots(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=cuadro_grafico)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Cuadro de resultados con scrollbar
frame_resultados = tk.Frame(frame_contenedor, bg="white")
frame_resultados.pack(side="left", padx=20, pady=20, fill="both", expand=True)

# Text + Scrollbar
scrollbar = tk.Scrollbar(frame_resultados)
scrollbar.pack(side="right", fill="y")

cuadro_resultados = tk.Text(frame_resultados, wrap="word", yscrollcommand=scrollbar.set, font=("Arial", 12))
cuadro_resultados.pack(fill="both", expand=True)

scrollbar.config(command=cuadro_resultados.yview)

# Área de texto para mostrar dominio, recorrido e intersecciones
texto_resultados = tk.Text(cuadro_resultados, width=100, height=30, bg="black", fg="white", font=("Arial", 10))
texto_resultados.pack(expand=True, padx=10, pady=10)

# Insertar texto de ejemplo

root.mainloop()

#---------------------Librerias---------------------------------
import tkinter as tk
from tkinter import messagebox
import math 
import sympy as sp
import matplotlib.pyplot as plt
from sympy.parsing.sympy_parser import parse_expr

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

        if inter_x:
            mensaje += f"Intersecciones con X: {list(inter_x)}"
        else:
            mensaje += "No hay intersecciones con X"

        print(mensaje)
        messagebox.showinfo("Intersecciones", mensaje)

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
        dominio()
        recorrido()
        interseccion()
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
    messagebox.showinfo("Dominio", f"Dominio de la función: {dominio_final}")
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
        messagebox.showinfo("Recorrido", f"Recorrido de la función: {rango}")

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
        # parsear la funcion simbolica (valida la funcion)
        funcion = sp.sympify(texto)

        # Reemplaza 'x' por '(valor)' en la cadena original para que se muestre tal cual
        texto_sustituido = texto.replace("x", f"({valor_str})")

        # Parsea la expresion sustituida SIN evaluar (para conservar 2**2 en lugar de 4)
        expr = parse_expr(texto_sustituido, evaluate=False)

        # Coleccion de pasos
        pasos = []
        pasos.append(f"f(x) = {texto}")
        pasos.append(f"f({valor_str}) = {texto_sustituido}")

        # simplifica subexpresiones numericas una por una
        current = expr
        # encuentra subnodos numericos no resueltos
        while True:
            # seleccion de subexpresiones que NO tienen símbolos libres y que no son ya un numero
            numeric_nodes = [n for n in current.preorder_traversal()
                            if getattr(n, "free_symbols", set()) == set() and not n.is_Number]

            if not numeric_nodes:
                break

            # subexpresion mas profunda 
            node = numeric_nodes[-1]
            # simplificar/valuar ese nodo
            try:
                node_val = sp.simplify(node)
                # si se lo convierte en numero, forzamos evaluacion numerica
                if not node_val.is_Number:
                    node_val = sp.N(node)
            except Exception:
                # evaluacion numerica
                node_val = sp.N(node)

            # Reemplaza la subexpresion por su valor
            current = current.xreplace({node: node_val})

            # Añade un paso mostrando la expresion resultante tras esa simplificacion
            pasos.append(f"f({valor_str}) = {str(current)}")

        # si la expresion no es numerica, evalua el resultado final numerico
        resultado_final = current
        if not resultado_final.is_Number:
            try:
                resultado_final = sp.N(resultado_final)
                pasos.append(f"f({valor_str}) = {str(resultado_final)}")
            except Exception:
                # si no se puede evaluar numericamente, lo dejamos como esta
                pass

        # Formatea la salida para mostrarla en un messagebox
        texto_mostrar = "\n".join(pasos)
        # si es un numero, mostramos el par ordenado final
        if getattr(resultado_final, "is_Number", False):
            texto_mostrar += f"\n\nPar ordenado: ({valor_str}, {resultado_final})"

        messagebox.showinfo("Desarrollo paso a paso", texto_mostrar)

    except sp.SympifyError:
        messagebox.showerror("Error", "Funcion no valida (no se pudo interpretar).")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo realizar el desarrollo paso a paso.\nDetalles: {e}")

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
text2.set("x a evaluar (opcional)")
tk.Label(root,textvariable=text2, font=("Arial",16)).pack()
entrada2= tk.Entry(root)
entrada2.pack()

tk.Button(root,text="Analizar funcion", width=13,height=1,command=analizis).pack()
tk.Button(root,text="Graficar funcion", width=13,height=1,command=graficar).pack()
tk.Button(root, text="Desarrollo paso a paso", width=20, height=1, command=paso_a_paso).pack()


root.mainloop() #esto mantendra viva la venta hasta cerrarla

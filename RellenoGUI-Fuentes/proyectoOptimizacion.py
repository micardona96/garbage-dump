##Minizinc
from cProfile import label
import json
from logging import exception, root
from math import inf
from turtle import title
from unittest import IsolatedAsyncioTestCase
from minizinc import Instance, Model, Solver, model
##Interfaz
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import * 
from tkinter import ttk  
from tkinter.filedialog import askopenfilename
from tkinter.font import Font

def validator(n):
    if n in ['1','2','3','4','5','6','7','8','9','0']:
        return True
    return False

def inicio(parentFrame):
    for widget in parentFrame.winfo_children():
        widget.destroy()

    frameMenu = tk.Frame(parentFrame, bg ='white')
    li1 = tk.Label(frameMenu, image= startPage, bg ='white')
    li2 = tk.Label(frameMenu, bg ='white', 
    fg="#1d2239", font = customFont, justify= LEFT,
    text="Bienvenido a Trashlocator, la app que le permitirá calcular " + '\n' + 
    "la ubicación más óptima de tu relleno sanitario."+ '\n' +
    "Puedes ingresar los datos manualmente o cargar un archivo .dzn " + '\n' +
    "que los contenga.")
    li1.pack(side=LEFT,fill=BOTH, anchor=CENTER)
    li2.pack(side=LEFT, fill=BOTH, anchor=CENTER)
    frameMenu.pack(anchor=CENTER, padx=20, pady=20, fill=X,side=TOP)

def ingresarDatos(parentFrame):
    entryE = []
    entryN = []
    for widget in parentFrame.winfo_children():
        widget.destroy()

    frameMenu = tk.Frame(parentFrame, bg ='white')
    frameInput = tk.Frame(frameMenu, bg ='white')

    vcmd = (frameMenu.register(validator), '%S')

    li1 = tk.Label(frameInput, bg ='white', fg="#1d2239", font = customFont, justify= LEFT, text="Ingrese el tamaño de la región")
    e1 = tk.Entry(frameInput,bg ='white', validate='key',vcmd=vcmd)
    li3 = tk.Label(frameInput, bg ='white', fg="#1d2239", font = customFont, justify= LEFT, text="Ingrese la cantidad de ciudades")
    e2 = tk.Entry(frameInput,bg ='white', validate='key',vcmd=vcmd)

    li1.pack(side=LEFT, padx=10)
    e1.pack(side=LEFT, padx=10)
    li3.pack(side=LEFT, padx=10)
    e2.pack(side=LEFT, padx=10)

    btn = ttk.Button(frameInput, text = 'Aceptar', style = 'TButton', command = lambda: ingresarUbicaciones(int(e2.get()),frameMenu,entryE, entryN, e1.get(), e2.get()))
    btn.pack(side=RIGHT)

    frameInput.pack(anchor=CENTER, padx=20, pady=20, fill=X,side=TOP)
    frameMenu.pack(anchor=CENTER, padx=20, pady=20, fill=X,side=TOP)

def ingresarUbicaciones(ciudades,pFrame,entryE,entryN, n, m):
    
    for i in range(ciudades):
        cityFrame = Frame(pFrame, bg='white')
        vcmd = (cityFrame.register(validator), '%S')
        lab = tk.Label(cityFrame, bg ='#1d2239', font = ('Sans Serif', 10), foreground = '#76BE49', text="Ciudad "+str(i+1))
        lab.pack(side=LEFT, padx=10)
        lab0 = tk.Label(cityFrame, bg ='white', fg="#1d2239", text="     Posición este:",font=customFont)
        lab0.pack(side=LEFT, padx=10)
        entryE.append(tk.Entry(cityFrame,bg ='white', fg="#1d2239", validate='key',vcmd=vcmd, font=customFont))
        entryE[i].pack(side=LEFT, padx=10)
        lab1 = tk.Label(cityFrame, bg ='white', fg="#1d2239", text="Posición norte:", font=customFont)
        lab1.pack(side=LEFT, padx=10)
        entryN.append(tk.Entry(cityFrame, bg ='white', fg="#1d2239", validate='key',vcmd=vcmd, font=customFont))
        entryN[i].pack(side=LEFT, padx=10)
        cityFrame.pack(side=TOP, pady=10)
    btnCalcular = ttk.Button(pFrame, text = 'Calcular', style = 'TButton', command = lambda: dznify(n, m, entryE, entryN))
    btnCalcular.pack(pady=10)

def dznify(n,m,entryE, entryN):
    citiesE = []
    citiesN = []
    f = open("../Datos/Datos.dzn","w+")
    f.write("n=" + n + ";\n")
    f.write("m=" + m + ";\n")
    f.write("ciudades=[")
    for e, i in zip(entryE,entryN):
        citiesE.append(int(e.get()))
        citiesN.append(int(i.get()))
        f.write("|"+ e.get() + "," + i.get() + "\n")
    f.write("|];") 
    f.close()  
    connectMinizinc("../Datos/Datos.dzn",False)

def cargarArchivo(parentFrame):
    for widget in parentFrame.winfo_children():
        widget.destroy()
    global fileName 
    fileName = ""
    Tk().withdraw() 
    fileName = askopenfilename()
    connectMinizinc(fileName, True)

def connectMinizinc(file, isLoaded):
    solver = Solver.lookup("gecode")
    # Create an Instance of the project model for solver
    instance = Instance(solver, Model("../Relleno.mzn"))
    # Assign the values from a dzn
    instance.add_file(file)
    result = instance.solve()
    texto = str(result)
    texto = texto.replace("'",'"')
    mijson = json.loads(texto)
    drawSolution(mijson['n'],mijson['m'],mijson['ciudades'],mijson['distancias'],mijson['pos_este'],mijson['pos_norte'], isLoaded)

def drawSolution(n,m,cities,distances,x,y, isLoaded):
    solutionFrame = Frame(frameMenu, bg='white')
    if isLoaded:
        frameMenu.pack_propagate(0)
    else:
        frameMenu.pack_propagate(1)

    solutionFrame.pack(expand=True,fill=X)
    cityX, cityY = splitArray(cities)
    fig, ax = plt.subplots()
    rect = patches.Rectangle((0, 0), n, n, linewidth=1, edgecolor='m', facecolor='none', label = 'Ecoreg')
    ax.add_patch(rect)
    plt.axis([-1, n+1, -1, n+1])
    plt.title("SOLUCIÓN")
    plt.xlabel("Ubicación en el este")
    plt.ylabel("Ubicación en el norte")
    plt.plot(x,y, 'ro', label ='Relleno sanitario')
    plt.plot(cityX, cityY, 'bo', label = 'Ciudades')
    plt.grid(color='c',linestyle='dotted')
    plt.legend(loc = "best")
    canvas = FigureCanvasTkAgg(fig, master = solutionFrame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def splitArray(arr):
    x = []
    y = []
    for i in range(len(arr)):
        if (i % 2) == 0:
            x.append(arr[i])
        else:
            y.append(arr[i])
    return x,y


##Interfaz
root = Tk()
root.geometry('1060x720')
root.configure(bg = 'white')
root.title('Proyecto')

mainFrame = tk.Frame(root)
mainFrame.pack(fill=BOTH,expand=1)

canvas = tk.Canvas(mainFrame,bg = 'white')
canvas.pack(side=LEFT,fill=BOTH,expand=1)
canvas.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
 
scrollBar = ttk.Scrollbar(mainFrame,orient=VERTICAL, command=canvas.yview)
scrollBar.pack(side=RIGHT,fill=Y)

canvas.configure(yscrollcommand=scrollBar.set)
##Imagenes
sFrame = Frame(canvas)
canvas.create_window((0,0),window=sFrame,anchor="nw")

global frameMenu
frameMenu = tk.Frame(sFrame, bg ='white')

frameMenu.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox("all")))

scrollBar = ttk.Scrollbar(frameMenu,orient=VERTICAL, command=canvas.yview)
scrollBar.pack(side=RIGHT,fill=Y)

banner = tk.PhotoImage(file="banner.png")
startPage = tk.PhotoImage(file="inicio.png")
##Estilos
style = ttk.Style()
style.configure('TButton', background ='#1d2239',borderwidth = '0',font = ('Sans Serif', 10, 'bold'), foreground = '#76BE49')
customFont = Font(font='lbFont',family='Sans Serif', size=10)
##Header
frameHeader = tk.Frame(sFrame, bg ='#1d2239', height= 130)
frameHeader.pack(fill=BOTH, expand=1)

l1 = tk.Label(frameHeader,image=banner, bg ='#1d2239')
l1.pack(fill=X)

btn1 = ttk.Button(frameHeader, text = 'Inicio', style = 'TButton', command = lambda: inicio(frameMenu))
btn1.pack(side=LEFT,fill=BOTH)
btn2 = ttk.Button(frameHeader, text = 'Ingresar datos', style = 'TButton', command = lambda: ingresarDatos(frameMenu))
btn2.pack(side=LEFT,fill=BOTH, padx=10)
btn3 = ttk.Button(frameHeader, text = 'Ingresar archivo', style = 'TButton', command = lambda: cargarArchivo(frameMenu))
btn3.pack(side=LEFT,fill=BOTH, padx=10)
btn4 = ttk.Button(frameHeader, text = 'Salir', style = 'TButton', command = quit)
btn4.pack(side=RIGHT,fill=BOTH, padx=10)
inicio(frameMenu)

frameMenu.pack()

root.mainloop()

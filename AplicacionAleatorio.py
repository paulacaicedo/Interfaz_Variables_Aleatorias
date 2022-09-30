# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""



import math as ma
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import *

import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#import pandas as pd
import matplotlib.pyplot as plot
#from pandastable import Table
 

#DATOS GENERALES DE USO
media = 10;
desviacion = 2;
tasa = 0.5
Escala = 2;
Forma = 5
teta=4.5
a=25

#Funciones

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)


def tool_bar(canvas,funcion):
    toolbar = NavigationToolbar2Tk(canvas, funcion)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    
    canvas.mpl_connect("key_press_event", on_key_press)


#SACAR VALORES PSEUDOALEATORIOS

def visual_basic(semilla, cantidad):
    
    ri = []
    
    m = ma.pow(2, 24)
    xi = semilla
    for i in range(0,cantidad):
        temp = int((a*xi)%m)
        r = temp / (m-1)
        ri.append(r)
        xi = temp
        
        
    
    return ri
    
    
def fortran(semilla, cantidad):
    ri = []
    
    xi = semilla
    for i in range(0,cantidad):
        temp = int((1140671485*(xi)+12820163)% ma.pow(2, 24))
        r = int(630360016*(temp) % (ma.pow(2, 31)-1))
        
        xi = temp
        ri.append(float('0.'+str(r)))
        
        
    return ri   
     
    


#PRIMERO FUNCIONES QUE REALIZAN LAS DISTRIBUCIONES


#DISTRIBUCION NORMAL

def distNor_boxMuller(r1,r2):
    
    z1 = []
    z2 = []
    
    xi = []
    
    for i in range(0,len(r1)):
        
        zi= ma.pow((-2*ma.log(r1[i])), 0.5)*ma.cos(2*ma.pi*r2[i])
        z1.append(zi)
        
        zi_1= ma.pow((-2*ma.log(r1[i])), 0.5)*ma.sin(2*ma.pi*r2[i])
        z2.append(zi_1)
    
    for i in range(0,len(z1)):
        xi.append(media + (desviacion*z1[i]))
        
    return xi
    
        
def distNor_Polar(r1,r2):
    
    w1 = []
    a1 = []
    
    z1 = []
    z2 = []
    
    
    for i in range(0, len(r1)):
        v1_i = ((-2*r1[i])-1)
        v2_i = ((-2*r2[i])-1)
        
        temp = ((v1_i)*(v1_i)) + ((v2_i)*(v2_i))
        w1.append(temp)
        
        print(temp)
        
        
        x =(-2*np.log(temp))/temp
        ai = ma.sqrt(x)
        a1.append(ai)
        
        z1.append(ai*v1_i)
        z2.append(ai*v2_i)
        
    
    return z1,z2
        



#DISTRIBUCION LOG.NORMAL


def dist_logNormal(r1,r2):
    
    xi = []
    z1= distNor_boxMuller(r1,r2)
    
    for i in range(0, len(z1)):
        xi.append(ma.exp(z1[i]))
        
    
    return xi
    
    
    


#DISTRIBUCION CHI CUADRADA

def dist_chi_cuadrada(grados,r1,r2):
    
   
    
    chi = []
    lista_r = []
    longitud = 0
    

    #numeros aleatorios de distribucion normal
    for i in range(0,grados):
        
        xi = distNor_boxMuller(r1,r2)
        lista_r.append(xi)
        longitud = len(xi)
        
    
    
    for i in range(0,longitud):
        for j in range(0,grados):
            x =+ ma.pow(lista_r[j][i], 2)
        
        chi.append(x);

    
    return chi

    


#DISTRIBUCION T

def dist_T(grados,r1,r2):
    
    #numeros pseudoaleatorios de acuerdo al grado siempre por lo menos debe de haber dos
    
    ti = []
    lista_r = []
    longitud = 0
    
    #numeros aleatorios de distribucion normal
    for i in range(0,grados):
        
        z1 = distNor_boxMuller(r1,r2)
        lista_r.append(z1)
        longitud = len(z1)
    
    
    for i in range(0,longitud):
        
        x = 0
        for j in range(1,grados):
            
            print(lista_r[j][i])
            x = x + (lista_r[j][i])
            
        
        print(x)
        temp = lista_r[0][i] / ma.sqrt(x/grados-1)
        
        ti.append(temp)
        
        
    return ti
    



#DISTRIBUCION F

def dist_F(grado1,grado2,r1,r2,r3,r4):
    
    
    fi = []
    
    x1 = dist_chi_cuadrada(grado1,r1,r2)
    x2 = dist_chi_cuadrada(grado2,r3,r4)
    
  
    for i in range(0,len(x1)):
        temp = x1[i]/x2[i]
        
        
        
        fi.append(temp)
    
    
    return fi
    
    
    
   
#DISTRIBUCION EXPONENCIAL

def dist_Exponencial(r1,r2):
    
    z1,z2 = distNor_boxMuller(r1,r2)
    di = []
    for i in range(0,len(z1)):
        temp = (-1/tasa) * ma.log(z1[i])
        di.append(temp)
        
    return di
  
  
#DISTRIBUCION GAMMA


def dist_gamma(r1,r2):
    
    
    di = []
    
    b = Forma * (-ma.log(4))
    q =  1/ Forma
    d = 1 + ma.log(teta)
    a_1 = (1/(ma.sqrt(2*Forma-1)))
    
    
    # HALLAR VI, ZI, WI, YI
    
    vi = []
    zi = []
    yi = []
    wi = []
    
    for i in range(0,len(r1)):
        v1 = a_1* (ma.log(r1[i]/(1-r2[i])))
        vi.append(v1)
    
    for i in range(0,len(r1)):
        z1 = (ma.pow(r1[i], 2)*r2[i])
        zi.append(z1)
        
    for i in range(0,len(vi)):
        y1 = Forma*ma.exp(vi[i])
        yi.append(y1)
        
    for i in range(0,len(vi)):
        w1 = b + q*vi[i] - yi[i]
        wi.append(w1)
        
    for i in range(0,len(wi)):
        x = (wi[i] + d) - (teta*zi[i])

        if(x>0):
            print('si')
            d1 = Escala * y1
            di.append(d1)
        else:
            print('aca')
            if(w1 >= (ma.log10(z1))):
                print('si')
                d1 = Escala * y1
                di.append(d1)
        

    return di
            
        
        
        


#------------------------------------------------------------------------------
#GRAFICOS
def histograma(datos):

    funcion = tk.Tk()
    
    #Figure(figsize=(5, 4), dpi=100) 
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.hist(x=datos)
    

    canvas = FigureCanvasTkAgg(fig, funcion)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    
    ax.set_xlabel('Valor de los datos')
    ax.set_ylabel("Cantidad de los datos")
    
    tool_bar(canvas,funcion)
    
    
    funcion.mainloop()


 
#----------------------------------------------------------------------



def algoritmo(event):
    
     
    
    global grados_1
    global grados_2
    
    global entrada_grados_1
    global entrada_grados_2
    
    grados_1 = tk.StringVar()
    grados_2 = tk.StringVar()
    
    entrada_grados_1 = ttk.Label(master, text="Grados Libertad 1:")
    entrada_grados_1.place_forget()
    
    entrada_grados_2 = ttk.Label(master, text="Grados Libertad 2:")
    entrada_grados_2.place_forget()
    
    
    gr_1 = ttk.Entry(master,textvariable=grados_1)
    gr_1.place_forget()
    gr_2 = ttk.Entry(master,textvariable=grados_2)
    gr_2.place_forget()
     
    
    seleccion_aleatoria = str(combo.get())
    
    if(seleccion_aleatoria == "Dist.Chi-Cuadrado"):
         
        entrada_grados_1.place(x=30, y=170)
        gr_1.place(x=140, y=170)
        
    
    if(seleccion_aleatoria == "Distribucion T"):
        
        entrada_grados_1.place(x=30, y=170)
        gr_1.place(x=140, y=170)
    
    if(seleccion_aleatoria == "Distribucion F"):
        
        entrada_grados_1.place(x=30, y=170)
        gr_1.place(x=140, y=170)
        
        entrada_grados_2.place(x=270, y=170)
        gr_2.place(x=369, y=170)
        
    if(seleccion_aleatoria == "Distribucion Log-Normal"):
        entrada_grados_1.grid_remove()
        entrada_grados_2.grid_remove()
        
       
    
     

    
    
    
#---------------------------------------------------------------------------------

 

def graficar():
    
    r1 = []
    r2 = []
     
    xi = []
    
    seleccion_aleatoria = str(combo.get())
    can = int( variable_cantidad.get())
    sem = int(variable_semilla.get())
    seleccion_generador = str(combo_1.get())
    valor = grafico_valor.get()
    
     
    re = ''.join(reversed(str(variable_semilla.get())))
    
    if(seleccion_aleatoria == "Dist.Normal BoxMuller"):
        if(seleccion_generador == "VisualBasic"):
            r1 = visual_basic(sem,can)
            r2 = visual_basic((int(re)+1),can)

            xi = distNor_boxMuller(r1,r2)
           
            if(valor == 1): histograma(xi)
            
            
             
        if(seleccion_generador == "Fortran"):
            r1 = fortran(sem,can)
            r2 = fortran((int(re)+1),can)

            xi = distNor_boxMuller(r1,r2)
           
            if(valor == 1): histograma(xi)
         
        
        
    #-------------------------------------------------------------------    
        
    if(seleccion_aleatoria == "Distribucion Log-Normal"):
        print('Log Normal')
        if(seleccion_generador == "VisualBasic"):
            r1 = visual_basic(sem,can)
            r2 = visual_basic((int(re)+1),can)

            xi = dist_logNormal(r1,r2)
           
            
            if(valor == 1): histograma(xi)
            
            
            
        if(seleccion_generador == "Fortran"):
            r1 = fortran(sem,can)
            r2 = fortran((int(re)+1),can)

            xi = dist_logNormal(r1,r2)
           
            if(valor == 1): histograma(xi)
        
     
    #------------------------------------------------------------    
     
    if(seleccion_aleatoria == "Distribucion Exponencial"):
       print('Exponencial')
       if(seleccion_generador == "VisualBasic"):
           r1 = visual_basic(sem,can)
           r2 = visual_basic((int(re)+1),can)

           xi = dist_Exponencial(r1,r2)
         
           
           if(valor == 1): histograma(xi)
           
           
           
       if(seleccion_generador == "Fortran"):
           r1 = fortran(sem,can)
           r2 = fortran((int(re)+1),can)

           xi = dist_Exponencial(r1,r2)
          
           if(valor == 1): histograma(xi)

            
     #------------------------------------------------------------------------    
            
    if(seleccion_aleatoria == "Dist.Chi-Cuadrado"):
        
        g_1 = int(grados_1.get())
         
        
        if(seleccion_generador == "Fortran"):
            r1 = fortran(sem,can)
            r2 = fortran((int(re)+1),can)

            xi = dist_chi_cuadrada(g_1,r1,r2)
            
           
            if(valor == 1): histograma(xi)
        
        if(seleccion_generador == "VisualBasic"):
            
           r1 = visual_basic(sem,can)
           r2 = visual_basic((int(re)+1),can)
           
           xi = dist_chi_cuadrada(g_1,r1,r2)
            
           
           if(valor == 1): histograma(xi)
        
           
           
    
         
    #------------------------------------------------------------------------        
    if(seleccion_aleatoria == "Distribucion T"):
        
        g_1 = int(grados_1.get())
        
        if(seleccion_generador == "Fortran"):
            r1 = fortran(sem,can)
            r2 = fortran((int(re)+1),can)

            xi = dist_T(g_1,r1,r2)
            
           
            if(valor == 1): histograma(xi)
         
        
        if(seleccion_generador == "VisualBasic"):
           r1 = visual_basic(sem,can)
           r2 = visual_basic((int(re)+1),can)
           
           xi = dist_T(g_1,r1,r2)
         
           
           if(valor == 1): histograma(xi)
     
            
    #--------------------------------------------------------------
    if(seleccion_aleatoria == "Distribucion F"):
        
        g_1 = int(grados_1.get())
        g_2 = int(grados_2.get())
        
        print('Distribucion F')
        if(seleccion_generador == "VisualBasic"):
           r1 = visual_basic(sem,can)
           r2 = visual_basic((sem * sem),can)
           
           r3 = fortran(sem,can)
           r4 = fortran((int(re)+1),can)
           
           xi = dist_F(g_1,g_2,r1,r2,r3,r4)
          
           
           if(valor == 1): histograma(xi)
           
           
        if(seleccion_generador == "Fortran"):
            
            r1 = visual_basic(sem,can)
            r2 = visual_basic((int(re)+1),can)
            
            r3 = fortran(sem,can)
            r4 = fortran((sem * (sem-can)),can)
            
            xi = dist_F(g_1,g_2,r1,r2,r3,r4)
        
            
            if(valor == 1): histograma(xi)
        
            
    #----------------------------------------------------------------
    if(seleccion_aleatoria == "Distribucion Gamma"):
         
        if(seleccion_generador == "VisualBasic"):
            
            
            
            r1 = visual_basic(sem,can)
            r2 = visual_basic((int(re)+1),can)

            xi = dist_gamma(r1,r2)
            
            while(len(xi)==can):
                
                print('aca')
                
                np.random.seed(sem+5)
                x = np.random.rand()*10
                
                print(x)
                
                r1 = visual_basic(x,can)
                r2 = visual_basic((int(re)+1),can)
                
                print(x)
                xi = dist_gamma(r1,r2)
            
            print(xi)
           
            if(valor == 1): histograma(xi)
            
        if(seleccion_generador == "Fortran"):
            
            r1 = fortran(sem,can)
            r2 = fortran((int(re)+1),can)
            
            print(r1)
            print(r2)
            
            xi = dist_gamma(r1,r2)
            print(xi)
            
           
            if(valor == 1): histograma(xi)
        
            
    
#------------------------------------------------------------------------------------
#PANTALLA PRINCIPAL 

master = tk.Tk()
master.geometry('525x280')
master.title('Aplicacion')

texto = ttk.Label(master, text="Generador de Variables Aleatorias")
texto.place(x=150, y=10)

label_combo = ttk.Label(master, text="Seleccione la Variable Aleatoria")
label_combo.place(x=30, y=40)

aleatoria = tk.StringVar() 
combo = ttk.Combobox(master,textvariable=aleatoria,
                     values = ["Dist.Normal BoxMuller",
                                    "Distribucion Log-Normal",
                                    "Dist.Chi-Cuadrado",
                                    "Distribucion T",
                                    "Distribucion F",
                                    "Distribucion Exponencial",
                                    "Distribucion Gamma"
                                    ],state="readonly")
combo.place(x=30, y=60) 


combo.bind("<<ComboboxSelected>>",algoritmo)



label_combo_1 = ttk.Label(master, text="Seleccione la Generador Aleatorio")
label_combo_1.place(x=250, y=40)

combo_1 = ttk.Combobox(master,
                       values = ["VisualBasic",
                                    "Fortran",
                                    ],state="readonly")
combo_1.place(x=250, y=60) 


 

#CANTIDAD A GENERAR

variable_cantidad = tk.StringVar()
v = ttk.Label(master, text="Cantidad a Generar:")
v.place(x=30, y=120)

entrada_1 = ttk.Entry(master,textvariable=variable_cantidad)
entrada_1.place(x=140, y=120)


variable_semilla = tk.StringVar()
v = ttk.Label(master, text="Semilla Inicial:")
v.place(x=30, y=140)

entrada_1 = ttk.Entry(master,textvariable=variable_semilla)
entrada_1.place(x=140, y=145)




#METODO GRAFICOS
grafico_valor = tk.IntVar() 

texto_1 = ttk.Label(master, text="Seleccione Grafico:")
texto_1.place(x=30, y=200)

primer_grafico = tk.Radiobutton(master, text="Histograma", variable = grafico_valor, value=1)
primer_grafico.place(x=30, y=220)
 



#BOTON DE GRAFICA
button = tk.Button(master,text = 'Graficar', command = graficar)
button.place(x=390, y=220) 

master.mainloop()

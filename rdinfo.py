#!/usr/bin/python
# -*- UTF-8 -*-

import csv
from math import sqrt
from nltk import word_tokenize, ngrams
import nltk as nltk
import csv


import pandas as pd
import numpy as np

def CargarDiccionarioLemas():
    file=open("diccionarioLematizador.txt","rb")
    lema_d={}

    for line in file:
        #print(line)
        bloques = line.split()
        palabra = bloques[0]
        lema = bloques[1]
        #print("i",a,b)
        #print( bloques[0],bloques[1])
        lema_d.update({palabra:lema})
    return lema_d

def lematizador(lema_d,palabra):
    palabra=palabra.lower()
    if palabra in lema_d:
        lema = str(lema_d.get(palabra))
    else:
        lema = palabra
    return lema

def cargaStopWords():
    file = open("stopwords.txt", "rb")
    stopWords = {}
    for linea in file:
        linea = linea.replace('\n','')
        if not linea in stopWords:
            stopWords.update({linea:linea})
    #print(stopWords)
    return stopWords

def stopWordFilterLematiza(lema_d,stopwordlist,linea):
    salida = ""
    palabras = word_tokenize(linea)
    for palabra in palabras:
        if not palabra in stopwordlist:
            salida = salida + lematizador(lema_d,palabra) +" "
    return salida

def generaDiccionario(texto):
    diccionario = dict()
    wordIndex = 0
    for linea in texto:
        palabras = linea.split()
        for palabra in palabras:
            if not palabra in diccionario:
                diccionario.update({palabra:wordIndex})
                wordIndex += 1
    return diccionario

def calculaCoseno(a,b,sizeVec):
    sumXX, sumXY, sumYY = 0 , 0 , 0
    for i in range( 0 , sizeVec-1):
        x = a[i]
        y = b[i]
        sumXX += x * x
        sumYY += y * y
        sumXY += x * y
    return sumXY / sqrt(sumXX*sumYY)

def getCosine(x):
    return x[1]

#####  INICIO

bufferEntrada=[]  #para guardar en memoria el archivo
nLines = 0        #lineas leidas
stopWords = cargaStopWords()
lema_d = CargarDiccionarioLemas()



#cargar archivo a analizar
with open("noticias_Apple.csv","rb") as aEntrada:
#with open("SoloLasNoticias.csv", "r", errors="ignore") as aEntrada:
        for linea in aEntrada:
            #Normalizar: Minusculas
            linea = linea.lower()
            #eliminamos comas  csv => txt
            linea = linea.replace(',',' ')
            #filtramos stop words
            linea = stopWordFilterLematiza(lema_d,stopWords,linea)
            bufferEntrada.append(linea)
            nLines += 1
            if nLines % 10000 == 0:
                print(nLines)

# Generar diccionario
nltk.download('punkt')
diccionarioPalabras = generaDiccionario(bufferEntrada)
print(diccionarioPalabras)
# Matriz de Termino - Documento
terminosDicc = len(diccionarioPalabras)
matrizTD = np.array([nLines,terminosDicc])
matrizTD = np.zeros([nLines,terminosDicc])
numLinea = 0

for linea in bufferEntrada:
    palabras = linea.split()
    for palabra in palabras:
        nColumna = diccionarioPalabras.get(palabra)
        matrizTD[numLinea][nColumna] += 1
    numLinea += 1
print(matrizTD)
print("Terminos ")
print(terminosDicc)

# Generamos vector Consulta
consulta = np.random.randint(2 , size=terminosDicc)
# similitud Coseno
simDict = dict()
for i in range(0 , nLines-1):
    documento = matrizTD[i]
    simDict[i]=calculaCoseno(documento , consulta , terminosDicc)
# mostrar Top 10
listaTop = [[d,c] for d,c in simDict.items()]
listaTop.sort(key=getCosine,reverse=1)

print("############### BEST 10  ##############")
print(listaTop[:10])

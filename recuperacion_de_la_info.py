from nltk import word_tokenize, ngrams
import csv

def crearDiicionarioBigrama():

    with open('noticias_Apple.csv', 'r', encoding='utf8') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')

        terminos = []

        listaBigramas = []
        for linea in fileReader:
            # print(linea[4].lower())

            lineaSplit = word_tokenize(linea[4])
            twoGrams = ngrams(lineaSplit, 2)
            for bigrama in twoGrams:
                #print(palabra)
                if bigrama not in terminos:
                    print (bigrama)
                    terminos.append(bigrama)

    print(terminos)
    return terminos

def crearDiicionario():

    with open('noticias_Apple.csv', 'r', encoding='utf8') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')

        terminos = {}

        for linea in fileReader:
            # print(linea[4].lower())

            lineaSplit = word_tokenize(linea[4])

            for palabra in lineaSplit:
                print(palabra)
                terminos[palabra] = 1

        print(terminos)
    return terminos
#crearDiicionario()

def crearMatrizTerminoDocumento():
    terminos = crearDiicionarioBigrama()

    with open('noticias_Apple.csv', 'r', encoding='utf8') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for linea in fileReader:
            listaVectorDocumento = []
            for bigrama in terminos:
                #print(word)
                listaDocumento = word_tokenize(linea[4])

                if bigrama in listaDocumento:
                    listaVectorDocumento.append(listaDocumento.count(bigrama))
                else:
                    listaVectorDocumento.append(0)
            print(listaVectorDocumento)
#crearMatrizTerminoDocumento()

def crearVEctorConsulta(texto):
    terminos = crearDiicionario()

    vectorConsulta=[]
    query = word_tokenize(texto)

    for word, valor in terminos.items():
        if word in query:
            vectorConsulta.append(1)
        else:
            vectorConsulta.append(0)

    print(vectorConsulta)

#crearVEctorConsulta(" no conocer Revelan !!!")

import math
def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)



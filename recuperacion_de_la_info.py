from nltk import word_tokenize, ngrams
import nltk as nltk
import csv
import math


stopWords = {}
lema_d = {}
terminos = {}

def CargarDiccionarioLemas():
    file=open("diccionarioLematizador.txt","r")
    #lema_d={}

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
    file = open("stopwords.txt", "r")
    #stopWords = {}
    for linea in file:
        linea = linea.replace('\r','')
        linea = linea.replace('\n','')
        if not linea in stopWords:
            stopWords.update({linea:linea})
    #print(stopWords)
    return stopWords



def crearDiicionarioBigrama():
    with open('noticias_Apple.csv', 'r') as csvfile:
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

#    with open('noticias_Apple.csv', 'r') as csvfile:
    with open('na.csv', 'r') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for linea in fileReader:
            # print(linea[4].lower())
            lineaSplit = word_tokenize(linea[4])

            for palabra in lineaSplit:
                palabra = palabra.lower()
                if palabra not in stopWords:
                    palabra = lematizador(lema_d, palabra)
                    print(palabra)
                    terminos[palabra] = 1
        print(terminos)
    return terminos
#crearDiicionario()

def crearMatrizTerminoDocumento():
    terminos = crearDiicionarioBigrama()

    with open('noticias_Apple.csv', 'r') as csvfile:
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

    vectorConsulta=[]
    query = word_tokenize(texto)

    for word, valor in terminos.items():
        word = lematizador(lema_d,word)
        if word in query:
            vectorConsulta.append(1)
        else:
            vectorConsulta.append(0)

    print(vectorConsulta)
    return vectorConsulta

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)




nltk.download('punkt')
cargaStopWords()
lema_d = CargarDiccionarioLemas()
terminos = crearDiicionario()

vectorConsulta = crearVEctorConsulta(" no conocer amazon sale lanza !!!")


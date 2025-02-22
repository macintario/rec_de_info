from nltk import word_tokenize, ngrams
import pymongo
import nltk as nltk
import csv
import math
from flask import Flask ,request, jsonify

bufferNoticias = []

stopWords = {}
lema_d = {}
terminos = {}

textoLematizado = []

matrizTD =[]

cliente = pymongo.MongoClient("mongodb://localhost:27018/") #server
basedd = cliente["recinfo"] #database
coleccion = basedd["noticias"]


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
    id=0
#    with open('noticias_Apple.csv', 'r') as csvfile:
    with open('na.csv', 'r') as csvfile:
        fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for linea in fileReader:
            # print(linea[4].lower())
            renglonLematizado = []
            #bufferNoticias[id] = []
            bufferNoticias.append([{"id":id},{"encabezado":linea[4]},{"url":linea[5]},{"noticia":linea[6]},{"vector":[]}])
            id += 1
            lineaSplit = word_tokenize(linea[4])

            for palabra in lineaSplit:
                palabra = palabra.lower()
                if palabra not in stopWords:
                    palabra = lematizador(lema_d, palabra)
                    #print(palabra)
                    renglonLematizado.append(palabra)
                    terminos[palabra] = 1
            textoLematizado.append(renglonLematizado)
        #print(terminos)

    return terminos
#crearDiicionario()



def crearMatrizTerminoDocumento():
#    terminos = crearDiicionarioBigrama()
    nLinea = 0
#    with open('noticias_Apple.csv', 'r') as csvfile:
#    with open('na.csv', 'r') as csvfile:
#        fileReader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for linea in textoLematizado:
        listaVectorDocumento = [0]*len(terminos)
        for palabraLematizada in linea:
            nTermino = 0
            for palabraDicc in terminos:
                if palabraDicc == palabraLematizada:
                    listaVectorDocumento[nTermino] = 1
                #else:
                #    listaVectorDocumento.insert(nTermino, 0)
                nTermino += 1
            #print(listaVectorDocumento)
        #registro = bufferNoticias[nLinea][4]
        #registro["vector"] = listaVectorDocumento
        bufferNoticias[nLinea][4]["vector"] = listaVectorDocumento
        #print(registro)
        nLinea +=1
        matrizTD.append(listaVectorDocumento)
    print(matrizTD)
    print(bufferNoticias)
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

    #print(vectorConsulta)
    return vectorConsulta

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0., 0., 0.
    for i in range(len(v1)):
        x = v1[i]+0.; y = v2[i]+0.
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

def almacenaMongo(coleccion,buffer):
    for registro in buffer:
        # print(registro)
        insercion = coleccion.insert({"id":registro[0]["id"],
                                      "encabezado": registro[1]["encabezado"],
                                      "url": registro[2]["url"],
                                      "noticia":registro[3]["noticia"],
                                      "vector":registro[4]["vector"]
                                      })
        #print(insercion)
        #id,encabezado,url,noticia,vector
    return 0

def getTopFive(queryVector,matrizTD):
    topFive =  []
    distancias = []
    nDoc=0
    for vDoc in matrizTD:
        distancia = cosine_similarity(queryVector, vDoc)
        distancias.append([nDoc,distancia])
        nDoc += 1
    distancias.sort(key=lambda d: d[1],reverse=1)
    print(distancias)
    topFive = distancias[:5]
    return topFive


################################################ main ###################################

#nltk.download('punkt')
cargaStopWords()
lema_d = CargarDiccionarioLemas()
terminos = crearDiicionario()
crearMatrizTerminoDocumento()

almacenaMongo(coleccion,bufferNoticias) #almacenamos las noticias


##################### Levantamiento de EndPoint   ###########################
app = Flask(__name__)
@app.route('/noticias', methods=['GET'])
def getNewsFromDatabase():

#http://localhost:5000/noticias?palabras=apple,servicio,spotify
    print(request.args)
    queryVector = crearVEctorConsulta(request.args["palabras"])
    top5 = getTopFive(queryVector,matrizTD)
    lasNoticias = []
    for doc,dist in top5:
        noticia  =  coleccion.find_one({"id":doc},{"_id":0})
        lasNoticias.append(noticia)
        print(noticia)
    return jsonify(success=True, data=lasNoticias)

if __name__ == "__main__":
  app.run(host='localhost', port=5000, debug=True)

#vectorConsulta = crearVEctorConsulta(" no conocer amazon sale lanza !!!")
#almacena vector en BDD y conservar matriz en memoria.
#busca vectorconsulta en metriz y luego buca vectores resultantes en BDD para trer noticias
#qry: db.noticias.find({"noticia":{"vector":[ 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0]}})

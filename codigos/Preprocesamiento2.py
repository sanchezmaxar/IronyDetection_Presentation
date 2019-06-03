import nltk
from string import punctuation
import pickle
from nltk.tokenize import TweetTokenizer,word_tokenize
# nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import itertools
import emoji

def preprocessing(corpus,getVocabulary):
    twits=[]
    with open(corpus,"r") as f:
        docs=f.read().splitlines()
        twits=[d.split("|",2) for d in docs]
    cont=0
    # letras=[("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u")]
    cosas=[("\\n","\n"),("http://link","η"),("\\\"","\"")]
    twitsVectors=[]
    vocabularioBueno=["UNK"]
    dcont=1/len(twits)
    
    for t in twits:
        print("Llevo {0}".format(cont),end="\r")
        t[1]=t[1].lower()
        
        for c,v in cosas:
            t[1]=t[1].replace(c,v)
        
        for c in t[1]:
            if getVocabulary:
                if c not in vocabularioBueno:
                    vocabularioBueno.append(c)##Aqui va lo de los vectores
        # input(list(t[1]))
        twitsVectors.append([int(t[0]), list(t[1])])
        cont+=dcont

    if getVocabulary:
        return twitsVectors,vocabularioBueno
    else:
        return twitsVectors

def SplitHash(hashTag):
    salida=[""]
    contM=0
    contm=0
    for c in hashTag:
        if c.isupper():
            if salida[-1]!="" :
                salida.append(c)
            else:
                salida[-1]+=c
            contM+=1
        else:
            salida[-1]+=c
            contm+=1
    if contM==len(hashTag) or contm==len(hashTag) or sum([1 for i in salida if len(i)==1])>len(salida)*0.5:
        return [hashTag]
    else:
        return salida

def wordVect2Vect(twits,vocabulario):
    vectores=[]
    cont=0
    dcont=1/len(twits)
    for t in twits:
        vAux=[]
        print("Llevo ",cont,end="\r")
        for p in t[1]:
            if p in vocabulario:
                vAux.append(vocabulario.index(p))
            else:
                vAux.append(vocabulario.index("UNK"))
        vectores.append([t[0],vAux])
        # input(vectores[-1])
        cont+=dcont
    return vectores    

def getVectors(archivoEntr,archivoPrue,archivoSalpickle):
    print("Inicia el preprocesamiento de {0} y {1}".format(archivoEntr,archivoPrue))
    twitsTrain,vocabulario=preprocessing(archivoEntr,True)
    print("Termine de encontrar el vocab y preprocessar el entrenamiento")
    twitsTest=preprocessing(archivoPrue,False)
    print("Termine de preprocesar la prueba")
    vectoresTrain=(wordVect2Vect(twitsTrain,vocabulario))
    print("Termine de encontrar los vectores de entrenamiento")
    vectoresTest=(wordVect2Vect(twitsTest,vocabulario))
    print("Termine de encontrar los vectores de prueba")

    print("Guardando")

    vTrx=[]
    vTry=[]
    vTsx=[]
    vTsy=[]
    for v in vectoresTrain:
        vTry.append(v[0])
        vTrx.append(v[1])
    for v in vectoresTest:
        vTsy.append(v[0])
        vTsx.append(v[1])
    pickle.dump([(vTrx,vTry),(vTsx,vTsy)],open(archivoSalpickle,"wb"))

lista=[["corpus_train0.txt","corpus_test0.txt","vectoresSet0.pkl"],
    ["corpus_train1.txt","corpus_test1.txt","vectoresSet1.pkl"],
    ["corpus_train2.txt","corpus_test2.txt","vectoresSet2.pkl"],
    ["corpus_train3.txt","corpus_test3.txt","vectoresSet3.pkl"],
    ["corpus_train4.txt","corpus_test4.txt","vectoresSet4.pkl"],
    ]
for docs in lista:
    print("Preprocesando {0},{1},{2}".format(docs[0],docs[1],docs[2]))
    getVectors(docs[0],docs[1],docs[2])
print("Termine todo.")
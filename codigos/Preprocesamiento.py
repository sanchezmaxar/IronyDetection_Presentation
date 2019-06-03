from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score,confusion_matrix,recall_score,precision_score,f1_score
from unicodedata import normalize
import numpy as np
import re
import random
import pickle

def noCaracteresEspeciales(texto):
	# -> NFD y eliminar diacríticos
	texto = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", texto), 0, re.I
    )

	# -> NFC
	return re.sub('\W',' ',texto).lower()

def crearVocabulario(archCorpus,umbral):
	"""Con esta función creamos el vocabulario a partir del archCorpus
	INPUT: archCorpus- nombre del archivo con el corpus, 
		umbral- numero de apariciones minima para considerarlas relevantes
	OUTPUT: el vocabulario"""
	corpus=open(archCorpus,"r").readlines()
	vocabulario={"UNK":0}
	for twit in corpus:
		twitSplit=noCaracteresEspeciales(twit)
		for palabra in twitSplit.split():
			if palabra!="http://link":
				if palabra not in vocabulario:
					vocabulario[palabra]=1
				else:
					vocabulario[palabra]+=1
	ignorados=0
	for palabra in list(vocabulario):
		if vocabulario[palabra]<umbral:
			vocabulario["UNK"]+=1
			vocabulario.pop(palabra)
			ignorados+=1
	print("ignore ",ignorados," palabras")
	return vocabulario

def obtenerCorpuses(nombreArchivo,nombresBase):
	"""Con esta función se crea 5 archivos con las  secciones del corpus
	INPUT:el nombre del corpus completo sin seccionar
	OUTPUT:si el proceso fue exitoso regresa los nombres de los archivos sino 0"""
	try:
		corpus=open(nombreArchivo,"r").readlines()
		random.shuffle(corpus,random.random)
		X=[x.split("|",2)[2] for x in corpus]
		y=[y.split("|",2)[1] for y in corpus]
		# X=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
		# y=np.array([20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1])
		print('El total del corpus es: ',len(X),' twits')
		skf = KFold(n_splits=5)
		i=0
		nombres=[]
		for train, test in skf.split(X, y):
			# print("%s %s" % (train, test))
			f=open(nombresBase[0]+str(i)+".txt","w")
			for idx in train:
				f.write(y[idx]+"|"+X[idx])
			f.close()
			f=open(nombresBase[1]+str(i)+".txt","w")
			for idx in test:
				f.write(y[idx]+"|"+X[idx])
			nombres.append([nombresBase[0]+str(i)+".txt",nombresBase[1]+str(i)+".txt"])
			i+=1
			f.close()

		return nombres
	except Exception as e:
		print("Ha ocurrido un problema: ",e)
		return 0

def convertirAVector(oracion,dic):
	vector=[]
	texto=noCaracteresEspeciales(oracion).split()
	for t in texto:
		try:
			vector.append(dic.index(t))
		except:
			vector.append(dic.index("UNK"))
	return vector


def corpusAVectores(corpuses,basePickle,vocabulario,separacion,ids):
	# try:
	dic=list(vocabulario.keys())
	# print(corpuses)
	with open(corpuses[0],"r") as f:
		c=f.readlines()
		vect_train=np.array(list(map(lambda x:(int(x[0]),convertirAVector(x[1],dic)),[i.split(separacion,1) for i in c ])),dtype=object)
	with open(corpuses[1],"r") as f:
		c=f.readlines()
		vect_test=np.array(list(map(lambda x:(int(x[0]),convertirAVector(x[1],dic)),[i.split(separacion,1) for i in c ])),dtype=object)
		# print(vect_test)

	pickle.dump([(vect_train[:,1],vect_train[:,0]),(vect_test[:,1],vect_test[:,0]),dic],open(basePickle+str(ids)+".pkl","wb"))

	return basePickle+str(ids)+".pkl"
	# except Exception as e:
	# 	print("Ha ocurrido un error: ",e)
	# 	return 0
nombresCorpus=obtenerCorpuses(
	"corpus_complete_alan.txt",
	["corpus_train","corpus_test"])
print("----Terminado----\n\n")
# ----------------------------------------
i=0
for nombre in nombresCorpus:
	print("Creando el vocabulario")
	print(colored("\tCorpus "+str(i+1)+" de 5\n\n",'red'))
	
	# ----------------------------------------
	#creamos el vocabulario
	vocabulario=crearVocabulario(
		nombre[0] #el corpus de entrenamiento
		,5 #umbral a partir de cuantas apariciones se considera relevante
		)
	print("----Terminado----\n\n") 
	
	# ----------------------------------------
	#Aqui convertimos a vectores los corpus actuales el de entrenamiento y el de test
	print("Obteniendo los vectores...")
	nombreVectores=corpusAVectores(nombre,"vectores",vocabulario,"|",i)
	print("----Terminado----\n\n")
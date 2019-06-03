"""Este script genera los """
print("Cargando bibliotecas")
from utilidades import *
from termcolor import colored
# print(colors.red('this is red'))
print("----Terminado----\n\n")

# ----------------------------------------
# Con esta función se secciona el corpus y lo 
print("Obteniendo los corpus")
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
	
	# ----------------------------------------
	# Aqui entrenamos la bi-lstm
	print("Entrenando...")
	bi_lstm(nombreVectores,
		"modeloJson_corpus"+str(i)+".json",
		"pesosh5"+str(i)+".hd5")

	print("----Terminado----\n\n")

	# ----------------------------------------
	# Aqui vamos a evaluar el modelo que se ha creado
	evaluar("modeloJson_corpus"+str(i)+".json",
		"pesosh5"+str(i)+".hd5",
		nombreVectores)

	i+=1
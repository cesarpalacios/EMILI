# -*- coding: utf-8 -*- 

#!/usr/bin/env python
#Created by @ceapalaciosal
#Codigo bajo Creative Commons
import json


def tratamiento(matriz, a, datos):
	
	dia = matriz[a-1,0]
	fecha = matriz[a-1,1]
	nodo = matriz[a-1,2]
	direccion = matriz[a-1,3]
	porDireccion = False
	

	vn = a-1
	

	head = matriz[2,:]
	colHora = 0 
	colSentido = 0
	colData = 0
	colObservaciones = 0
	index = 0
	for value in head:
		if value == "PERIODO" or value == "PERÍODO": #La columna del periodo(HORA...)
			colHora = index
		if value == "SENTIDO": #Aunque no se use, sirve para saber donde comienzan los datos
			colSentido = index
		if value == "OBSERVACIONES":
			colObservaciones=index #Marca el final de las columnas de datos
		index+=1

	colData = max(colHora, colSentido)+1 # Esto marca el comienzo de los datos
	matriz = matriz[3:vn,:]

	clasificaciondatos(matriz, dia, fecha, nodo, direccion, datos, head, colHora, colSentido, colData, colObservaciones)

def entero(numero):
	numero = float(numero)
	valor = int(numero)
	return valor

def clasificaciondatos(matriz, dia, fecha, nodo, direccion, datos, head, colHora, colSentido, colData, colObservaciones):

	sentt = sent1 = sent1B = sent2 = sent2B = sent3 = sent3B = sent4 = sent4B = 0
	tamano = len(matriz[:,1]) #Numero de filas

	cont = 0
	tamano = len(matriz[:,1]) #Numero de filas

	
	#Obtenemos la informacion del archivo 
	tipoDia = "HABIL"
	if dia in ["SABADO","DOMINGO"]:
		tipoDia = "NOHABIL"

	key = tipoDia+"_"+direccion+"_"+nodo

	if datos.get(key) is None:
		datos[key]={}
	
	entry = datos[key]

	if entry.get(fecha) is None:
		entry[fecha]={}


	entryFecha = entry[fecha]

	for i in range(0, tamano):
		h = int(float(matriz[i, colHora])/100)
		sentido = matriz[i][colSentido]
		if entryFecha.get(h) is None:
			entryFecha[h]={}
			for j in range(colData, colObservaciones-1):
				entryFecha[h][head[j]]=[]

		for j in range(colData, colObservaciones-1):
			entryFecha[h][head[j]].append(matriz[i][j])

		if sentido == '1.0': 
			sent1 = 1
		if sentido == '1B':
			sent1B = 1
		if sentido == '2.0':
			sent2 = 1
		if sentido == '2B':
			sent2B = 1
		if sentido == '3.0':
			sent3 = 1
		if sentido == '3B': 
			sent3B = 1
		if sentido == '4.0':
			sent4 = 1
		if sentido == '4B': 
			sent4B = 1	

	sentt = sent1 + sent2 + sent3 + sent4 + sent1B + sent2B + sent3B + sent4B	
	keys = datos[tipoDia+"_"+direccion+"_"+nodo][fecha].keys()
	for key in keys:
		datosHora = datos[tipoDia+"_"+direccion+"_"+nodo][fecha][key]
		types = datosHora.keys()
		for tipo in types:
			datosHora[tipo] = eval('+'.join(datosHora[tipo]))/sentt
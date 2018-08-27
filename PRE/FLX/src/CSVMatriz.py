# -*- coding: utf-8 -*- 
#!/usr/bin/env python

#Created by @ceapalaciosal
#Codigo bajo Creative Commons

import csv
import datetime
import numpy as np
import os
import sys
sys.path.append('core')
from wcsv import *
from clasificacion import *
from matriz import *



def listaCSV(direccion, Year):
	path = os.path.join(direccion,'')

	lstFilesEmissions = []

	lstDir = os.walk(path)  
	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == ".csv"):
	        	lstFilesEmissions.append(nombreFichero+extension)

	#print "Number files in format CSV: ", len(lstFilesEmissions)

	data = {}
	lectura(lstFilesEmissions, direccion, data)

	#Hace promedio estacion, fecha, hora

	estacion = data.keys()
	for est in estacion:
		fechas = data[est].keys()
		primerDia =  data[est][fechas[0]]


		for i in range(1, len(fechas)):
			dataDia = data[est][fechas[i]]
			keys = dataDia.keys()
			for key in keys:
				dataHora = dataDia[key]
				types = dataHora.keys()			
				for tipo in types:
					primerDia[key][tipo] += dataHora[tipo]		
		

		hora = primerDia.keys()

		for hour in hora: 
			flows =  primerDia[hour].keys()
			
			for flow in flows:
				primerDia[hour][flow] = primerDia[hour][flow]/len(fechas)


		data[est] = primerDia
		
		for hour in hora: 
			flows =  primerDia[hour].keys()
			suma = 0
			for flow in flows:
				suma +=  primerDia[hour][flow]
			
			primerDia[hour]['TOTAL'] = suma

		data[est] = primerDia

	write(data, direccion, Year)
	

def lectura(lstFilesEmissions, direccion, data):
	tamano = len (lstFilesEmissions)

	for emissions in lstFilesEmissions[0:]:
		direccionuno = os.path.join(direccion,'')
		direccioncsv = direccionuno + emissions
		matriz = np.genfromtxt(direccioncsv, delimiter='|', dtype=None)

		a = len(matriz)
		tratamiento(matriz, a, data)


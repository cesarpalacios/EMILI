#Created by @ceapalaciosal
#Codigo bajo Creative Commons
#-*-encoding: utf-8 -*-

#!/usr/bin/env python

#List Library Import
import csv
import os
import unicodedata
import xlrd
import datetime


def readsum(workbook, direccioncsv):

	days = {'MONDAY':'LUNES','TUESDAY':'MARTES','WEDNESDAY':'MIERCOLES','THURSDAY':'JUEVES','FRIDAY':'VIERNES','SATURDAY':'SABADO','SUNDAY':'DOMINGO'}

	direccioncsv = os.path.join(direccioncsv,'')

	dh = workbook.sheet_by_index(0) #Numero de Sheet donde se encuentran los datos generales.
	sh = workbook.sheet_by_index(1) #Numero de Sheet donde se encuentran los datos BASE
	

	nodo = int(dh.cell_value(2, 21))
	fecha = dh.cell_value(6, 21)
	if type(fecha) == float:
		fecha = str(int(fecha))

	year = int(str(20)+str(fecha[4:]))
	day = int(fecha[:2])
	month = int(fecha[2:4])
	
	fecha = datetime.date(year, month, day)
	
	dia = days[fecha.strftime('%A').upper()]
	#print dia
	

	if type(sh.cell_value(4, 3)) is float:
		interseccion = sh.cell_value(4, 1) +"_"+ sh.cell_value(4, 2)
	else:
		interseccion = sh.cell_value(4, 2) +"_"+ sh.cell_value(4, 3)

	index = colXC5 = 0
	for pos in range (0, sh.ncols):
		if sh.cell_value(2, pos) == "C3":
			colC3 = index
		if sh.cell_value(2, pos) == "C4":
			colC4 = index
		if sh.cell_value(2, pos) == "C6":
			colC6 = index
		if sh.cell_value(2, pos) == ">C6":
			colXC6 = index
		if sh.cell_value(2, pos) == ">C5":
			colXC5 = index
		index += 1

	generales = [dia, fecha, nodo, interseccion,"NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN"] #23 Campos en X
	
	data = open(''.join([direccioncsv, str(nodo), '-', str(fecha), '.csv']), 'wb') #crea el csv datos
	fluj = csv.writer(data, delimiter='|')	
	#fluj.writerow([sh.cell_value(0, pos) for pos in range(0, 23)])
	fluj.writerow(['', 'ESTRUCTURA DE LA BASE DE DATOS', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
	fluj.writerow(["","FECHA DE TOMA DE INFORMACION EN FORMATO DD/MM/AAA","VIA  ESPECIFICA DONDE SE EFECTUO LA TOMA DE INFORMACION","LOCALIZACION ESPECIFICA DONDE SE EFECTUO LA TOMA DE INFORMACION","PERIODO DE CONTEO DE 15 MINUTOS IDENTIFICADO CON LA HORA HORA INICIAL DEL FORMATO GENERAL","ACCESOS A LOS FLUJOS VEHICULARES","AUTOMOVILES","COLECTIVOS","BUSETA/BUSETON","BUSES","ALIMENTADOR","ARTICULADO","BIARTICULADOS","BUS ESPECIAL","BUS INTERMUNICIPAL","CAMIONES DE 2 EJES PEQUENO","CAMIONES DE 2 EJES GRANDE","CAMIONES DE 3 y 4 EJES","CAMIONES DE 5 EJES","CAMIONES DE MAS DE 5 EJES","MOTOS","BICICLETAS","OBSERVACIONES REFERIDAS SOLAMENTE A LA TOMA DE INFORMACION"])
	fluj.writerow(["TOTAL MIXTOS","FECHA","VIA PRINCIPAL","VIA SECUNDARIA","PERIODO","SENTIDO","L","C","BT","B","AL","AT","BA","ESP","INT","C2P","C2G","C3-C4","C5",">C5","M","BIC","OBSERVACIONES"])
	

	for rownum in range(3, sh.nrows):
		
		dat = []

		for pos in range(0, colC3):
			dat.append(sh.cell_value(rownum, pos))
		
		#print dat
		C3andC4 = sh.cell_value(rownum, colC3) + sh.cell_value(rownum, colC4)
		dat.append(C3andC4)
		
		dat.append(sh.cell_value(rownum, colC4+1))
		
		if colXC5 == 0:
			XC5 = sh.cell_value(rownum, colC6) + sh.cell_value(rownum, colXC6)
			dat.append(XC5)
			
			for pos in range (colXC6+1, sh.ncols):
				dat.append(sh.cell_value(rownum, pos))

		else:
			for pos in range (colXC5, sh.ncols):
				dat.append(sh.cell_value(rownum, pos))
		if (int(dat[0])!=0): 
			if (dat[1] !=''):				
				fluj.writerow([dato.encode('utf8') if type(dato) is unicode else dato for dato in dat])	
	fluj.writerow([dato.encode('utf8') if type(dato) is unicode else dato for dato in generales])
	data.close()

def readsumtwo(workbook, direccioncsv):

	days = {'MONDAY':'LUNES','TUESDAY':'MARTES','WEDNESDAY':'MIERCOLES','THURSDAY':'JUEVES','FRIDAY':'VIERNES','SATURDAY':'SABADO','SUNDAY':'DOMINGO'}

	direccioncsv = os.path.join(direccioncsv,'')
	#workbook = xlrd.open_workbook(direccion) #encoding_override="utf-8")
	#all_worksheets = workbook.sheet_names()
	
	dh = workbook.sheet_by_index(0) #Numero de Sheet donde se encuentran los datos generales.
	sh = workbook.sheet_by_index(1) #Numero de Sheet donde se encuentran los datos BASE
	

	nodo = int(dh.cell_value(2, 21))
	fecha = dh.cell_value(6, 21)
	if type(fecha) == float:
		fecha = str(int(fecha))

	year = int(str(20)+str(fecha[4:]))
	day = int(fecha[:2])
	month = int(fecha[2:4])
	fecha = datetime.date(year, month, day)
	dia = days[fecha.strftime('%A').upper()]
	#print dia
	

	if type(sh.cell_value(4, 3)) is float:
		interseccion = sh.cell_value(4, 1) +"_"+ sh.cell_value(4, 2)
	else:
		interseccion = sh.cell_value(4, 2) +"_"+ sh.cell_value(4, 3)

	generales = [dia, fecha, nodo, interseccion,"NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN"] #23 Campos en X
	
	data_emissions = open(''.join([direccioncsv, str(nodo), '-', str(fecha), '.csv']), 'wb') #crea el csv datos Base
	emission = csv.writer(data_emissions, delimiter='|') #quoting=csv.QUOTE_ALL) #Abre el CSV para escritura de emsiones
	#Escribe los datos contenidos en el sheet Base
 	for rownum in xrange(sh.nrows):
 		
 		if (sh.row_values(rownum)[0]!=0):
 			emission.writerow([unicode(entry).encode("utf-8") for entry in sh.row_values(rownum)]) 	
 	emission.writerow([unicode(data).encode("utf-8") for data in generales])
	data_emissions.close()

def convertXLSCSV(lista, direccion):

	especificacionuno = os.path.join(direccion, '')

	for i in lista [0:]:
		direccionuno = os.path.join(direccion, '')
		direccionexcel = direccionuno + i
		print "Process File Excel", i
		workbook = xlrd.open_workbook(direccionexcel) #encoding_override="utf-8")
		#print "Abriendo Libro"
		sh = workbook.sheet_by_index(1) #Numero de Sheet donde se encuentran los datos BASE
		#print "Las columnas son", sh.ncols
		#print "Las Filas son", sh.nrows
		text = []

		for pos in range(0, sh.ncols):
			text.append(sh.cell_value(2, pos))
		

		if "C3" in text: 
			readsum(workbook, direccion) #Realiza la creacion CSV para los casos de C3, C4, C6 >C6
		else:	
			readsumtwo(workbook, direccion) #Realiza la creacion del CSV cuando la base de datos es normal

def listaExcel(direccion):
	#Variable para la ruta al directorio
	path = direccion
	#Lista vacia para incluir los ficheros
	lstFiles = []

	#Lista con todos los ficheros del directorio:
	lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros
	
	#Crea una lista de los ficheros que existen en el directorio y los incluye a la lista.
	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == ".xlsx" or extension == ".xls"):
	            lstFiles.append(nombreFichero+extension)

	print "Number files in format Excel: ", len(lstFiles)
	convertXLSCSV(lstFiles, direccion)

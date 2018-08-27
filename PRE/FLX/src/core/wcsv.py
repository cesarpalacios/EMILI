# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons

import csv
import os
import xlrd
from matriz import *

def writematriz(matriz, folder):

	csvsalida = open(folder + '.csv', 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	
	for x in range(0, matriz.shape[0]):
		salida.writerow(matriz[x])

	csvsalida.close()

# def writesum(data):
# 	folder = os.path.join('..', 'data', 'flows', '')
# 	csvsalida = open(folder +'sumcol.csv', 'w')
# 	salida = csv.writer(csvsalida, delimiter=',')

# 	salida.writerow(['Estacion', 'IDEstacion', 'IDNodo', '>C5', 'AL', 'AT', 'B', 'BA', 'BT', 'C', 'C2G', 'C2P', 'C3-C4', 'C5', 'ESP', 'INT', 'L', 'M', 'TOTAL', 'NH_>C5', 'NH_AL', 'NH_AT', 'NH_B', 'NH_BA', 'NH_BT', 'NH_C', 'NH_C2G', 'NH_C2P', 'NH_C3-C4', 'NH_C5', 'NH_ESP', 'NH_INT', 'NH_L', 'NH_M', 'NH_TOTAL'])

# 	IDEstation = data.keys()
	
# 	for ID in IDEstation: 

# 		flujos = sorted(data[ID]['HABIL'].keys())

# 		for veh in range(0, 3):
# 			csvsalida.write(data[ID]['GENERAL'][veh])
# 			csvsalida.write(',')
		
# 		for vehicles in flujos:
# 				csvsalida.write(str(data[ID]['HABIL'][vehicles]))
# 				csvsalida.write(',')

# 		for vehicles in flujos:
# 				csvsalida.write(str(data[ID]['NOHAB'][vehicles]))
# 				csvsalida.write(',')
# 		csvsalida.write('\n')
	
# 	csvsalida.close()

def writedisolver(data, Year): 
	
	folder = os.path.join('..', 'data','out', '')
	csvsalida = open(folder + 'MOB' + '_' + Year + '.csv', 'w')
	salida = csv.writer(csvsalida, delimiter=',')

	Title1 = ['Estacion', 'Tipo', 'IDEstacion', 'IDNodo', 'hora']
	#csvsalida.write() #'>C5_DSEL', '>C5_GNV', '>C5_Gas', 'AL_Dsel', 'AT_Dsel', 'AUT_GNV', 'AUT_Gas', 'BA_Dsel', 'BT_Dsel', 'B_Dsel', 'C2G_Dsel', 'C2G_GNV', 'C2G_Gas', 'C2P_Dsel', 'C2P_GNV', 'C2P_Gas', 'C3-C4_Dsel', 'C3-C4_GNV', 'C3-C4_Gas', 'CC_Dsel', 'CC_GNV', 'CC_Gas', 'ESP_Dsel', 'ESP_GNV', 'ESP_Gas', 'INT_Dsel', 'INT_GNV', 'INT_Gas', 'MB_Dsel', 'M_Gas', 'TX_GNV', 'TX_Gas', 'C5_Dsel', 'C5_GNV', 'C5_Gas'])
	
	keys = data.keys()
	#print data
	if ('HABIL' in data[keys[0]]['Tipo']): 
		Title2 = sorted(data[keys[0]]['Tipo']['HABIL']['hora'][0]['new'])
	else: 
		Title2 = sorted(data[keys[0]]['Tipo']['NOHAB']['hora'][0]['new'])
	Title = Title1 + Title2
	for leter in Title:
		if leter == Title[0]:
			csvsalida.write(leter)
		else: 
			csvsalida.write(',')
			csvsalida.write(leter)
	csvsalida.write('\n')



	for key in keys: 
		Types = data[key]['Tipo'].keys()
		for Type in Types: 
			hours = data[key]['Tipo'][Type]['hora'].keys()
			for hour in hours: 
				csvsalida.write(data[key]['Tipo'][Type]['Estacion'][0])
				csvsalida.write(',')
				csvsalida.write(Type)
				csvsalida.write(',')
				csvsalida.write(str(key))
				csvsalida.write(',')
				csvsalida.write(data[key]['Tipo'][Type]['IDNodo'][0])
				csvsalida.write(',')
				csvsalida.write(str(hour))
				category = data[key]['Tipo'][Type]['hora'][hour]['new'].keys()
				category = sorted(category)
				for cat in category: 
					csvsalida.write(',')
					csvsalida.write(str(data[key]['Tipo'][Type]['hora'][hour]['new'][cat]))
				csvsalida.write('\n')

def write(datos, folder, Year):

	IDEstation = os.path.join('..', 'data', 'in', 'Constants','IDNodos.xlsx')
	out = os.path.join('..', 'data', 'out', '')
	IDEstation = convertXLSCSV(IDEstation)
	csvsalida = open(out + 'RPM'+ '_' + Year + '.csv', 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	salida.writerow(['Estacion','Tipo','IDEstacion','IDNodo', 'hora', '>C5', 'AL', 'AT', 'B', 'BA', 'BT', 'C', 'C2G', 'C2P', 'C3-C4', 'C5', 'ESP', 'INT', 'L', 'M', 'TOTAL'])

	estacion = datos.keys()
	for est in estacion:
		cont = 0
		for ray in est:
			if ray == '_':
				pos = cont 
			cont += 1
		pos = pos + 1	
		if 'HABIL' in est: 
			day = est[:5]
			estacion = est[6:pos-1]
		else:
			day = est[:3]
			estacion = est[4:pos-1]
		
		IDNodo = est[pos:]

		
		for pos in range(1, len(IDEstation)):
			NNodo = int(float(IDEstation[pos][1]))
			if int(NNodo) == int(IDNodo): 
				NEstation = int(float(IDEstation[pos][0]))
				#break

			

		hora = datos[est].keys()
		
		if len(hora) < 24: 
			print 'WARNING! Review hours in station', NEstation, 'Nodo', IDNodo

		for hour in hora:
			flujos = []
			tipo = datos[est][hour].keys()
			tipo = sorted(tipo)
			#print tipo
			for tip in tipo:
				flujos.append(datos[est][hour][tip])
			csvsalida.write(estacion+','+day+','+str(NEstation)+','+IDNodo+','+str(int(float(hour)))+',')

			salida.writerow(flujos)
	csvsalida.close()			

	print 'Process END, Files output in folder: ', out






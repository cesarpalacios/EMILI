# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons

import sys
import os
import json
sys.path.append('core')
from clear import *
from ExcelCSV import*
from CSVMatriz import*
from disolver import*


def projection(flows, projections, Year, id):

	Mflows = convertCSVMatriz(flows)
	MProjections = convertXLSCSV(projections)
	flows = {}
	projection = {}

	for i in range(1, MProjections.shape[0]):
		name = MProjections[i][0]
		if projection.get(name) is None:
			projection[name] = float(MProjections[i][1])

	#print projection
	
	head = Mflows[0,:]
	index = 0
	for value in head:
		if value == 'IDNodo':
			colIDNodo = index
		if value == 'Estacion':
			colEstation = index
		if value == 'Tipo':
			colTipo = index
		if value == 'IDEstacion':
			colIDEstation = index
		if value == 'hora':
			colhour = index
		#if value == 'TOTAL':
			#colend = index
		index += 1

	for i in range(1, Mflows.shape[0]):
		key = int(Mflows[i][colIDEstation])
		hour = int(Mflows[i][colhour])
		Tipo = Mflows[i][colTipo]

		if flows.get(key) is None:
			flows[key] = {}
			flows[key]['Tipo'] = {}

		entrytipe = flows[key]['Tipo']
		if entrytipe.get(Tipo) is None:
			entrytipe[Tipo] = {'Estacion': [], 'IDNodo': [], 'hour': {}}


		if flows[key]['Tipo'][Tipo]['Estacion'] == []:
			flows[key]['Tipo'][Tipo]['Estacion'].append(Mflows[i][colEstation])
			flows[key]['Tipo'][Tipo]['IDNodo'].append(Mflows[i][colIDNodo])

		entryhour = flows[key]['Tipo'][Tipo]['hour']

		if entryhour.get(hour) is None:
			entryhour[hour] = {}

		entryflows = entryhour[hour]
		if id == 'MOB':
			colend = Mflows.shape[1]
		else:
			colend = Mflows.shape[1]-1

		for x in range(colhour+1, colend):
			categories = Mflows[0][x]
			if entryflows.get(categories) is None:
				entryflows[categories] = []
			entryflows[categories].append(float(Mflows[i][x]))

	keys = flows.keys()
	#if id == 1:
		#print flows
	for key in keys:
		Types = flows[key]['Tipo'].keys()
		for Type in Types:
			hours = flows[key]['Tipo'][Type]['hour'].keys()
			for hour in hours:
				categories = projection.keys()
				#print categories
				for category in categories:
					#print category,'valor flow', flows[key]['Tipo'][Type]['hour'][hour][category][0], 'valor mult', projection[category], '',  projection[category] * flows[key]['Tipo'][Type]['hour'][hour][category][0]
					mult = projection[category] * flows[key]['Tipo'][Type]['hour'][hour][category][0]
					flows[key]['Tipo'][Type]['hour'][hour][category] = mult

	writeprojections(flows, id, Year)

def writeprojections(data, id, Year):
	#print id
	folder = os.path.join('..', 'data','out', '')
	keys = data.keys()
	
	if id == 'RPM':
		csvsalida = open(folder + 'RPM' + '_' + Year + '.csv', 'w')
		names = ['Estacion','Tipo','IDEstacion','IDNodo', 'hora', '>C5', 'AL', 'AT', 'B', 'BA', 'BT', 'C', 'C2G', 'C2P', 'C3-C4', 'C5', 'ESP', 'INT', 'L', 'M', 'TOTAL']
	
	elif id == 'MOB':
		csvsalida = open(folder + 'MOB' + '_' + Year + '.csv', 'w')
		names1 = ['Estacion', 'Tipo', 'IDEstacion', 'IDNodo', 'hora',]
		
		if ('HABIL' in data[keys[0]]['Tipo']):
			names2 = sorted(data[keys[0]]['Tipo']['HABIL']['hour'][0])
		else: 
			names2 = sorted(data[keys[0]]['Tipo']['NOHAB']['hour'][0])
		names = names1 + names2

	for name in names:
		if name == names[0]:
			csvsalida.write(name)
		else:
			csvsalida.write(',')
			csvsalida.write(name)
	
	csvsalida.write('\n')

	keys = data.keys()
	for key in keys:
		Types = data[key]['Tipo'].keys()
		for Type in Types:
			hours = data[key]['Tipo'][Type]['hour'].keys()
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
				category = sorted(data[key]['Tipo'][Type]['hour'][hour].keys())
				#print category
				#category = sorted(category)
				for cat in category:
					csvsalida.write(',')
					csvsalida.write(str(data[key]['Tipo'][Type]['hour'][hour][cat]))
				#csvsalida.write('0')
				csvsalida.write('\n')
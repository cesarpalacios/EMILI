#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Created by @ceapalaciosal
#Codigo bajo Creative Commons
import sys
sys.path.append("core")
from matriz import *
from wcsv import *
import xlrd
import json


def disolver(flows, category, Year):
	MCategory = convertXLSCSV(category)
	Mflows = convertCSVMatriz(flows)

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
		if value == 'TOTAL': 
			colend = index
		index += 1


	category = {}
	for i in range(1, MCategory.shape[0]):
		flow = MCategory[i][0]
		subflow = MCategory[i][1]

		if category.get(flow) is None: 
			category[flow] = {}
		

		category[flow][subflow] = []
		category[flow][subflow].append(float(MCategory[i][2]))

	#print category
	flows = {}
	for i in range(1, Mflows.shape[0]):
		key = int(Mflows[i][colIDEstation])
		hour = int(Mflows[i][colhour])
		Tipo = Mflows[i][colTipo]

		if flows.get(key) is None: 
			flows[key] = {}
			flows[key]['Tipo'] = {}

		entrytipe = flows[key]['Tipo']
		if entrytipe.get(Tipo) is None:
			entrytipe[Tipo] = {'Estacion': [], 'IDNodo': [], 'hora': {}}
		 

		if flows[key]['Tipo'][Tipo]['Estacion'] == []: 
		 	flows[key]['Tipo'][Tipo]['Estacion'].append(Mflows[i][colEstation])
		 	flows[key]['Tipo'][Tipo]['IDNodo'].append(Mflows[i][colIDNodo])

		entryhour = flows[key]['Tipo'][Tipo]['hora']

		if entryhour.get(hour) is None: 
		 	entryhour[hour] = {'old': {}, 'new':{}}

		entryflows = entryhour[hour]['old']

		for x in range(colhour+1, colend):
			categories = Mflows[0][x]
			if entryflows.get(categories) is None: 
				entryflows[categories] = []
			entryflows[categories].append(float(Mflows[i][x]))

	keys = flows.keys()
	for key in keys: 
		Types =  flows[key]['Tipo'].keys()
		
		for Type in Types: 
			hours = flows[key]['Tipo'][Type]['hora'].keys()
			for hour in hours: 
				categories =  flows[key]['Tipo'][Type]['hora'][hour]['old'].keys()
				for cat in categories:
					#print cat
					subcategory = category[cat].keys()
					#print subcategory
					for subcat in subcategory: 
						flows[key]['Tipo'][Type]['hora'][hour]['new'][subcat] = float(flows[key]['Tipo'][Type]['hora'][hour]['old'][cat][0]) * float(category[cat][subcat][0])

	#print flows
	writedisolver(flows, Year)

	




	

	

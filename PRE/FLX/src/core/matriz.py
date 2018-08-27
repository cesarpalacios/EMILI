# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons

#List Library Import
import csv
import os
import xlrd
import unicodedata
import numpy as np



def convertXLSCSV(direccion):

	direccionexcel = direccion
	workbook = xlrd.open_workbook(direccionexcel)
	all_worksheets = workbook.sheet_names()

	data = workbook.sheet_by_index(0) 
	direccioncsv = direccionexcel + '.csv'
	
	data_emissions = open(''.join([direccioncsv]), 'wb')
	emissions = csv.writer(data_emissions, delimiter=',')

 	for rownum in xrange(data.nrows):
 		emissions.writerow([entry for entry in data.row_values(rownum)])
 	data_emissions.close()
 	matriz = convertCSVMatriz(direccioncsv)
 	return matriz


def convertCSVMatriz(direccioncsv):

	matriz = np.genfromtxt(direccioncsv, delimiter=',', dtype=None)
	return  matriz

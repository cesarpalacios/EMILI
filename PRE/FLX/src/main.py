# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons
import sys
import os
sys.path.append('core')
from clear import *
from ExcelCSV import*
from CSVMatriz import*
from disolver import*
from projection import *

print 'Insert information'
#Year = raw_input('Insert Year Flows: ')
Year = str('2014')
#YearProjection = raw_input('Insert Year Projection: ')
YearProjection = str('2030')


folder = os.path.join('..', 'data','out', '')
clear(folder)

print ('Init process flows')
folder = os.path.join('..', 'data', 'in', 'Flows2', '')

listaExcel (folder)
listaCSV(folder, Year)

flows = os.path.join('..', 'data', 'out', 'RPM' + '_' + Year + '.csv')
category = os.path.join ('..', 'data', 'in','Constants', 'CATEGORY.xlsx')
disolver(flows, category, Year)

#flows = os.path.join('..', 'data', 'out', 'RPM.csv')
projections = os.path.join('..', 'data','in', 'Projection', 'Resuspended_grow_factors.xlsx')
projection(flows, projections, YearProjection , 'RPM')

flows = os.path.join('..', 'data', 'out', 'MOB' + '_' + Year + '.csv')
projections = os.path.join('..', 'data','in', 'Projection', 'Movile_grow_factors.xlsx')
projection(flows, projections,YearProjection , 'MOB')

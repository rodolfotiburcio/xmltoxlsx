from flask import render_template, redirect, url_for, request
from flask import send_file
import os

from app import app
from app.forms import UploadFiles

import glob, os
import xml.etree.ElementTree as ET
import xlsxwriter as XLS
import pandas as pd

def muestra(file):
    '''
    Function to read only the required data from each xml file, only when the taxid 
    is the correct 'IAU1411211Z5', for this company
    '''
    tree = ET.parse(file)
    root = tree.getroot()
    try:
        if root[1].attrib.get('Rfc') == 'IAU1411211Z5' : #change this for other companies
            rfc_valido = 'Correcto'
        else:
            rfc_valido = 'ERROR EN RFC'
        data = {
            '''
            the data to be returned into a excel file
            '''
            'RFC inamex': root[1].attrib.get('Rfc') + ' ' + rfc_valido,
            'Serie-Folio': str(root.attrib.get('Serie')) + '-' + str(root.attrib.get('Folio')),
            'Fecha y hora': root.attrib.get('Fecha'),
            'Uso CFDI': root[1].attrib.get('UsoCFDI'),
            'Forma de pago': root.attrib.get('FormaPago'),
            'Metodo de pago': root.attrib.get('MetodoPago'),
            'Total': root.attrib.get('Total'),
            'Moneda': root.attrib.get('Moneda')
            }
        return data
    except:
        return {
            'RFC inamex': 'Error',
            'Serie-Folio': 'Error',
            'Fecha y hora': 'Error',
            'Uso CFDI': 'Error',
            'Forma de pago': 'Error',
            'Metodo de pago': 'Error',
            'Total': 'Error',
            'Moneda': 'Error'
            }

@app.route('/', methods = ['GET', 'POST'])
def home():
    '''
    Single page app, where files are uploaded and automaticaly download a excel file
    '''
    form = UploadFiles()
    if form.validate_on_submit():
        datos = []
        files = form.files.data
        for file in files:
            datos.append(muestra(file))
        df = pd.DataFrame.from_records(datos)
        print(df)
        html = df.to_html(classes='table table-striped')
        text_file = open("./app/templates/home.html","w")
        text_file.write(html)
        text_file.close()       
        writer = pd.ExcelWriter('Facturas.xlsx', engine='xlsxwriter')
        df.to_excel(writer,sheet_name='Lista de facturas')
        writer.save()
        return send_file('../Facturas.xlsx')
    context = {
        'form':form
    }
    return render_template('upload.html', **context)

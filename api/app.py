from flask import Flask, request, jsonify
import boto3
from boto3.dynamodb.conditions import Attr

app = Flask(__name__)

# Conexión a la base de datos
db = boto3.resource('dynamodb', region_name='us-east-1')
tabla = db.Table('proy-medidas')

# Función auxiliar para no repetir código
def buscar(mes, anio):
    filtro = Attr('Mes').eq(int(mes)) & Attr('Año').eq(int(anio))
    return tabla.scan(FilterExpression=filtro)['Items']

@app.route('/')
def inicio():
    return "<h1>Servidor Web Activo</h1>"

# Temperatura Media (/temp)
@app.route('/temp')
def media():
    m = request.args.get('month')
    a = request.args.get('year')

    datos = buscar(m, a)
    if len(datos) == 0:
        return "No hay datos"

    suma = 0
    for d in datos:
        suma += float(d['MediaSemanal'])

    promedio = suma / len(datos)
    return jsonify({'valor': promedio})

# Desviación Máxima (/sd)
@app.route('/sd')
def desviacion():
    m = request.args.get('month')
    a = request.args.get('year')

    datos = buscar(m, a)

    maximo = 0
    for d in datos:
        valor = float(d['DesviacionSemanal'])
        if valor > maximo:
            maximo = valor

    return jsonify({'valor': maximo})

# Diferencia con mes anterior (/maxdiff)
@app.route('/maxdiff')
def diferencia():
    m = int(request.args.get('month'))
    a = int(request.args.get('year'))

    # Máximo de este mes
    datos_hoy = buscar(m, a)
    max_hoy = 0
    for d in datos_hoy:
        if float(d['MediaSemanal']) > max_hoy:
            max_hoy = float(d['MediaSemanal'])

    # Mes anterior
    if m == 1:
        m_ant, a_ant = 12, a - 1
    else:
        m_ant, a_ant = m - 1, a

    datos_ant = buscar(m_ant, a_ant)
    max_ant = 0
    for d in datos_ant:
        if float(d['MediaSemanal']) > max_ant:
            max_ant = float(d['MediaSemanal'])

    resultado = max_hoy - max_ant
    return jsonify({'valor': resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

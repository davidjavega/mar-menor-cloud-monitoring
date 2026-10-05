import json
import urllib.parse
import boto3
import csv
from datetime import datetime
from decimal import Decimal

# Recursos de AWS
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# Tabla de DynamoDB donde guardaremos los datos semanales
temperatura_table = dynamodb.Table('proy-medidas')

def lambda_handler(event, context):

    print("Evento recibido por la función Lambda:")
    print(json.dumps(event, indent=2, ensure_ascii=False))

    # Obtener bucket y key del objeto subido a S3
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )

    # Fichero temporal donde se descargará el CSV en la Lambda
    local_filename = '/tmp/proy-datos_semanales.csv'

    # Descargar el fichero desde S3
    try:
        s3.meta.client.download_file(bucket, key, local_filename)
        print(f"Fichero descargado de S3: s3://{bucket}/{key} -> {local_filename}")
    except Exception as e:
        print(e)
        print(
            f'Error obteniendo el objeto {key} del bucket {bucket}. '
            'Comprueba que existen y que están en la misma región que la función.'
        )
        raise e

    # Leer el CSV y escribir cada fila en DynamoDB
    row_count = 0

    with open(local_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')

        for row in reader:
            row_count += 1

            try:
                fecha_str = row['Fecha']     
                media = float(row['Medias'])
                sd  = float(row['Desviaciones'])

                # Extraer mes y año de la fecha (para las estadísticas mensuales)
                fecha_dt = datetime.strptime(fecha_str, '%Y/%m/%d')
                año = fecha_dt.year
                mes = fecha_dt.month 

                # Alerta de desviación
                alerta_desviacion = sd > 0.5

                if alerta_desviacion:
                    message = f"Alerta de desviación en la fecha {fecha_str}: {sd}"
                    print(message)
                    sns = boto3.client('sns')
                    alertTopic = "proy-alerta"
                    snsTopicArn = [t['TopicArn'] for t in sns.list_topics()['Topics'] if t['TopicArn'].lower().endswith(':' + alertTopic.lower())][0]
                    sns.publish(
                        TopicArn=snsTopicArn, 
                        Message=message, 
                        Subject='Alerta de desviación',
                        MessageStructure='string'
                        )

                # Item que insertaremos en DynamoDB
                item = {
                    'Fecha': fecha_str,              # PK de la tabla
                    'MediaSemanal': Decimal(str(media)),           # temperatura media de la semana
                    'DesviacionSemanal': Decimal(str(sd)), # desviación estándar de la semana
                    'Año': año,                    
                    'Mes': mes,
                    'AlertaDesviacion': alerta_desviacion
                }

                # Insertar en DynamoDB
                temperatura_table.put_item(Item=item)


            except Exception as e:
                print(f"Error en la Fila {row_count} ---")
                print(f"Error: {e}")
                
                raise e

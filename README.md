# Mar Menor Cloud Monitoring

## Descripción

Proyecto cloud desarrollado en AWS para el procesamiento, almacenamiento y consulta de datos de temperatura del Mar Menor.

La solución implementa un pipeline de datos automatizado, un sistema de alertas y una API REST contenerizada. La aplicación se despliega mediante Amazon ECS y utiliza un balanceador de carga para distribuir las peticiones entre las tareas del servicio.

<img width="878" height="836" alt="image" src="https://github.com/user-attachments/assets/6bcc14e5-694d-4891-ac7f-dd95f0c733dc" />


## Arquitectura

El sistema se divide en los siguientes bloques:

### 1. Pipeline de datos

- Ingesta de archivos CSV mediante **Amazon S3**.
- Procesamiento automático de los datos con **AWS Lambda**.
- Almacenamiento de los resultados en **Amazon DynamoDB**.
- Generación de alertas mediante **Amazon SNS** cuando la desviación estándar supera el umbral establecido.

### 2. API REST

- API desarrollada con **Flask**.
- Consulta de los datos almacenados en DynamoDB mediante **Boto3**.
- Endpoints para obtener métricas de temperatura y desviación.
- Contenerización de la aplicación mediante **Docker**.
- Almacenamiento de la imagen del contenedor en **Amazon ECR**.

### 3. Infraestructura

- **VPC** con dos subredes públicas.
- **Internet Gateway** para proporcionar conectividad exterior.
- **Amazon ECS** para el despliegue de la aplicación.
- **Application Load Balancer** para distribuir el tráfico.
- Grupos de seguridad para controlar el acceso entre los distintos componentes.
- Infraestructura base definida mediante **AWS CloudFormation**.

### 4. Disponibilidad y escalabilidad

- Servicio ECS configurado con varias tareas.
- Despliegue distribuido entre dos zonas de disponibilidad.
- Balanceo de carga entre las instancias del servicio.
- Configuración del clúster con capacidad mínima y máxima para adaptarse a la carga.

## API

La aplicación permite realizar las siguientes consultas:

- `/temp` — temperatura media para un mes y año.
- `/sd` — desviación máxima registrada.
- `/maxdiff` — diferencia respecto al mes anterior.

## Tecnologías utilizadas

- **Python**
- **Flask**
- **Boto3**
- **Docker**
- **Amazon S3**
- **AWS Lambda**
- **Amazon DynamoDB**
- **Amazon SNS**
- **Amazon EC2**
- **Amazon ECR**
- **Amazon ECS**
- **Application Load Balancer**
- **AWS CloudFormation**

## Contexto académico

Proyecto realizado para la asignatura **Infraestructura para la Computación de Altas Prestaciones** del Grado en Ciencia e Ingeniería de Datos de la Universidad Politécnica de Cartagena.

Curso 2025/2026.

Proyecto desarrollado en un equipo de tres estudiantes.

import boto3
import uuid

bucketName= 'pruebas-sw'
# Let's use Amazon S3
s3 = boto3.resource('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')


# data = open("img/prueba1.jpg",'rb')
# s3.Bucket(bucketName).put_object(Key='prueba1.jpg', Body=data)
# x = input('presione cualquier tecla para continuar')

def uploadFile(nombreBucket,ruta):
    data = open(ruta,'rb')
    id= uuid.uuid4()
    s3.Bucket(nombreBucket).put_object(Key=f'{id}.jpg', Body=data)
    print(f'imagen: {ruta} , subida exitosamente')
    return f'{id}.jpg'

def detectarTexto(ruta, precision):
    with open(ruta,'rb') as source_image:
        source_bytes =  source_image.read()
    
    response = rekognition.detect_text(Image={'Bytes': source_bytes})

    textDetections = response['TextDetections']
    texto = ''
    # print('Detectado------------')
    # for text in textDetections:
    #     print ('Detected text:' + text['DetectedText'])
    #     print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
    #     print ('Id: {}'.format(text['Id']))
    #     if 'ParentId' in text:
    #         print ('Parent Id: {}'.format(text['ParentId']))
    #     print ('Type:' + text['Type'])
    #     print()

    for text in textDetections:
        if text['Confidence'] > precision:
            if text['Type'] == 'LINE':
                texto+= text['DetectedText']+ ' '

    return texto.lower()
# def extraerTexto(response):

control = 'test.png'
precision = 900.0
texto_control = detectarTexto('img/test.png', 92.00)
def menu(control,precision):
    print("Bienvenido, aca podras comparar el texto de una imagen con otras\n")
    print('Ingresa una opcion:')
    print('1. Ingresar imagen de control y su precision. Por defecto es test.png con precision del 90')
    print('2. Comparar imagen de control con otra')
    print('3. Salir')
    while True:
        try:
            select = int(input('Ingrese opcion: '))
            if select == 1:
                control = input('Ingrese el nombre de la imagen y su extension: ')
                precision = float(input('Ingrese la precision minima para las palabras: '))

            elif select == 2:
                imagen = input('Ingrese el nombre de la imagen a comprar con la de control: ')
                texto_imagen = detectarTexto('img/'+imagen, precision)
                if texto_imagen == texto_control:
                    print('el texto es el mismo en ambas imagenes')
                else:
                    print('el texto es diferente')

                print(f"texto imagen control: {texto_control}")
                print(f"texto imagen: {texto_imagen}")
                
            elif select == 3:
                break
            else:
                print('El valor ingresado no es valido, ingrese 1 o 2')
        except ValueError:
            print('El valor ingresado no es valido, ingrese 1 o 2')

print(menu(control,precision))

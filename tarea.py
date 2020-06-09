import boto3
from os import listdir, system
from os.path import isfile, join
import datetime

rekognition = boto3.client('rekognition', region_name='us-east-1')

# 
def detectarTexto(ruta, precision):
    """ Transforma una imagen en un texto, solo aceptar
    
    """
    with open(ruta,'rb') as source_image:
        source_bytes =  source_image.read()
    
    response = rekognition.detect_text(Image={'Bytes': source_bytes})

    textDetections = response['TextDetections']
    texto = ''

    for text in textDetections:
        if text['Confidence'] > precision:
            if text['Type'] == 'LINE':
                texto+=text['DetectedText'].lower() + ' '

    return texto.strip()

def printMenu(nombreImagenControl, precisionMinima):
    system('cls')
    texto = """
    Bienvenido:
    Aca podrás comparar si imágenes contienen el mismo texto, las imágenes deben estar en la carpeta 'img', selecciona una opción:

    Imagen de control actual: {}
    Precisión: {}

    1. Seleccionar imagen de control
    2. Configurar la precisión mínima de AWS rekognition, para que una palabra sea detectada
    3. Ver texto de imagen de control(Se mostrará el texto en minúsculas)
    4. Comparar otras imagenes
    5. Salir

    """.format(nombreImagenControl, precisionMinima)

    print(texto)

textoTerceraOpcion = """
Escriba el nombre de una imagen y su extension. Ejemplo: "imagen1.jpg" o puede utilizar '*' para seleccionarlas todas

Ingrese nombre: """

def EscribirLog(fecha, nombreImagenControl, textoImagenControl, nombreImagenPrueba, textoImagenPrueba, Resultado):
    file = open('logImagenes.txt','a')
    file.write("""Fecha: {}        
ImagenControl: {}
textoControl: {}
ImagenPrueba: {}
textoPrueba: {}

Resultado: {}

------------------------------------------------

""".format(fecha, nombreImagenControl, textoImagenControl, nombreImagenPrueba, textoImagenPrueba, Resultado))
    file.close()

## Este es el supuesto mas importante, el texto de la imagen de prueba debe estar en el mismo orden que en el de control, de lo contrario sera falso
def compararTextos(textoControl, textoPrueba):  
    return textoPrueba in textoControl

def menu(nombreImagenControl, precisionMinima):
    printMenu(nombreImagenControl, precisionMinima)
    while True:
        try:
            select = int(input('Ingrese opcion: '))
            if select == 1:
                nombreImagenControl = input('Ingrese el nombre de la imagen y su extension: ')
                printMenu(nombreImagenControl, precisionMinima)
            
            elif select == 2:
                precisionMinima = float(input('Ingrese la precision minima para las palabras: '))
                printMenu(nombreImagenControl, precisionMinima)

            elif select == 3:
                texto_imagen = detectarTexto('img/'+nombreImagenControl, precisionMinima)
                print(f'Texto de la imagen de control: \'{texto_imagen}\'')
            
            elif select == 4:
                entrada =  input(textoTerceraOpcion).strip()
                textoImagenControl = detectarTexto('img/'+nombreImagenControl, precisionMinima)
                
                while True:
                    if entrada == '*':
                        nombresImagenes = [f for f in listdir('img/') if isfile(join('img/', f))] # una lista con todos los nombres de los archivos

                        for nombreImagenPrueba in nombresImagenes:
                            textoImagenPrueba = detectarTexto('img/'+nombreImagenPrueba, precisionMinima)
                            Resultado = compararTextos(textoImagenControl,textoImagenPrueba)
                            hora = str(datetime.datetime.now())

                            EscribirLog(hora, nombreImagenControl, textoImagenControl, nombreImagenPrueba, textoImagenPrueba, Resultado)

                            print(f'{nombreImagenControl} -> {nombreImagenPrueba} = {Resultado}')
                        break
                    
                    else:
                        try:
                            textoImagenPrueba = detectarTexto('img/'+entrada, precisionMinima)
                            Resultado = compararTextos(textoImagenControl,textoImagenPrueba)
                            hora = str(datetime.datetime.now())

                            EscribirLog(hora, nombreImagenControl, textoImagenControl, entrada, textoImagenPrueba, Resultado)

                            print(f'{nombreImagenControl} -> {entrada} = {Resultado}')
                            break
                        except:
                            print('Ingrese un nombre de imagen de prueba válido\n')
                            entrada =  input('Ingrese nombre: ').strip()
                        

                input('Presione enter para volver al menu principal')
                printMenu(nombreImagenControl, precisionMinima)
                
            elif select == 5:
                break
            else:
                print('El valor ingresado no es valido')
        except ValueError:
            print('El valor ingresado no es valido')

def main():
    control = 'test.png'
    precision = 97.0

    menu(control, precision)

if __name__ == "__main__":
    main()
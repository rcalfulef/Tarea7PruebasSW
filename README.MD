# Hecho por Andres Calfulef

Instalacion de librerias:

Recomiendo utilizar pipenv para crear un entorno virtual, realice los siguientes pasos:

1. pip install pipenv (esto instala pipenv)
2. pipenv shell (se activa el entorno virtual)
3. pipenv install (para que se instalen las librerias a utilizar)
4. py tarea.py


Credenciales:
    Es necesario utilizar credenciales que tengan acceso a Rekognition. Estas deben estar guardadas en ~/.aws/credentials


Consideraciones:

La imagen de it's monday but keep smiling se llama 'test.png'

Para que el texto de una imagen de prueba se considere dentro de la imagen de control debe ocurrir lo siguente:
- Los textos son insensibles a mayusculas y minusculas.         
        (HolA,hola)     -> True
- Si los textos contienen simbolos estos deben ser los mismos   
        (Hola!,hola)    -> False
        (HolA!,hola!)   -> True
- El texto de la imagen de control debe estar en el mismo orden en la imagen de prueba
        (hola como estas, como estas)   -> True
        (hola como estas, estas como)   -> False

import  matplotlib.pyplot as plt
import os
import cv2
# Datos de ejemplo
dataset = [[1, [{'CALM': 98.2421875}], [(19, 23)], [{'Male': 97.80467987060547}], ['(20-32)']], [1, [{'CALM': 100.0}], [(18, 22)], [{'Male': 99.99887084960938}], ['(20-32)']], [1, [{'CALM': 99.8046875}], [(19, 25)], [{'Male': 99.63265991210938}], ['(20-32)']], [1, [{'CALM': 100.0}], [(18, 22)], [{'Male': 99.95218658447266}], ['(20-32)']], [1, [{'CALM': 98.828125}], [(19, 23)], [{'Male': 98.44634246826172}], ['(20-32)']], [1, [{'CALM': 92.48046875}], [(19, 23)], [{'Male': 99.67190551757812}], ['(20-32)']], [1, [{'CALM': 98.6328125}], [(19, 23)], [{'Male': 97.6740493774414}], ['(20-32)']], [1, [{'CALM': 99.609375}], [(19, 23)], [{'Male': 99.92989349365234}], ['(20-32)']], [1, [{'CALM': 99.8046875}], [(19, 23)], [{'Male': 99.70756530761719}], ['(20-32)']], [1, [{'CALM': 99.4140625}], [(18, 22)], [{'Male': 99.88824462890625}], ['(20-32)']], [1, [{'CALM': 97.0703125}], [(19, 27)], [{'Male': 99.82593536376953}], ['(20-32)']], [1, [{'CALM': 100.0}], [(19, 23)], [{'Male': 99.99237060546875}], ['(20-32)']], [1, [{'CALM': 98.6328125}], [(18, 22)], [{'Male': 99.97943878173828}], ['(20-32)']], [1, [{'CALM': 98.6328125}], [(19, 23)], [{'Male': 99.9327163696289}], ['(20-32)']], [1, [{'CALM': 99.609375}], [(18, 22)], [{'Male': 99.83551025390625}], ['(20-32)']], [1, [{'CALM': 100.0}], [(19, 23)], [{'Male': 99.99946594238281}], ['(20-32)']]]


#Seccion de recostruccion
def recostruccion_video():
    imagenes=os.listdir('Images')
    video_salida = 'static/video/video_salida.avi'

    primera_imagen = cv2.imread(os.path.join('Images', imagenes[0]))
    altura, ancho, _ = primera_imagen.shape




    # Crear el objeto VideoWriter
    video_writer = cv2.VideoWriter(video_salida, cv2.VideoWriter_fourcc(*'XVID'), 1, (ancho, altura))

    # Recorrer la lista de archivos y agregar cada imagen al video
    for nombre_archivo in imagenes:
        ruta_imagen = os.path.join("Images", nombre_archivo)
        imagen = cv2.imread(ruta_imagen)
        #redimensionar

        video_writer.write(imagen)
        print(ruta_imagen)
    # Liberar el objeto VideoWriter
    video_writer.release()


#SEccion de analisis
class analisis:
    def Transformacion_datos(datos):
        categoria = list(set(datos))
        valor =[]
        for datox in categoria:
            count =0
            for datoy in datos:
                if datox == datoy:
                    count +=1
            valor +=[count]

        return categoria,valor
            
            

    def main(dict_predict):
        #Listas
        genero =[]
        estado=[]
        rango_edad =[]
        edades = []

        #Division de datos
        for lista in dict_predict:
            estado +=[list(lista[1][0].keys())[0]]
            genero +=[list(lista[3][0].keys())[0]]
            rango_edad +=[lista[2][0]]
            edades +=[lista[4][0]]

        #Analisis
        analisis.Pie_estado(estado)
        analisis.Bar_edades(edades)
    
    def Pie_estado(emociones):
        #Configurar los datos
        categorias,valores = analisis.Transformacion_datos(emociones)
        
        fig,ax=plt.subplots()
        ax.pie(valores,labels=categorias)
        fig.savefig('static/predicciones/Pie_estados.png', bbox_inches='tight')

    def Bar_edades(edades):
        #Configurar los datos
        categorias,valores = analisis.Transformacion_datos(edades)

        fig,ax=plt.subplots()
        ax.bar(height=valores,x=categorias)
        fig.savefig('static/predicciones/Bar_edades.png', bbox_inches='tight')        
    
# analisis.main(dataset)

        
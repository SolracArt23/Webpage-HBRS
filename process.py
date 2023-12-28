import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import boto3
from PIL import Image
from Analisis import analisis,recostruccion_video
from comparador import Comparar

#Cargue de claves
from dotenv import load_dotenv


def Lectura_archivo():
    for general,_,files in os.walk('Grabaciones'):
        video_analisis = files[0]
    resultado_view=view_video(general+'/'+video_analisis)
    return resultado_view

#funcion para guardar imagen
def Save_img(array_img,count):
    try:
        array_img_rgb = cv2.cvtColor(array_img, cv2.COLOR_BGR2RGB)
        array_img_rgb =cv2.resize(array_img_rgb,(225,225))
        imagen_pil = Image.fromarray(array_img_rgb)
        imagen_pil.save(f'Images/imagen_{count}.jpg')

    except:pass
    return 

#Funcion de limpieza de los datos
class Extract_information:

    def emotion_func(edades):
        Emotions=[[emotion['Confidence'],emotion['Type']]for emotion in edades]

        emocion_prob =0
        emocion_mayor = ''
        for emocion in Emotions:
            if emocion_prob< emocion[0]:
                emocion_prob = emocion[0]
                emocion_mayor = emocion[1]

        return {emocion_mayor:emocion_prob}

    def Age_range(rangeEdades):
        AgeRange=rangeEdades['AgeRange']
        agerange ='('+str(AgeRange['Low'])+'-'+str(AgeRange['High'])+')'
        return AgeRange['Low'],AgeRange['High']

    def Gender(genero):
        a=list(genero.values())
        b={a[0]:a[-1]}
        return b

    def Seccion_edades(edades):
        mayor_edad = edades['High']
        lista_edades = {13:'(0-13)',19:'(14-19)',32:'(20-32)',42:'(33-42)',62:"(43-62)",100:"(63-100)"}

        for l  in lista_edades:
            if mayor_edad <= l:
                result= lista_edades[l]
                break

        return result

    def Main(dict_data):
        #variables
        emocion=[]
        rango_edades=[]
        genero=[]
        seccion_edades=[]
        #extraccion de emociones
        ids = len([x for x in dict_data['FaceDetails']])
        if ids ==0:
            return 0
        for x in range(ids):
            emocion += [Extract_information.emotion_func(dict_data['FaceDetails'][x]['Emotions'])]
            rango_edades += [Extract_information.Age_range(dict_data['FaceDetails'][x])]
            genero += [Extract_information.Gender(dict_data['FaceDetails'][x]['Gender'])]
            seccion_edades += [Extract_information.Seccion_edades(dict_data['FaceDetails'][x]['AgeRange'])]

        return ids,emocion,rango_edades,genero,seccion_edades

#funcion del bondingbox
def faceBox(faceNet, frame,indice=0.7):
    frameWidth=frame.shape[1]
    frameHeight=frame.shape[0]
    blob = cv2.dnn.blobFromImage(frame, 1.0,(227,227), [104,117,223], swapRB =False)
    faceNet.setInput(blob)
    detection = faceNet.forward()
    bboxs=[]
    ids=[]
    for i in range(detection.shape[2]):
        confidence=detection[0,0,i,2]
        if confidence>indice:
            x1=int(detection[0,0,i,3]*frameWidth)
            y1=int(detection[0,0,i,4]*frameHeight)
            x2=int(detection[0,0,i,5]*frameWidth)
            y2=int(detection[0,0,i,6]*frameHeight)
            bboxs.append([x1,y1,x2,y2])
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),1)
            ids.append(i)
    return frame, bboxs,ids

def view_video(source):
    # Seccion del modelo
    faceProto = "models/opencv_face_detector.pbtxt"
    faceModel = "models/opencv_face_detector_uint8.pb"
    faceNet=cv2.dnn.readNet(faceModel, faceProto)
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    padding=10

    origen =0
    destino = 0


    #Seccion del video
    captura = cv2.VideoCapture(source)
    video = []
    contador=0
    while (captura.isOpened()):

        ret, imagen = captura.read()
        if ret == True:
            #Redimencionar imagen
            imagen = cv2.resize(imagen,(500,500))
            #detectar las caras
            frame,bboxs,ids=faceBox(faceNet,imagen,0.6)

            if contador ==3:
                for bbox in bboxs:
                    face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]
                    video +=[np.array(face)]

                contador = 0
                    
            cv2.imshow('video', imagen)
            
            if cv2.waitKey(30) == ord('s'): #or len(video) >=50:
                break

        else: break
        contador +=1

    captura.release()
    cv2.destroyAllWindows()

    for x in range(len(video)):        
        Save_img(video[x],x)
    
    #Comparar imagenes
    Comparar()
    
    #Predecir
    response=Send_AWS()
    # print(f"Respuesta de process: {response}")

    #Simulacion
    # response=Send_AWS_simulacion()
    recostruccion_video()

    return response


def Send_AWS_simulacion():
    Respuesta =[[2, ['CALM'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Female'], ['(40-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']],[1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']], [1, ['SURPRISED'], [(18, 22)], ['Male'], ['(20-32)']]]
    return  Respuesta




def Send_AWS():
    lista_image = [image  for _,_,images in os.walk('Images') for image in images]
    print(len(lista_image))
    
    # prediccion=np.random.randint(len(lista_image),size=20)
    # lista_image = [lista_image[x]  for x in prediccion]
    # print(lista_image)

    load_dotenv()
    access_key_id = os.getenv('ACCESS_KEY')
    secret_access_key =os.getenv('SECRET_KEY')   

    dataset=[]
    client = boto3.client('rekognition',
                        aws_access_key_id=access_key_id,
                        aws_secret_access_key=secret_access_key,
                        region_name='us-east-1')

    #prediccion del modelo por imagen
    for img in lista_image:
        print(f'Se predijo esta imagen: {img}')
        # db= MySQLdb.connect(host="208.109.225.208",user='hbrs_user',password='Mldu.zAu2ruN',port=3306,database='hbrs_bd')
        # cursor = db.cursor()
        with open(f'Images/{img}', 'rb') as image_file:
            image_bytes = image_file.read()
        # Detectar caras en la imagen
        response = client.detect_faces(
            Image={
                'Bytes': image_bytes
            },
            Attributes=['AGE_RANGE','GENDER','EMOTIONS']
        )
        #mostrar resultados
        try:
            numero_personas,emocion,rango_edades,genero,seccion_edades = Extract_information.Main(response)
            # Desempaqueta las emociones
            emocion_nombre = []
            emocion_confianza = []
            for emoction in emocion:
                for key, value in emoction.items():
                    emocion_nombre += [key]
                    emocion_confianza += [value]
                    break 
                # Desempaqueta los géneros
            genero_nombre = []
            genero_confianza = []
            for gender in genero:
                for key, value in gender.items():
                    genero_nombre += [key]
                    genero_confianza += [value]
                    break  

            dataset +=[[numero_personas,emocion_nombre,rango_edades,genero_nombre,seccion_edades]]
        except:
            print("no se encontro cara")    

    #seccion de analisis
    print(dataset)
    # analisis.main(dataset)
    return dataset

    #Seccion de recostruccion del video

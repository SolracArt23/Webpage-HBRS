import os
from dotenv import load_dotenv



def Comparar():
    #CArgar las imagenes guardadas
    Por_eliminar = []
    video =[]
    for general_path,_,files in os.walk('Images'):
        for img in files:
            video.append(general_path+'/'+img)

     #Comparar imagenes
    for x in range(len(video)):
        for y in range(x+1,len(video)):
            try:
                compare_images(video[x],video[y])
            except:pass

def compare_faces(url_img_compare_1, url_img_compare_2):
    
    bytes_1 = byte_for_img(url_img_compare_1)
    bytes_2 = byte_for_img(url_img_compare_2)
    load_dotenv()
    access_key_id = os.getenv('ACCESS_KEY')
    secret_access_key = os.getenv('SECRET_KEY')
    client = boto3.client('rekognition',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key,
                          region_name='us-east-1')

    try: 
        answer = client.compare_faces(SourceImage={'Bytes': bytes_1},
                                      TargetImage={'Bytes': bytes_2})
        if 'FaceMatches' in answer:
            for match in answer['FaceMatches']:
                confidence = match['Face']['Confidence']
                similarity = match['Similarity']
                print(f'img: {url_img_compare_1} Confidence: {confidence}, Similarity: {similarity} with img: {url_img_compare_2}')

                os.remove(url_img_compare_1)

                return True

        if 'UnmatchedFaces' in answer:
                print(answer)

    except:
        return


import cv2

def compare_images(image1_path, image2_path):
    # Lee las imágenes
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Convierte las imágenes a escala de grises
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Calcula los histogramas de las imágenes en escala de grises
    hist_image1 = cv2.calcHist([gray_image1], [0], None, [256], [0, 256])
    hist_image2 = cv2.calcHist([gray_image2], [0], None, [256], [0, 256])

    # Compara los histogramas utilizando la distancia de Bhattacharyya
    similarity = cv2.compareHist(hist_image1, hist_image2, cv2.HISTCMP_BHATTACHARYYA)

    # Muestra la similitud entre las imágenes
    print(f"Similitud entre las imágenes: {similarity}")

    # Puedes ajustar un umbral según tus necesidades
    threshold = 0.2
    if similarity < threshold:
        print("Las imágenes son muy similares.")
        os.remove(image1_path)
        # return image2_path


    else:
        print("Las imágenes no son muy similares.")
        result=compare_faces(image1_path, image2_path)

# # Rutas de las imágenes que quieres comparar
# image1_path = "Images/imagen_14.jpg"
# image2_path = "Images/imagen_6.jpg"

# # Llama a la función para comparar las imágenes
# compare_images(image1_path, image2_path)


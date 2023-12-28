from flask import Flask,render_template,Response,url_for,request,jsonify
from werkzeug.utils import secure_filename
import os
import threading
from process import Lectura_archivo
import MySQLdb
#Creacion de backend
app = Flask(__name__)
# db = MySQLdb.connect(host='bydeylrhwrudhbj5hdcf-mysql.services.clever-cloud.com',user='uhrl7ap9vhtyrlt1',password='v3YUJacwoyGiiuabmO9x',port=3306,database='hbrs_from')

#configurar la carpeta de gravaciones
app.config['Grabaciones'] = 'Grabaciones'


@app.route('/')
def MainPage():
    print(url_for('static', filename='video/video_salida.mp4'))
    return render_template('index.html')

#Formulario
@app.route('/from',methods=['POST'])
def Formulario():
    print(request.form.nombre)
    # cursor = db.cursor()
 



# Funcion de subida de archivos
@app.route('/Guardar_archivo',methods=['POST'])
def Guardar_archivo():
    #detectar archivo
    print(request.files)
    if 'file' in request.files:
        file = request.files['file']
        #Por posibles errores
        if file.filename =='':
            return 'no se cargo el archivo correctamente'
        
        #Limpiar carpetas
        for _,_,images in os.walk('Grabaciones'):
            for image in images:
                os.remove('Grabaciones/'+image)

        for _,_,images in os.walk('Images'):
            for image in images:
                os.remove('Images/'+image)

        #Guardar el archivo
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['Grabaciones'],filename))

        result=Lectura_archivo()
        print(result)

        return result

    return None

#ejecucion de servidor 
if __name__ == '__main__':
    app.run('0.0.0.0',port=8081,debug=True)
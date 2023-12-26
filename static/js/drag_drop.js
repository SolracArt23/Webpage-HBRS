// Creacion de funcion de drag and drop

$(document).ready(function(){

    // Cunadoa agarras un documento
    $('#drop-area').on('dragenter dragover',function(e){
        e.preventDefault();
        $(this).css('background-color','#e9e9e9');

    });
    // Cunado lo sueltas
    $('#drop-area').on('dragleave',function(e){
        e.preventDefault();
        $(this).css('background-color','white');    
    });
    // Cuando se pone encima de drag
    $('#drop-area').on('drop',function(e){
        e.preventDefault();
        $(this).css('background-color','white');
        var files = e.originalEvent.dataTransfer.files;
        //Detectar si es un mp4
        if (files[0].type == 'video/mp4' || files[0].type == 'video/mp3'|| files[0].type == 'video/webm' || files[0].type == 'video/x-matroska'){

            //Encio del archivo
            formData = new FormData();
            formData.append('file',files[0]);
            fetch('/Guardar_archivo',{
                method:'POST',
                body:formData
            }).then(response => response.text())
            .then( data =>{
                document.getElementById('text-drop').textContent = "Se leyo el documento correctamente";


                //Crear la tabla de respuesta
                console.log(data)
                const array = JSON.parse(data)
                
                for (const [rango,emocion, rangoEdad, genero, edad] of array) {
                insertarDatos(emocion, rangoEdad, genero, edad);
                }
                  

            }).catch(error =>{
                console.log('Error',error)
            })

        }
        else{

            document.getElementById('text-drop').textContent = 'Archivo invalido';
        }

        // console.log(files);
        
    });
    $('#drop-area').on('click',function(e){
        $('#file-input').click();

    });
    $('#file-input').on('change', function() {
        var files = $(this)[0].files;
        // handleFiles(files);
        console.log(file.name);
    });
    

})

function insertarDatos(emocion, rangoEdad, genero, edad) {
    const tabla = document.getElementById("Tabla_resultados");
    const fila = tabla.insertRow();
    const celdaEmocion = fila.insertCell();
    const celdaRangoEdad = fila.insertCell();
    const celdaGenero = fila.insertCell();
    const celdaEdad = fila.insertCell();
    celdaEmocion.innerHTML = emocion;
    celdaRangoEdad.innerHTML = rangoEdad[0];
    celdaGenero.innerHTML = genero;
    celdaEdad.innerHTML = edad;
  }
  


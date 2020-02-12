#Selecciono imagen base
FROM python:3.6

#Creo directorio de trabajo y me paro en el
WORKDIR /usr/src/app

#Copio el archivo con los nombres de las librerias python necesarias
COPY docker-requirements.txt ./

#Ejecuto el comando pip install para instalar las librerias desde el archivo recien copiado
RUN pip install -r docker-requirements.txt

#Copio los archivos necesarios para que mi aplicacion corra
COPY config.yml ./
COPY peyalookerapi.py ./
COPY peyaredshift.py ./
COPY api.py ./

#Recuerdo que debo exponer el puerto ...
EXPOSE 5987

#Comando para ejecutar la api
CMD ["python","api.py"]

#Docker
# Para hacer el build:
# sudo docker build -t peyabi/looker . --rm
# Para ejecutar el contenedor:
# sudo docker run -d -ti -p 5987:5987 peyabi/looker

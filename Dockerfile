FROM python:3.6

WORKDIR /usr/src/app

COPY docker-requirements.txt ./

RUN pip install -r docker-requirements.txt

COPY config.yml ./
COPY peyalookerapi.py ./
COPY peyaredshift.py ./
COPY api.py ./

EXPOSE 5000

CMD ["python","api.py"]



# docker run -ti -p 5099:5000 lookerapi
# docker build -t lookerapi . --rm
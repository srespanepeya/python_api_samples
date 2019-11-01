FROM python:3.6

WORKDIR /usr/src/app

COPY docker-requirements.txt ./

RUN pip install -r docker-requirements.txt

COPY config.yml ./
COPY peyalookerapi.py ./
COPY api.py ./

EXPOSE 5000

CMD ["python","api.py"]
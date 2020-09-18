FROM python:3.7

COPY ./app /app

COPY ./meo_client /meo_client

WORKDIR /meo_client

RUN python setup.py install

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

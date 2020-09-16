FROM python:3.7

COPY requirements.txt ./

RUN pip install -r requirements.txt

EXPOSE 80

COPY ./app /app

WORKDIR /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

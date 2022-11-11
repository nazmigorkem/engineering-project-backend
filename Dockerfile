FROM python:3.10.8-alpine

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 5000

WORKDIR /app/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]

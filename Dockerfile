FROM python:3.9-buster@sha256:bae5b428ebf32d01a902718b0a58874cbf33d7a4b6a65b7cd7b21d48b0d2e2f1

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY amazon_dogs/ amazon_dogs/
COPY main.py .

CMD ["python", "main.py"]

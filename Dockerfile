FROM python:3.11-buster@sha256:3a19b4d6ce4402d11bb19aa11416e4a262a60a57707a5cda5787a81285df2666

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY amazon_dogs/ amazon_dogs/
COPY main.py .

CMD ["python", "main.py"]

FROM python:3.9-buster

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY amazon_dogs/ amazon_dogs/
COPY main.py .

CMD ["python", "main.py"]

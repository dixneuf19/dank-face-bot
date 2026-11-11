FROM python:3.15-slim@sha256:65a65fc7b30b06cb6df4930fd4650697cb23f4c2698ab81fc87e4b031bc36928

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY amazon_dogs/ amazon_dogs/
COPY main.py .

CMD ["python", "main.py"]

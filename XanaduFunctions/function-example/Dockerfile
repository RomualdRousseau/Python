FROM romualdrousseau/python:3
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD python ./main.py

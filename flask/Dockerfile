FROM python:alpine
WORKDIR /app

COPY app.py .
COPY random_heads_tails.py .
COPY random_top_analyze.py .

COPY requirements.txt .

COPY ./templates/index.html ./templates/index.html
COPY ./templates/index.html ./templates/about.html
COPY ./templates/index.html ./templates/random_heads_tails.html
COPY ./templates/index.html ./templates/random_top_analyze.html
COPY ./static/styles.css ./static/styles.css

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=370112"]
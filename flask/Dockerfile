FROM python:alpine

WORKDIR /app

COPY app.py .
COPY random_heads_tails.py .
COPY random_top_analyze.py .
COPY japanese_name_generator.py .
COPY requirements.txt .
COPY ./templates/index.html ./templates/index.html
COPY ./templates/about.html ./templates/about.html
COPY ./templates/random_heads_tails.html ./templates/random_heads_tails.html
COPY ./templates/random_top_analyze.html ./templates/random_top_analyze.html
COPY ./templates/random_japanese_names.html ./templates/random_japanese_names.html

COPY ./static/style.css ./static/style.css

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=37112"]

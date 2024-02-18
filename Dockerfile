FROM python:alpine

WORKDIR /app

COPY requirements.txt .

# main BE
COPY ./src/app.py .

# main FE
COPY ./src/templates/index.html ./templates/index.html
COPY ./src/templates/about.html ./templates/about.html

COPY ./src/static/style.css ./static/style.css
COPY ./src/static/main.js ./static/main.js
COPY ./src/static/script_copy.js ./static/script_copy.js
COPY ./src/static/rss_feed.js ./static/rss_feed.js

# applications BE
COPY ./src/random_heads_tails.py .
COPY ./src/random_top_analyze.py .
COPY ./src/japanese_name_generator.py .
COPY ./src/generate_passwords.py .
COPY ./src/rss_parser3.py .

# application FE
COPY ./src/templates/random_heads_tails.html ./templates/random_heads_tails.html
COPY ./src/templates/random_top_analyze.html ./templates/random_top_analyze.html
COPY ./src/templates/random_japanese_names.html ./templates/random_japanese_names.html
COPY ./src/templates/random_password.html ./templates/random_password.html
COPY ./src/templates/rss_parser.html ./templates/rss_parser.html

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=37112"]

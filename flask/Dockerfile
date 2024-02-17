FROM python:alpine

WORKDIR /app

COPY requirements.txt .

# main BE
COPY app.py .

# main FE
COPY ./templates/index.html ./templates/index.html
COPY ./templates/about.html ./templates/about.html

COPY ./static/style.css ./static/style.css
COPY ./static/main.js ./static/main.js
COPY ./static/script_copy.js ./static/script_copy.js

# applications BE
COPY random_heads_tails.py .
COPY random_top_analyze.py .
COPY japanese_name_generator.py .
COPY generate_passwords.py .

# application FE
COPY ./templates/random_heads_tails.html ./templates/random_heads_tails.html
COPY ./templates/random_top_analyze.html ./templates/random_top_analyze.html
COPY ./templates/random_japanese_names.html ./templates/random_japanese_names.html
COPY ./templates/random_password.html ./templates/random_password.html

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=37112"]

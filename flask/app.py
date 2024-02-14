from flask import Flask, render_template, request
from random_heads_tails import coin_flip
from random_top_analyze import top_analyze, config

app = Flask(__name__)

@app.route('/random_heads_tails', methods=['GET', 'POST'])
def random_heads_tails():
    if request.method == 'POST':    
        return coin_flip()
    else:
        return render_template('random_heads_tails.html')  

@app.route('/random_top_analyze', methods=['GET', 'POST'])
def random_top_analyze():
    if request.method == 'POST':
        return top_analyze()
    else:
        return render_template('random_top_analyze.html', 
                               default_first_number=config['first_number'], 
                               default_last_number=config['last_number'], 
                               default_numbers_to_select=config['numbers_to_select'], 
                               default_simulation_runs=config['simulation_runs'])

@app.route('/')
def index():
    return render_template('index.html', title='Home Page')

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, render_template, request
from random_heads_tails import coin_flip
from random_top_analyze import top_analyze, config
from japanese_name_generator import JapaneseNameGenerator

app = Flask(__name__)

def generate_japanese_names(num_names, save_to_file, sex):
    name_generator = JapaneseNameGenerator(num_names=num_names, save_to_file=save_to_file, params={"sex": sex})
    random_names = name_generator.generate_names()
    return random_names

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_names = int(request.form.get('num_names', 1))
        save_to_file = bool(request.form.get('save_to_file', False))
        sex = request.form.get('sex', 'male')
        
        # Get names and return to page
        random_names = generate_japanese_names(num_names, save_to_file, sex)
        return render_template('index.html', names=random_names)
    else:
        return render_template('index.html', names=[])

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

@app.route('/random_japanese_names', methods=['GET', 'POST'])
def random_japanese_names():
    if request.method == 'POST':
        num_names = int(request.form.get('num_names', 1))
        sex = request.form.get('sex', 'male')
        save_to_file = bool(request.form.get('save_to_file', False))
        name_generator = JapaneseNameGenerator(num_names=num_names, save_to_file=save_to_file, params={"sex": sex})
        names = name_generator.generate_names()
        return render_template('random_japanese_names.html', names=names)
    else:
        return render_template('random_japanese_names.html')

# API 
@app.route('/api/generate_names', methods=['GET'])
def generate_names_api():
    num_names = int(request.args.get('num_names', 1))
    save_to_file = bool(request.args.get('save_to_file', False))
    sex = request.args.get('sex', 'male')
    
    name_generator = JapaneseNameGenerator(num_names=num_names, save_to_file=save_to_file, params={"sex": sex})
    names = name_generator.generate_names()
    return jsonify({"names": names})

if __name__ == '__main__':
    app.run(debug=True)

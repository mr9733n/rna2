import secrets
import string
from flask import Flask, jsonify, render_template, request
from random_heads_tails import coin_flip
from random_top_analyze import top_analyze, config
from japanese_name_generator import JapaneseNameGenerator
from generate_passwords import decorate_password, generate_passphrase, generate_passwords, generate_pronounceable_password, word_list

__version__ = '1.2.1'

app = Flask(__name__)

routes_info = {
    'index': {'title': 'Home','description': 'Home Page', 'show_in_menu': True},
    'about': {'title': 'About','description': 'About this application', 'show_in_menu': True},
    'random_heads_tails': {'title': 'Random Heads Tails','description': 'Coin Flip', 'show_in_menu': True},
    'random_top_analyze': {'title': 'Random Top Analyze','description': 'Random Top Analyze', 'show_in_menu': True},
    'random_japanese_names': {'title': 'Random Japanese Name','description': 'Random Japanese Name', 'show_in_menu': True},
    'generate_names_api': {'title': 'Random Japanese Name API','description': 'Usage:\n GET http://localhost:5000/api/generate_names?num_names=5&sex=male&save_to_file=true', 'show_in_menu': False},
    'generate_password': {'title': 'Password Generator', 'description': 'Password Generator', 'show_in_menu': True},
    # '  '
    # Add new routes here...
}

def generate_japanese_names(num_names, save_to_file, sex):
    name_generator = JapaneseNameGenerator(num_names=num_names, save_to_file=save_to_file, params={"sex": sex})
    random_names = name_generator.generate_names()
    return random_names

def get_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and not rule.rule.startswith('/static'):
            route_info = routes_info.get(rule.endpoint, {})
            title = route_info.get('title', 'No title')
            description = route_info.get('description', 'No description available')
            show_in_menu = route_info.get('show_in_menu', False)
            routes.append({
                'endpoint': rule.endpoint, 
                'title': title,
                'description': description,
                'show_in_menu': show_in_menu
            })
    return routes

@app.context_processor
def inject_routes():
    return dict(routes=get_routes())

@app.route('/about')
def about():
    return render_template('about.html', title='About', version=__version__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Home page showing different functionalities """
    if request.method == 'POST':
        num_names = int(request.form.get('num_names', 1))
        save_to_file = bool(request.form.get('save_to_file', False))
        sex = request.form.get('sex', 'male')
        
        random_names = generate_japanese_names(num_names, save_to_file, sex)
        return render_template('index.html', names=random_names, version=__version__)
    else:
        return render_template('index.html', names=[], version=__version__)

@app.route('/random_heads_tails', methods=['GET', 'POST'])
def random_heads_tails():
    """ Flip a coin to get heads or tails """
    if request.method == 'POST':    
        return coin_flip(__version__)
    else:
        return render_template('random_heads_tails.html', version=__version__)  

@app.route('/random_top_analyze', methods=['GET', 'POST'])
def random_top_analyze():
    """ Random Top Analyze """
    if request.method == 'POST':
        return top_analyze(__version__)
    else:
        return render_template('random_top_analyze.html', 
                               default_first_number=config['first_number'], 
                               default_last_number=config['last_number'], 
                               default_numbers_to_select=config['numbers_to_select'], 
                               default_simulation_runs=config['simulation_runs'], version=__version__)

@app.route('/random_japanese_names', methods=['GET', 'POST'])
def random_japanese_names():
    """ Random Japanese Name Generator """
    if request.method == 'POST':
        num_names = int(request.form.get('num_names', 1))
        sex = request.form.get('sex', 'male')
        save_to_file = bool(request.form.get('save_to_file', False))
        name_generator = JapaneseNameGenerator(num_names=num_names, save_to_file=save_to_file, params={"sex": sex})
        names = name_generator.generate_names()
        return render_template('random_japanese_names.html', names=names, version=__version__)
    else:
        return render_template('random_japanese_names.html', version=__version__)
    
@app.route('/generate-password', methods=['GET', 'POST'])
def generate_password():
    """ Random Password Generator """
    data = request.form
    num_passwords = int(data.get('num_passwords', 5))
    password_length = int(data.get('password_length', 32))
    uppercase = 'uppercase' in data
    lowercase = 'lowercase' in data
    digits = 'digits' in data
    symbols = 'symbols' in data
    decorate_passwords = 'decorate_passwords' in data
    method_pronounceable = 'method_pronounceable' in data
    method_passphrase = 'method_passphrase' in data
    secret = data.get('secret', '')
    new_word_list = ', '.join(word_list)
    word_list_text = data.get('word_list', '')
    custom_word_list = [word.strip() for word in word_list_text.split(',') if word.strip()]

    generated_passwords = []

    if request.method == 'POST':
        for _ in range(num_passwords):
            password = ''
            if method_pronounceable:
                password = generate_pronounceable_password(password_length)
            elif method_passphrase:
                word_list_to_use = custom_word_list if custom_word_list else word_list
                password = generate_passphrase(4, word_list_to_use)
            else:
                password = generate_passwords(1, password_length, uppercase, lowercase, digits, symbols, secret, decorate_passwords=decorate_passwords)[0]
            if decorate_passwords:
                if method_passphrase:
                    segments = password.split('-')
                    modified_segments = []
                    for segment in segments:
                        modified_segment = segment
                        if uppercase:
                            modified_segment = modified_segment.capitalize()
                        if digits:
                            modified_segment += secrets.choice(string.digits)
                        modified_segments.append(modified_segment)
                    password = '-'.join(modified_segments)
                elif method_pronounceable:
                    segments = decorate_password(password, 4)
                    modified_segments = []
                    for segment in segments.split('-'):
                        if segment:  
                            if uppercase or digits:
                                if uppercase:
                                    segment = segment.capitalize()
                                if digits:
                                    segment += secrets.choice(string.digits)
                            modified_segments.append(segment)
                    password = '-'.join(modified_segments)

            generated_passwords.append(password)

        word_list_for_template = ', '.join(custom_word_list) if custom_word_list else ', '.join(word_list)
        return render_template('random_password.html', word_list=word_list_for_template, passwords=generated_passwords, version=__version__, use_secret=bool(secret))
    else:
        return render_template('random_password.html', word_list=new_word_list, version=__version__)

# Template 
# @app.route('/route')
# def route():
#    """ Provide information about the application and its creators """
#    return render_template('route.html', title='route', version=__version__)

# API 
@app.route('/api/generate_names', methods=['GET'])
def generate_names_api():
    """ Random Japanese Name Generator API """
    num_names = int(request.args.get('num_names', 1))
    save_to_file = bool(request.args.get('save_to_file', False))
    sex = request.args.get('sex', 'male')
    
    name_generator = JapaneseNameGenerator(num_names=num_names, save_to_file=save_to_file, params={"sex": sex})
    names = name_generator.generate_names()
    return jsonify({"names": names}, {"version": __version__})

#
if __name__ == '__main__':
    app.run(debug=True)

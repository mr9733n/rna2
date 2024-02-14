from flask import Flask, jsonify, render_template, request
from random_heads_tails import coin_flip
from random_top_analyze import top_analyze, config
from japanese_name_generator import JapaneseNameGenerator

app = Flask(__name__)

routes_info = {
    'index': {'title': 'Home','description': 'Home Page', 'show_in_menu': True},
    'about': {'title': 'About','description': 'About this application', 'show_in_menu': True},
    'random_heads_tails': {'title': 'Random Heads Tails','description': 'Coin Flip', 'show_in_menu': True},
    'random_top_analyze': {'title': 'Random Top Analyze','description': 'Random Top Analyze', 'show_in_menu': True},
    'random_japanese_names': {'title': 'Random Japanese Name','description': 'Random Japanese Name', 'show_in_menu': True},
    'generate_names_api': {'title': 'Random Japanese Name API','description': 'Usage:\n GET http://localhost:5000/api/generate_names?num_names=5&sex=male&save_to_file=true', 'show_in_menu': False},
    # ''
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
    return render_template('about.html', title='About Us')

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Home page showing different functionalities """
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
    """ Flip a coin to get heads or tails """
    if request.method == 'POST':    
        return coin_flip()
    else:
        return render_template('random_heads_tails.html')  

@app.route('/random_top_analyze', methods=['GET', 'POST'])
def random_top_analyze():
    """ Random Top Analyze """
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
    """ Random Japanese Name Generator """
    if request.method == 'POST':
        num_names = int(request.form.get('num_names', 1))
        sex = request.form.get('sex', 'male')
        save_to_file = bool(request.form.get('save_to_file', False))
        name_generator = JapaneseNameGenerator(num_names=num_names, save_to_file=save_to_file, params={"sex": sex})
        names = name_generator.generate_names()
        return render_template('random_japanese_names.html', names=names)
    else:
        return render_template('random_japanese_names.html')
# 
# @app.route('/route')
# def route():
#    """ Provide information about the application and its creators """
#    return render_template('route.html', title='route')

# API 
@app.route('/api/generate_names', methods=['GET'])
def generate_names_api():
    """ Random Japanese Name Generator API """
    num_names = int(request.args.get('num_names', 1))
    save_to_file = bool(request.args.get('save_to_file', False))
    sex = request.args.get('sex', 'male')
    
    name_generator = JapaneseNameGenerator(num_names=num_names, save_to_file=save_to_file, params={"sex": sex})
    names = name_generator.generate_names()
    return jsonify({"names": names})

if __name__ == '__main__':
    app.run(debug=True)

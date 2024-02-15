from flask import render_template, request

import numpy as np

def flip_coin(num_flips):
    coin_flips = np.random.choice(['heads', 'tails'], num_flips)
    heads_count = np.sum(coin_flips == 'heads')
    tails_count = num_flips - heads_count
    heads_percentage = round((heads_count / num_flips) * 100, 8)
    tails_percentage = round((tails_count / num_flips) * 100, 8)
    return heads_percentage, tails_percentage

def coin_flip(version):
    if request.method == 'POST':
        num_flips = int(request.form['num_flips'])
        heads_percentage, tails_percentage = flip_coin(num_flips)
        return render_template('random_heads_tails.html', show_results=True, heads=heads_percentage, tails=tails_percentage, version=version)
    else:
        return render_template('random_heads_tails.html', show_results=False, version=version)

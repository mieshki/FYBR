from flask import Blueprint, render_template

views = Blueprint('vies', __name__)

@views.route('/maps/index')
def mapa():
    return render_template('maps/index.html')

@views.route('/map')
def get_map():
    return render_template('maps/map.html')
from flask import Blueprint, render_template, request
from calculations import beam_pd  # Assuming calculations are in a separate module

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/generate', methods=['POST'])
def generate():
    beam_type = request.form['beam_type']
    length = int(request.form['length'])
    df = beam_pd(beam_type, length)
    return render_template('results.html', df=df)
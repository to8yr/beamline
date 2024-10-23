from flask import Flask, render_template, request
from calculations import beam_pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
  beam_type = request.form['beam_type']
  length = int(request.form['length'])
  parts = beam_pd(beam_type, length)
  html = parts.to_html(index=False, border=0, justify='center')
  return render_template('result.html', tables=[html], titles=parts.columns.values)

if __name__ == '__main__':
    app.run()
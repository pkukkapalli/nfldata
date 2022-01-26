from flask import Flask

app = Flask(__name__)

@app.route('/api/coaches')
def all_coaches():
    return {'resource': 'coaches'}

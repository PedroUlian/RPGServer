from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Servidor Flask funcionando!</h1><p>Bem-vindo ao seu servidor web.</p>'

@app.route('/api/hello')
def hello():
    return jsonify({
        'message': 'Olá do servidor Flask!',
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

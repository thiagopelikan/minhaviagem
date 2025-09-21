from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

VIAGEM_DATA = datetime(2025, 10, 10)

@app.route('/dias_para_viagem', methods=['GET'])
def dias_para_viagem():
    hoje = datetime.now()
    dias_restantes = (VIAGEM_DATA - hoje).days
    if dias_restantes < 0:
        mensagem = "A viagem já aconteceu!"
    elif dias_restantes == 0:
        mensagem = "A viagem é hoje!"
    else:
        mensagem = f"Faltam {dias_restantes} dias para a viagem."
    return jsonify({
        "dias_restantes": dias_restantes,
        "mensagem": mensagem
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

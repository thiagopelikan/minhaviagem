
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Lista de tools MCP disponíveis
MCP_TOOLS = [
    {
        "name": "dias_para_viagem",
        "description": "Retorna quantos dias faltam para a viagem (10/10/2025)",
        "endpoint": "/mcp/tool/dias_para_viagem",
        "method": "POST"
    }
]

VIAGEM_DATA = datetime(2025, 10, 10)

def calcular_dias_para_viagem():
    hoje = datetime.now()
    dias_restantes = (VIAGEM_DATA - hoje).days
    if dias_restantes < 0:
        mensagem = "A viagem já aconteceu!"
    elif dias_restantes == 0:
        mensagem = "A viagem é hoje!"
    else:
        mensagem = f"Faltam {dias_restantes} dias para a viagem."
    return {
        "dias_restantes": dias_restantes,
        "mensagem": mensagem
    }

@app.route('/mcp/tool/dias_para_viagem', methods=['POST'])
def mcp_tool_dias_para_viagem():
    # Recebe o JSON da Alexa
    data = request.get_json(force=True)
    print("[LOG] JSON recebido da Alexa:", data)
    request_type = data.get("request", {}).get("type")
    intent_name = data.get("request", {}).get("intent", {}).get("name")

    if request_type == "LaunchRequest":
        alexa_response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Bem-vindo à Skill Dias para Viagem! Pergunte quantos dias faltam para a viagem."
                },
                "shouldEndSession": False
            }
        }
        return jsonify(alexa_response)
    elif request_type == "IntentRequest" and intent_name == "DiasParaViagemIntent":
        resultado = calcular_dias_para_viagem()
        alexa_response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": resultado["mensagem"]
                },
                "shouldEndSession": True
            }
        }
        return jsonify(alexa_response)
    else:
        # Resposta padrão para intents desconhecidos
        alexa_response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Desculpe, não entendi o pedido."
                },
                "shouldEndSession": True
            }
        }
        return jsonify(alexa_response)

# Novo endpoint para listar as tools MCP
@app.route('/mcp/tools', methods=['GET'])
def listar_tools_mcp():
    return jsonify({"tools": MCP_TOOLS})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

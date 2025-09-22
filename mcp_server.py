
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
    },
    {
        "name": "roteiro",
        "description": "Retorna o roteiro do dia informado (de 10/10/2025 a 25/10/2025)",
        "endpoint": "/mcp/tool/roteiro",
        "method": "POST"
    }
]
# Novo endpoint para listar as tools MCP
import json

def get_roteiro_by_date(date_str):
    try:
        with open("roteiro.json", "r") as f:
            roteiros = json.load(f)
        return roteiros.get(date_str)
    except Exception as e:
        print("[LOG] Erro ao ler roteiro.json:", e)
        return None

# Endpoint do roteiro
@app.route('/mcp/tool/roteiro', methods=['POST'])
def mcp_tool_roteiro():
    data = request.get_json(force=True)
    print("[LOG] JSON recebido da Alexa (roteiro):", data)
    request_type = data.get("request", {}).get("type")
    intent_name = data.get("request", {}).get("intent", {}).get("name")
    slots = data.get("request", {}).get("intent", {}).get("slots", {})
    # Aceita tanto 'date' (Alexa padrão) quanto 'data' (personalizado)
    date_slot = None
    if slots.get("date") and slots["date"].get("value"):
        date_slot = slots["date"]["value"]
    elif slots.get("data") and slots["data"].get("value"):
        date_slot = slots["data"]["value"]

    # Se não informar data, pede para usuário informar
    if not date_slot:
        alexa_response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Qual data da viagem você gostaria de saber o roteiro? Diga uma data entre 10 e 25 de outubro de 2025."
                },
                "shouldEndSession": False
            }
        }
        return jsonify(alexa_response)

    roteiro = get_roteiro_by_date(date_slot)
    if roteiro:
        alexa_response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": roteiro
                },
                "shouldEndSession": True
            }
        }
    else:
        alexa_response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Desculpe, não tenho roteiro para essa data. Diga uma data entre 10 e 25 de outubro de 2025."
                },
                "shouldEndSession": False
            }
        }
    return jsonify(alexa_response)

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
                    "text": "Bem-vindo à Skill Dias para Viagem! Você pode perguntar quantos dias faltam para a viagem ou pedir o roteiro de qualquer dia entre 10 e 25 de outubro de 2025."
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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

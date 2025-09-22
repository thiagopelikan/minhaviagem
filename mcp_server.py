from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Endpoint do roteiro
@app.route('/mcp/tool/roteiro', methods=['POST'])
def mcp_tool_roteiro():
    print("[LOG] Entrou na função mcp_tool_roteiro")
    data = request.get_json(force=True)
    print("[LOG] JSON recebido da Alexa (roteiro):", data)
    request_type = data.get("request", {}).get("type")
    intent_name = data.get("request", {}).get("intent", {}).get("name")
    slots = data.get("request", {}).get("intent", {}).get("slots", {})
    dialog_state = data.get("request", {}).get("dialogState")
    # Aceita tanto 'date' (Alexa padrão) quanto 'data' (personalizado)
    slot_raw = slots.get('date', {})
    slot_value = slot_raw.get('value')
    slot_slotvalue = slot_raw.get('slotValue', {}).get('value') if slot_raw.get('slotValue') else None
    date_slot = None
    if slot_value:
        date_slot = str(slot_value).strip()
    elif slot_slotvalue:
        date_slot = str(slot_slotvalue).strip()
    elif slots.get("data"):
        if slots["data"].get("value"):
            date_slot = str(slots["data"]["value"]).strip()
        elif slots["data"].get("slotValue") and slots["data"]["slotValue"].get("value"):
            date_slot = str(slots["data"]["slotValue"]["value"]).strip()
    print(f"[LOG] Intent recebido: {intent_name}")
    print(f"[LOG] Slot date value: {slot_value}")
    print(f"[LOG] Slot date slotValue.value: {slot_slotvalue}")
    print(f"[LOG] dialogState: {dialog_state}")
    print(f"[LOG] Valor final usado para busca no roteiro: {date_slot}")
    print(f"[LOG] Checagem Dialog.DelegateRequest: {data.get('request', {}).get('type')}")
    if data.get("request", {}).get("type") == "Dialog.DelegateRequest":
        delegate_request = {
            "version": "1.0",
            "response": {
                "directives": [
                    {
                        "type": "Dialog.DelegateRequest",
                        "target": "skill",
                        "period": {"until": "EXPLICIT_RETURN"},
                        "updatedRequest": data["request"].get("updatedRequest", data["request"])
                    }
                ],
                "shouldEndSession": False,
                "type": "_DEFAULT_RESPONSE"
            }
        }
        return jsonify(delegate_request)
    print(f"[LOG] Checagem RoteiroIntent: intent_name={intent_name}, date_slot={date_slot}")
    if intent_name and intent_name.strip().lower() == "roteirointent".lower() and date_slot:
        roteiro = get_roteiro_by_date(date_slot)
        print(f"[LOG] Roteiro encontrado: {roteiro}")
        if roteiro:
            return jsonify({
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": roteiro
                    },
                    "shouldEndSession": True
                }
            })
        else:
            return jsonify({
                "version": "1.0",
                "response": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": "Desculpe, não tenho roteiro para essa data. Diga uma data entre 10 e 25 de outubro de 2025."
                    },
                    "shouldEndSession": False
                }
            })
    print(f"[LOG] Checagem dialogState: dialog_state={dialog_state}")
    print(f"[LOG] Resultado da busca do roteiro: {roteiro}")
    if dialog_state != "COMPLETED":
        print(f"[LOG] Delegando para Alexa. intent_name={intent_name}, date_slot={date_slot}, dialog_state={dialog_state}")
        delegate_response = {
            "version": "1.0",
            "response": {
                "directives": [
                    {
                        "type": "Dialog.Delegate"
                    }
                ],
                "shouldEndSession": False
            }
        }
        return jsonify(delegate_response)
    # Fallback: resposta padrão para intents desconhecidos ou dados ausentes
    print(f"[LOG] Fallback acionado. intent_name={intent_name}, date_slot={date_slot}, dialog_state={dialog_state}")
    alexa_response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": f"Desculpe, não entendi o pedido. intent_name={intent_name}, date_slot={date_slot}, dialog_state={dialog_state}"
            },
            "shouldEndSession": True
        }
    }
    return jsonify(alexa_response)
# Função utilitária para buscar roteiro por data
import json
def get_roteiro_by_date(date_str):
    try:
        with open("roteiro.json", "r") as f:
            print(f"[LOG] get_roteiro_by_date chamada com date: {date_str}")
            roteiros = json.load(f)
            print(f"[LOG] roteiros.json carregado: {roteiros}")
        return roteiros.get(date_str)
    except Exception as e:
        print("[LOG] Erro ao ler roteiro.json:", e)
        return None
print('[LOG] MCP_SERVER.PY INICIADO')

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Endpoint centralizador para Alexa
@app.route('/mcp/tool/minha_viagem', methods=['POST'])
def mcp_tool_minha_viagem():
    print("[LOG] Entrou na função mcp_tool_minha_viagem")
    data = request.get_json(force=True)
    print("[LOG] JSON recebido da Alexa (centralizador):", data)
    # Detecta intent
    intent_name = None
    slots = {}
    dialog_state = None
    if 'request' in data:
        req = data['request']
        intent_name = req.get('intent', {}).get('name')
        slots = req.get('intent', {}).get('slots', {})
        dialog_state = req.get('dialogState')
    print(f"[LOG] Intent detectado: {intent_name}")
    # Resposta personalizada para LaunchRequest
    request_type = data.get("request", {}).get("type")
    if request_type == "LaunchRequest":
        alexa_response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Oi! Me pergunte quantos dias faltam para a viagem ou qual o roteiro."
                },
                "shouldEndSession": False
            }
        }
        return jsonify(alexa_response)
    # Roteia para intent de saída
    if intent_name and intent_name.strip().lower() == "sairintent":
        print("[LOG] Intent de saída detectado")
        alexa_response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Até logo! Bora pra Disney família!"
                },
                "shouldEndSession": True
            }
        }
        return jsonify(alexa_response)
    # Roteia para dias_para_viagem
    if intent_name and intent_name.strip().lower() == "diasparaviagemintent".lower():
        print("[LOG] Redirecionando para dias_para_viagem")
        resposta = mcp_tool_dias_para_viagem()
        # Força shouldEndSession=False
        resp_json = resposta.get_json()
        resp_json["response"]["shouldEndSession"] = False
        return jsonify(resp_json)
    # Roteia para roteiro
    elif intent_name and intent_name.strip().lower() == "roteirointent":
        print("[LOG] Redirecionando para roteiro")
        resposta = mcp_tool_roteiro()
        resp_json = resposta.get_json()
        resp_json["response"]["shouldEndSession"] = False
        return jsonify(resp_json)
    # Fallback
    else:
        print(f"[LOG] Intent não reconhecido: {intent_name}")
        alexa_response = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Desculpe, não entendi o pedido."
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
    return jsonify({"tools": []})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

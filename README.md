

# Minha Viagem MCP Server

Este projeto implementa um servidor MCP (Model Context Protocol) em Python com integração para Alexa, permitindo consultar roteiros de viagem e quantos dias faltam para a viagem. O servidor expõe endpoints HTTP que podem ser usados por Skills Alexa ou qualquer cliente HTTP.

## Funcionalidades
- Endpoint centralizador `/mcp/tool/minha_viagem`: recebe requisições da Alexa e roteia para as funções corretas conforme o intent.
- Endpoint `/mcp/tool/roteiro`: retorna o roteiro do dia informado (de 10/10/2025 a 25/10/2025), usando o arquivo `roteiro.json`.
- Endpoint `/mcp/tool/dias_para_viagem`: retorna quantos dias faltam para a viagem.
- Mensagens personalizadas para LaunchRequest e fallback.

## Estrutura
- `mcp_server.py`: Código principal do servidor MCP, endpoints e lógica de roteamento Alexa.
- `roteiro.json`: Arquivo com os roteiros por data.
- `requirements.txt`: Dependências do projeto.
- `Procfile`: Para deploy em serviços como Render.

## Como rodar localmente
1. Instale as dependências:
    ```bash
    pip install flask
    ```
2. Inicie o servidor:
    ```bash
    python mcp_server.py
    ```
3. Teste os endpoints com curl:
    - Roteiro:
       ```bash
       curl -X POST http://localhost:5000/mcp/tool/roteiro \
          -H "Content-Type: application/json" \
          -d '{"request": {"intent": {"name": "RoteiroIntent", "slots": {"date": {"value": "2025-10-10"}}}}}'
       ```
    - Dias para viagem:
       ```bash
       curl -X POST http://localhost:5000/mcp/tool/dias_para_viagem \
          -H "Content-Type: application/json" \
          -d '{"request": {"intent": {"name": "DiasParaViagemIntent"}}}'
       ```
    - Centralizador Alexa:
       ```bash
       curl -X POST http://localhost:5000/mcp/tool/minha_viagem \
          -H "Content-Type: application/json" \
          -d '{"request": {"type": "LaunchRequest"}}'
       ```

## Como usar com Alexa
- Configure sua Skill para apontar para o endpoint `/mcp/tool/minha_viagem`.
- Envie intents como `DiasParaViagemIntent` ou `RoteiroIntent` conforme exemplos acima.
- O servidor responde com o texto apropriado para cada intent.

## Deploy
- Para deploy em Render, use o comando de start: `python mcp_server.py`.
- Certifique-se de que o arquivo `roteiro.json` está presente no diretório raiz.

## Exemplo de resposta
```json
{
   "version": "1.0",
   "response": {
      "outputSpeech": {
         "type": "PlainText",
         "text": "Faltam 18 dias para a viagem."
      },
      "shouldEndSession": true
   }
}
```

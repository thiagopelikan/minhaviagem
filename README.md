
# MCP Viagem Server (Exemplo MCP)

Este projeto implementa um servidor MCP (Model Context Protocol) em Python, com uma tool chamada "dias_para_viagem". O servidor MCP está habilitado para o protocolo STREAMABLE HTTP, permitindo integração com Alexa e outros clientes.

## Estrutura
- mcp_server.py: Código principal do servidor MCP e definição da tool.
- README.md: Manual do projeto.

## Como rodar

1. Instale as dependências:
   ```bash
   pip install flask
   ```
2. Inicie o servidor MCP:
   ```bash
   python mcp_server.py
   ```
3. Teste o endpoint MCP:
   ```bash
   curl -X POST http://localhost:5000/mcp/tool/dias_para_viagem -H "Content-Type: application/json" -d '{}'
   ```

## Tool MCP: dias_para_viagem
Retorna JSON com o número de dias para a viagem (10/10/2025) e mensagem amigável.

## Protocolo STREAMABLE HTTP
O servidor MCP está habilitado para responder via HTTP, compatível com integração Alexa.

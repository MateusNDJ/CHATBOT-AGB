# Chatbot para E-commerce Agb/Armazém Leste

Este projeto consiste em um chatbot desenvolvido em Python para o e-commerce Agb/Armazém Leste, especializado na venda de produtos de limpeza e cuidados automotivos. O chatbot é capaz de responder automaticamente a perguntas frequentes e também busca informações gerais sobre produtos através da internet.

## Funcionalidades

- **Respostas Pré-prontas**: O chatbot possui uma série de respostas pré-definidas para perguntas comuns, como status de pedidos, problemas de entrega, reembolsos, cancelamentos, entre outros.
- **Busca de Informações sobre Produtos**: O chatbot pode responder a perguntas gerais sobre produtos, utilizando a API do DuckDuckGo para buscar informações relevantes na internet.
- **Integração com a API da Shopee**: O chatbot é integrado com a API da Shopee para buscar e enviar mensagens relacionadas aos pedidos dos clientes.
  
## Estrutura do Projeto

O projeto contém os seguintes arquivos principais:

- `main.py`: O script principal que executa o chatbot.
- `respostas.json`: Um arquivo JSON que contém as respostas pré-prontas do chatbot.
- `.env`: Arquivo para armazenar as variáveis de ambiente, como credenciais da API da Shopee.

## Dependências

Para executar este projeto, você precisa das seguintes bibliotecas Python:

- `requests`: Para fazer chamadas HTTP à API da Shopee e à API do DuckDuckGo.
- `python-dotenv`: Para carregar variáveis de ambiente de um arquivo `.env`.

Você pode instalar essas dependências usando o pip:

```bash
pip install requests python-dotenv

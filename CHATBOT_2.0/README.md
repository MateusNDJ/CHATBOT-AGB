# Chatbot de Atendimento - Shopee

## Descrição

Este é um chatbot automatizado desenvolvido para facilitar o atendimento ao cliente na plataforma Shopee. Ele responde automaticamente a perguntas frequentes sobre status de pedidos, atrasos na entrega, reembolsos e outros tópicos relacionados. O objetivo é oferecer um suporte rápido e eficiente, melhorando a experiência do cliente.

## Funcionalidades

- **Resposta Automática**: O chatbot analisa as mensagens recebidas e responde automaticamente com informações relevantes baseadas em perguntas comuns dos clientes.
- **Integração com a API da Shopee**: O bot utiliza a API da Shopee para buscar mensagens e enviar respostas, garantindo que as interações estejam sempre atualizadas.
- **Mensagens Variadas**: Para evitar respostas repetitivas, o chatbot utiliza uma lista de respostas predefinidas, escolhendo aleatoriamente entre elas.
- **Registro de Logs**: O chatbot registra todas as interações e erros no log, permitindo fácil monitoramento e depuração.
- **Agradecimento ao Cliente**: Após cada resposta, uma mensagem de agradecimento é enviada, proporcionando uma experiência mais amigável ao usuário.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação utilizada para desenvolver o chatbot.
- **Requests**: Biblioteca para fazer chamadas HTTP à API da Shopee.
- **Hashlib**: Biblioteca para gerar assinaturas de segurança para autenticação na API.
- **OS**: Para gerenciar variáveis de ambiente.
- **Logging**: Para registrar informações e erros em um log.

## Configuração

### Pré-requisitos

Certifique-se de ter o Python 3.x instalado em sua máquina. Você também precisará das seguintes bibliotecas, que podem ser instaladas via pip:

```bash
pip install requests

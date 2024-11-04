import requests
import time
import hashlib
import random
import logging
import os
import re

# Configurações da API da Shopee vindas das variáveis de ambiente
PARTNER_ID = os.getenv("SHOPEE_PARTNER_ID")
API_KEY = os.getenv("SHOPEE_API_KEY")
SECRET_KEY = os.getenv("SHOPEE_SECRET_KEY")
SHOP_ID = os.getenv("SHOPEE_SHOP_ID")

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Respostas predefinidas
respostas = {
    "status do pedido": [
        "Olá! Seu pedido está a caminho ou está sendo preparado para envio.",
    ],
    "demora com a entrega": [
        "Olá! Pedimos desculpas pela demora na entrega. Por favor, aguarde mais 24-48 horas e, se o pedido não chegar, entre em contato com o suporte da Shopee.",
        "Olá! Você verificou com seus vizinhos? Pode ser que alguém tenha recebido por engano.",
    ],
    "reembolso/cancelamento": [
        "Olá! Não conseguimos efetuar o cancelamento, pois a Shopee só nos dá a opção de colocar o estoque como esgotado. Por favor, verifique com o suporte da Shopee para cancelar.",
        "Olá! Infelizmente não podemos cancelar, pois seu pacote já está a caminho. Recuse o pacote no ato da entrega ou devolva para reembolso.",
    ],
    "extraviado ou veio com defeito": [
        "Olá! O(A) senhor(a) verificou com seus vizinhos? Às vezes, os pedidos são entregues a vizinhos por engano.",
        "Olá! Poderia nos enviar uma imagem do produto que recebeu e do pacote que ele veio? O pacote chegou avariado?",
        "Olá! Provavelmente o pedido foi danificado ou perdido durante o trajeto. Fique tranquilo, o valor pago será reembolsado.",
    ],
    "outras_perguntas": [
        "Desculpe, não entendi sua pergunta. Pode reformular ou fornecer mais detalhes?"
    ],
    "agradecimento": [
        "Agradecemos pelo seu contato! Se precisar de mais ajuda, não hesite em nos chamar.",
    ]
}

# Função para gerar a assinatura da API
def gerar_assinatura(endpoint, timestamp):
    base_string = f"{PARTNER_ID}{endpoint}{timestamp}{SECRET_KEY}"
    return hashlib.sha256(base_string.encode()).hexdigest()

# Função para buscar mensagens da Shopee
def buscar_mensagens():
    try:
        endpoint = "/v2/message/get_message"
        timestamp = int(time.time())
        assinatura = gerar_assinatura(endpoint, timestamp)

        url = f"https://partner.shopee.com/api/v2{endpoint}"
        headers = {"Content-Type": "application/json"}
        parametros = {
            "partner_id": PARTNER_ID,
            "timestamp": timestamp,
            "sign": assinatura,
            "shop_id": SHOP_ID
        }

        response = requests.get(url, headers=headers, params=parametros)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar mensagens: {e}")
        return {"erro": "Não foi possível obter as mensagens"}

# Função para enviar uma resposta
def enviar_resposta(mensagem_id, resposta):
    try:
        endpoint = "/v2/message/send_message"
        timestamp = int(time.time())
        assinatura = gerar_assinatura(endpoint, timestamp)

        url = f"https://partner.shopee.com/api/v2{endpoint}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "partner_id": PARTNER_ID,
            "timestamp": timestamp,
            "sign": assinatura,
            "shop_id": SHOP_ID,
            "message_id": mensagem_id,
            "message": resposta
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        logging.info(f"Resposta enviada para a mensagem ID {mensagem_id}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar resposta: {e}")

# Função para gerar uma resposta baseada no conteúdo da mensagem
def gerar_resposta(conteudo):
    conteudo = conteudo.lower()
    if re.search(r"status do pedido", conteudo):
        return random.choice(respostas["status do pedido"])
    elif re.search(r"demora|entrega", conteudo):
        return random.choice(respostas["demora com a entrega"])
    elif re.search(r"reembolso|cancelamento", conteudo):
        return random.choice(respostas["reembolso/cancelamento"])
    elif re.search(r"extraviado|defeito", conteudo):
        return random.choice(respostas["extraviado ou veio com defeito"])
    else:
        return random.choice(respostas["outras_perguntas"])

# Função do chatbot para responder automaticamente
def responder_automaticamente():
    mensagens = buscar_mensagens()
    if "erro" not in mensagens:
        for mensagem in mensagens.get("data", []):
            conteudo = mensagem.get("content", "")
            mensagem_id = mensagem.get("id")

            # Gerar uma resposta baseada no conteúdo da mensagem
            resposta = gerar_resposta(conteudo)

            # Enviar a resposta de volta
            enviar_resposta(mensagem_id, resposta)

            # Enviar mensagem de agradecimento
            enviar_resposta(mensagem_id, random.choice(respostas["agradecimento"]))

# Executar o chatbot em um loop
if __name__ == "__main__":
    while True:
        responder_automaticamente()
        time.sleep(60)  # Aguarda 60 segundos antes de buscar novas mensagens

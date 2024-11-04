import requests
import time
import hashlib
import random
import logging
import os
import re
import json  # Importar o módulo JSON

# Configurações da API da Shopee vindas das variáveis de ambiente
PARTNER_ID = os.getenv("SHOPEE_PARTNER_ID")
API_KEY = os.getenv("SHOPEE_API_KEY")
SECRET_KEY = os.getenv("SHOPEE_SECRET_KEY")
SHOP_ID = os.getenv("SHOPEE_SHOP_ID")

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para carregar respostas do arquivo JSON
def carregar_respostas():
    with open('respostas.json', 'r', encoding='utf-8') as f:
        return json.load(f)

respostas = carregar_respostas()

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

# Função do chatbot para responder automaticamente
def responder_automaticamente():
    mensagens = buscar_mensagens()
    if "erro" not in mensagens:
        for mensagem in mensagens.get("data", []):
            conteudo = mensagem.get("content", "").lower()
            mensagem_id = mensagem.get("id")

            # Respostas com base em perguntas frequentes
            if "status do meu pedido" in conteudo:
                resposta = random.choice(respostas["status do pedido"])
            elif "demora" in conteudo or "entrega" in conteudo:
                resposta = random.choice(respostas["demora com a entrega"])
            elif "cancelar meu pedido" in conteudo:
                resposta = random.choice(respostas["reembolso/cancelamento"])
            elif "chegou danificado" in conteudo or "defeito" in conteudo:
                resposta = random.choice(respostas["extraviado ou veio com defeito"])
            elif "solicitar reembolso" in conteudo:
                resposta = random.choice(respostas["reembolso/cancelamento"])
            elif "alterar o endereço de entrega" in conteudo:
                resposta = random.choice(respostas["reembolso/cancelamento"])
            elif "troca e devolução" in conteudo:
                resposta = random.choice(respostas["reembolso/cancelamento"])
            elif "pedido extraviado" in conteudo:
                resposta = random.choice(respostas["extraviado ou veio com defeito"])
            elif "acompanhar meu pedido" in conteudo:
                resposta = random.choice(respostas["status do pedido"])
            elif "promoções" in conteudo or "cupons" in conteudo:
                resposta = random.choice(respostas["promoções e cupons"])
            else:
                resposta = random.choice(respostas["outras_perguntas"])

            # Enviar a resposta ao cliente
            enviar_resposta(mensagem_id, resposta)
            # Enviar um agradecimento, se aplicável
            if "reembolso" not in conteudo:  # Evitar repetir agradecimento em situações de reembolso
                enviar_resposta(mensagem_id, random.choice(respostas["agradecimento"]))

# Executar o chatbot em um loop
if __name__ == "__main__":
    try:
        while True:
            responder_automaticamente()
            time.sleep(60)  # Aguarda 60 segundos antes de buscar novas mensagens
    except KeyboardInterrupt:
        logging.info("Encerrando o chatbot...")

import os
import jwt
import json
import scrapy
import logging
from dotenv import load_dotenv

class ServimedSpider(scrapy.Spider):
    name = "servimed-spider"

    def __init__(self, argument=None):
        self.order_id = argument
        load_dotenv('.secrets')
        self.user = os.getenv('USER_LOGIN')
        self.password = os.getenv('PASSWORD_LOGIN')
        self.login_url = str(os.getenv('LOGIN_URL'))
        self.order_url = str(os.getenv('ORDER_URL'))

    def start_requests(self):
        payload = {
            'usuario': self.user,
            'senha': self.password,
        }

        logging.info('Realizando login ...')

        yield scrapy.Request(
            url=self.login_url,
            method='POST',
            body=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
            callback=self.after_login
        )

    def after_login(self, response):
        if "erro" in response.body.decode():
            logging.error("Login falhou")
            return

        logging.info("Login bem-sucedido. Continuando a navegação.")

        user_data = json.loads(response.text)
        self.userId = user_data['usuario']['codigoUsuario']

        cookies = self.extract_cookies(response.headers.getlist("Set-Cookie"))
        decoded_jwt = jwt.decode(
            cookies["accesstoken"],
            algorithms=["RS256"],
            options={"verify_signature": False}
        )
        access_token_id = decoded_jwt["token"]
        logged_user = decoded_jwt["codigoUsuario"]

        headers = {
            "accept": "application/json, text/plain, */*",
            "accesstoken": access_token_id,
            "contenttype": "application/json",
            "loggeduser": str(logged_user),
        }

        logging.info('Procurando pedido ...')

        response2 = scrapy.Request(
            url= self.order_url + str(self.order_id),
            headers=headers,
            callback=self.get_order_data,
            errback=self.get_order_data
        )
        yield response2

    def extract_cookies(self, cookies):
        cookie_dict = {}
        for cookie in cookies:
            cookie_str = cookie.decode('utf-8').split(';')[0]
            key, value = cookie_str.split('=', 1)
            cookie_dict[key] = value
        return cookie_dict

    def get_order_data(self, response):
        order = json.loads(response.text)

        itens = []
        order_data = {
            "motivo": '',
        }

        if (not order['itens']) or (order['usuarioCodigoExterno'] != self.userId):
            erro = {
                'ERROR': 'PEDIDO_NAO_ENCONTRADO'
            }
            logging.error(erro)
            return

        if order['rejeicao']:
            order_data["motivo"] = order['rejeicao'].strip()

        logging.info(f'Pedido {self.order_id} encontrado')
        logging.info(f'Situação: {order["pedidoStatusId"]}')
        logging.info('Retornando itens')

        for item in order['itens']:
            item_data = {
                "codigo_produto": item['produtoId'],
                "descricao": item['produto']['descricao'],
                "quantidade_faturada": item['quantidadeFaturada']
            }
            itens.append(item_data)

        order_data['itens'] = itens
        filename = f'./output/order-{self.order_id}.json'

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, 'w') as file:
            json.dump(order_data, file, indent=4)

        yield order_data


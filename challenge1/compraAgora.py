import os
import json
import logging
import time
from binascii import unhexlify
from dotenv import load_dotenv
from nacl.public import PublicKey, SealedBox

class CompraAgora:

    def __init__(self, session):
        self._session = session
        load_dotenv('.secrets')
        self.user = os.getenv('USER_LOGIN')
        self.password = os.getenv('PASSWORD_LOGIN')
        self.public_key_hex = os.getenv('PUBLIC_KEY')
        self.login_url = os.getenv('LOGIN_URL')
        self.image_url = os.getenv('IMAGE_URL')
        self.products_final = []
        self.logger = logging.getLogger(__name__)
        self.category_urls = {
            'alimentos': os.getenv('FOOD_CATEGORY_URL'),
            'bazar': os.getenv('BAZAAR_CATEGORY_URL'),
            'bebidas': os.getenv('DRINKS_CATEGORY_URL'),
            'bomboniere': os.getenv('BOMBONIERE_CATEGORY_URL'),
            'cuidados_pessoais': os.getenv('PERSONAL_CARE_CATEGORY_URL'),
            'laticinios': os.getenv('DAIRY_PRODUCTS_CATEGORY_URL'),
            'pets': os.getenv('PET_CATEGORY_URL'),
            'roupa_casa': os.getenv('HOUSEHOLD_CATEGORY_URL'),
            'sorvetes': os.getenv('ICE_CATEGORY_URL'),
        }

    def encrypt_with_public_key(self, payload, public_key_hex) -> str:
        public_key_bytes = unhexlify(public_key_hex)
        public_key = PublicKey(public_key_bytes)
        sealed_box = SealedBox(public_key)

        encrypted_payload = sealed_box.encrypt(payload.encode('utf-8'))

        return encrypted_payload.hex()

    def login(self):
        payload = {
            'usuario_cnpj': self.user,
            'usuario_senha': self.password,
            'eub': 0,
        }

        payload_json = json.dumps(payload)

        encrypted_payload = self.encrypt_with_public_key(
            payload_json,
            self.public_key_hex
            )

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        self.logger.info('Realizando login ...')
        login_response = self._session.post(
            self.login_url,
            json={'data': encrypted_payload},
            headers=headers
        )
        response = json.loads(login_response.text)

        if not response['success']:
            self.logger.error('Login falhou!')
            return
        
        self.logger.error('Login bem-sucedido!')

    def get_all(self):
        for category in self.category_urls:
            self.get_category_data(category)
        self.json_products_file()

    def get_category_data(self, category):
        current_page = 1
        total_page = 1
        products = []
        while current_page <= total_page:
            params = {}
            if current_page > 1:
                params["p"] = current_page

            response = self._session.get(
                self.category_urls[category],
                params=params
            )
            response2 = json.loads(response.text)

            if current_page == 1:
                total_page = response2['paginacao']['PaginasTotal']
                products = response2['produtos']
            else:
                for item in response2['produtos']:
                    products.append(item)

            time.sleep(3)
            current_page += 1

        for product in products:
            product_aux = {}
            product_aux['descricao'] = product['Nome']
            product_aux['descricao_fabricante'] = product['Fabricante']
            product_aux['imagem_url'] = self.image_url + product['Foto']
            self.products_final.append(product_aux)

    def json_products_file(self):
        self.logger.info(json.dumps(self.products_final, indent=4))
        filename = 'products.json'

        with open(filename, 'w') as file:
            json.dump(self.products_final, file, indent=4)

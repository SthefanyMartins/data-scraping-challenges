import logging
import requests
from compraAgora import CompraAgora

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='challenge1.log', level=logging.INFO)
    session = requests.Session()
    logger.info('Started process')
    compra = CompraAgora(session)
    compra.login()
    logger.info('Buscando itens por categoria')
    logger.info('Capturando produtos da categoria: Alimentos e Bebidas ...')
    compra.get_all()
    logger.info('Finished')

if __name__ == '__main__':
    main()
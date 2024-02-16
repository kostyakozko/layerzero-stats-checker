import os

from threading import Thread
from core.app import app
from core.database import DBManager
from core.logger_config import setup_logger
from core.utils import load_wallets_from_file
from loguru import logger
import socket

if __name__ == '__main__':
    setup_logger()

    wallets_list = load_wallets_from_file("data/wallets.txt")
    name_list = load_wallets_from_file("data/names.txt")

    DBManager.create_database(
        wallet_list=wallets_list,
        name_list=name_list,
    )

    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address=s.getsockname()[0]
        print(f"Запущен локальный сервер: https://{ip_address}:8080")
        s.close()

    Thread(target=lambda: app.run(ssl_context=('cert.pem', 'key.pem'), debug=True, use_reloader=False, host='0.0.0.0', port=8080)).start()

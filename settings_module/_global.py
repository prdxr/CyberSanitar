import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

SETTINGS_MODULE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_MODULE)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
